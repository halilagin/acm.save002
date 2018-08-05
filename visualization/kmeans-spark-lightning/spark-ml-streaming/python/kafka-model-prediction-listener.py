#!/usr/bin/env python
import threading, logging, time

#see: https://raw.githubusercontent.com/dpkp/kafka-python/master/example.py

import multiprocessing
import json
import time
from kafka import KafkaConsumer, KafkaProducer


#from numpy import asarray, array, vstack, hstack, size, random, argsort, ones, argmin, sin, cos, pi
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.datasets import make_blobs

from mlstreaming.base import StreamingDemo
from mlstreaming.util import loadrecent
from lightning import Lightning


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='acm:9092')

        while not self.stop_event.is_set():
            producer.send('my-topic', b"test")
            producer.send('my-topic', b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()

class Consumer(multiprocessing.Process):
    def __init__(self,ncenters=3, ndims=2, std=0.2, seed=None, update='drift', interval=15, transition=None):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        """
        Set up parameters for a streaming kmeans algorithm demo.

        Parameters
        ----------
        ncenters : int, or array-like (ncenters, ndims)
          Number of clusters as an integer, or an array of starting cluster centers.
          If given as an integer, cluster centers will be determined randomly.

        ndims : int
          Number of dimensions

        std : scalar
          Cluster standard deviation

        """

        np.random.seed(seed)
        if np.size(ncenters) == 1:
            centers = np.random.randn(ncenters, ndims) * 2
        else:
            centers = np.asarray(ncenters)
            ncenters = centers.shape[0]
        self.centers = centers
        self.ncenters = ncenters
        self.ndims = ndims
        self.npoints = 50
        self.std = std
        self.update = update
        self.interval = interval
        self.transition = transition
        self.lgnAddress="http://localhost:3010"
        self.lgn = Lightning(self.lgnAddress)
        self.lgn.create_session('kafka-streaming-kmeans')
        self.lgn.session.open()
        
    def stop(self):
        self.stop_event.set()

    def notifyLgn(self,model):
        time.sleep(1)
    # plot an update (if we got a valid model)
        #if len(model) == self.ncenters:

        pts, labels = make_blobs(self.npoints, self.ndims, self.centers, cluster_std=self.std)

        clrs = labels
        order = np.argsort(labels)
        clrs = clrs[order]
        pts = pts[order]
        s = np.ones(self.npoints) * 10

        if self.ndims == 1:
            pts = np.vstack((pts, model[:,None]))
        else:
            print("halil:",pts.shape, model.shape)
            pts = np.vstack((pts, model))
        clrs = np.hstack((clrs, np.ones(self.ncenters) * 5))
        s = np.hstack((s, np.ones(self.ncenters) * 10))

        # wait a few iterations before plotting
        # scatter plot for two dimensions
        viz=None
        if self.ndims == 2:
            if viz is None:
                viz = self.lgn.scatterstreaming(pts[:, 0], pts[:, 1], labels=clrs, size=s)
            else:
                viz.append(pts[:, 0], pts[:, 1], labels=clrs, size=s)

        # line plot for one dimension
        elif self.ndims == 1:
            if viz is None:
                viz = self.lgn.linestreaming(pts, labels=clrs, size=s/2)
            else:
                viz.append(pts, labels=clrs, size=s/2)

        else:
            raise Exception('Plotting only supported with 1 or 2 dimensions')

    def processModelPrediction(self, msg):
        pass
        model_, prediction_ = msg.value.split("-----")
        model=None
        try:
            model = np.fromstring(model_, dtype=floay, sep=",")
        except:
            pass
            model=np.zeros(shape=(1,2))
        print("notify lightning server")
        self.notifyLgn(model) 
    
    

    def run(self):
        #value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer = KafkaConsumer(bootstrap_servers='acm:9092',
                                 auto_offset_reset='earliest',
                                 value_deserializer=lambda m: m.decode('utf-8'),
                                 consumer_timeout_ms=1000)
        consumer.subscribe(['kmeans-output-topic'])

        while not self.stop_event.is_set():
            for message in consumer:
                #print(message)
                self.processModelPrediction(message)
                if self.stop_event.is_set():
                    break

        consumer.close()
        
        
def main():
    tasks = [
        Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)
    
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    #main()
    Consumer().start()
