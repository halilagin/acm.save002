
import json
from acm.util.DictionaryAsNestedObjectSerializer import DictionaryAsNestedObjectSerializer
from kafka import KafkaConsumer
import threading, logging, time
from acm.config.ConfigManager import ConfigManager
import multiprocessing



class KafkaClassificationModelConsumerProcess(multiprocessing.Process):

    pass
    
    def __init__(self, configJsonStr ):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.config = DictionaryAsNestedObjectSerializer(json.loads(configJsonStr))
    def run(self):
        pass
        consumer = KafkaConsumer(bootstrap_servers='acm:9092',auto_offset_reset='earliest', consumer_timeout_ms=1000)
        consumer.subscribe(self.config.acm.models.classification.kafkaTopic)
        
        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

        consumer.close()

class KafkaClassificationModelConsumerExecutor(object):
        
        def __init__(self, config):
            pass
            if config==None:
                self.configFile="acm.config.dev.yml"
            self.configManager = ConfigManager(params={"config.file":self.configFile})
            self.config = self.configManager.read()
        def start(self):
            pass
            k = KafkaClassificationModelConsumerProcess(self.config.toJson())
            k.start()
            k.join()

KafkaClassificationModelConsumerExecutor(None).start()
