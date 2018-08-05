
import json
from acm.util.DictionaryAsNestedObjectSerializer import DictionaryAsNestedObjectSerializer
from kafka import KafkaProducer
import multiprocessing
import time
import sys
class KafkaProducerProcess(multiprocessing.Process):
    pass
    
    def __init__(self, configJsonStr, msg):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.config = DictionaryAsNestedObjectSerializer(json.loads(configJsonStr))
        self.msg = msg
    def run(self):
        pass
        try:
            producer = KafkaProducer(bootstrap_servers='acm:9092')
            producer.send(self.config.acm.models.classification.kafkaTopic, self.msg)
            time.sleep(10)
            producer.close()
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise
        

