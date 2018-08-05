#!/usr/bin/env python
import os
import crontab 
import json
from acm.config.ConfigManager import ConfigManager
#see: http://stackabuse.com/scheduling-jobs-with-python-crontab/
class AcmModelTrainerScheduler(object):
    
    def __init__(self,config=None):
        pass
        self.username = "halil"
        self.acmRoot = "/home/halil/gitlab/acm"
        self.logisticRegressionTrainer = os.path.join(self.acmRoot,"pyspark/acm-text-classification/acm/RunMulticlassClassifier.py")
        self.pythonInterpreter="python3.6"
        

        


    def start(self):
        pass
        cron = crontab.CronTab(user=self.username)  
        cmd_ = "%s %s" %(self.pythonInterpreter, self.logisticRegressionTrainer)
        print (cmd_)
        job = cron.new(command=cmd_)  
        job.hour.every(12)
        cron.write()


