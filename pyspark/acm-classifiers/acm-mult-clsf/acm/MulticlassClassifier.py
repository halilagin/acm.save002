#!/usr/bin/env python

import os
import json
import time
from acm.config.ConfigManager import ConfigManager
from multiprocessing import Process, Manager, Queue
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from acm.config.ConfigManager import ConfigManager
from acm.util.DictionaryAsNestedObjectSerializer import DictionaryAsNestedObjectSerializer
from acm.util.ZipFileWriter import ZipFileWriter
from acm.kafka.KafkaProducerProcess import KafkaProducerProcess
from json import JSONEncoder
from kafka import KafkaProducer
from pywebhdfs.webhdfs import PyWebHdfsClient

class MyEncoder (JSONEncoder):
        pass
        def default(self,o):
            return o.__dict__

class MulticlassLogisticRegressionModelTrainer(object):
    pass

    def __init__(self):
        pass

    def hdfsizePath(self, path):
        return self.hdfsServerUrl+path

    def start(self,q,parentEnv, configJsonStr):
        pass
        self.config = DictionaryAsNestedObjectSerializer(json.loads(configJsonStr))
        self.hdfs = PyWebHdfsClient(host=self.config.acm.servers.hdfs.host,port=self.config.acm.servers.hdfs.restPort, user_name=self.config.acm.servers.hdfs.fileOwner)
        self.hdfsServerUrl = "hdfs://"+self.config.acm.servers.hdfs.host+":"+str(self.config.acm.servers.hdfs.port)

        env_ = json.loads(parentEnv)
        py4jExists=False
        for key in env_.keys():
            os.environ[key]=env_[key]
            if "py4j-" in env_[key]:
                py4jExists=True

        ### set pyspark env variable ###
        #os.environ["SPARK_HOME"]="/home/halil/programs/spark230"
        #if os.environ.get("PYTHONPATH") is None:
        #    os.environ["PYTHONPATH"] = os.path.join(os.environ["SPARK_HOME"], "python/")
        #    
        #if py4jExists==False:
        #    os.environ["PYTHONPATH"] = os.path.join(os.environ["SPARK_HOME"], "python/lib/py4j-0.10.6-src.zip")+ ":"+ os.environ["PYTHONPATH"] 


        #set config
        trainDataFiles= self.hdfsizePath(self.config.acm.models.classification.data.hdfs.inputDir+"/*.csv")
        print (trainDataFiles)
        


        sc =SparkContext()
        sqlContext = SQLContext(sc)


        data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(trainDataFiles).limit(1000)
        print(data.columns)

        drop_list = ['Dates', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y']

        data = data.select([column for column in data.columns if column not in drop_list])
        data.show(5)
        data.printSchema()

        # by top 20 categories
        data.groupBy("Category") \
            .count() \
            .orderBy(col("count").desc()) \
            .show()

        # by top 20 descriptions
        data.groupBy("Descript") \
            .count() \
            .orderBy(col("count").desc()) \
            .show()


        # regular expression tokenizer
        regexTokenizer = RegexTokenizer(inputCol="Descript", outputCol="words", pattern="\\W")

        # stop words
        add_stopwords = ["http","https","amp","rt","t","c","the"] # standard stop words

        stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

        # bag of words count
        countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)


        label_stringIdx = StringIndexer(inputCol = "Category", outputCol = "label")

        transformers=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx]

        pipeline = Pipeline(stages=transformers)

        pipelineFit = pipeline.fit(data)
        dataset = pipelineFit.transform(data)

        dataset.show(5)



        ### Randomly split data into training and test sets. set seed for reproducibility
        (trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)
        print("Training Dataset Count: " + str(trainingData.count()))
        print("Test Dataset Count: " + str(testData.count()))

        # Build the model
        lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
        
        # Train model with Training Data
        lrModel = lr.fit(trainingData)
        savedModelsDir=self.hdfsizePath(self.config.acm.models.classification.data.hdfs.savedModels)
        savedModelsZipDir=self.hdfsizePath(self.config.acm.models.classification.data.hdfs.zipDir)
        modelSavePolicy=self.config.acm.models.classification.modelSavePolicy

        if modelSavePolicy=="mostRecentOne":
            time_ms = str(int(time.time()*1000))
            #if not os.path.exists(outputDir):
            #    os.mkdir(outputDir)
            #if not os.path.exists(zipDir):
            #    os.mkdir(zipDir)
            self.hdfs.make_dir(self.config.acm.models.classification.data.hdfs.savedModels)
            self.hdfs.make_dir(self.config.acm.models.classification.data.hdfs.zipDir)
            newModelDirName = self.config.acm.models.classification.data.hdfs.savedModels + "/" + time_ms
            modelOutputPath = newModelDirName+"/model"
            pipelineOutputPath = newModelDirName+"/pipeline"
            self.hdfs.make_dir(newModelDirName)
            self.hdfs.make_dir(modelOutputPath)
            self.hdfs.make_dir(pipelineOutputPath)
            lrModel.write().overwrite().save(self.hdfsizePath( modelOutputPath))
            pipelineFit.write().overwrite().save(self.hdfsizePath(pipelineOutputPath))

            #zer=ZipFileWriter()
            #zipFilePath = os.path.join(zipDir, modelFileName+".zip")
            #zer.zip(zipFilePath, modelOutputPath)
#
#            with open(zipFilePath, mode='rb') as file: # b is important -> binary
#                fileContent = file.read()
#                k = KafkaProducerProcess(configJsonStr,fileContent)
#                k.start()
#                k.join()
#                #producer = KafkaProducer(bootstrap_servers='acm:9092')
#                #producer.send(config.acm.models.classification.kafkaTopic,fileContent)
            


class MulticlassClassifierExecutor(object):
    
    def __init__(self, config=None):
        pass
        if config==None:
            self.configFile="acm.config.dev.yml"
        self.configManager = ConfigManager(params={"config.file":self.configFile})
        self.config = self.configManager.read()


    # this method run as a child process
    # lr: logistic regression
    def lrModelTrainer(self, q, parentEnv, configJsonStr):
        pass
        classifier = MulticlassLogisticRegressionModelTrainer()
        classifier.start(q, parentEnv, configJsonStr)
        q.put(["hello parent!", "I am lrModelTrainer"])

    # this is the start point of parent process
    def start(self):
        pass
        fs = [self.lrModelTrainer] #functions
        ps=[] #processes
        qs=[] # queues
        #passing objects to child process via queue
        env_ = json.dumps(os.environ.copy())
        for f in fs:
            q = Queue() 
            configJsonStr = self.config.toJson()
            p = Process(target=f, args=(q,env_,configJsonStr))
            qs.append(q)
            p.start()
            ps.append(p)
            p.join()
            
        for q in qs:
            print (q.get())
