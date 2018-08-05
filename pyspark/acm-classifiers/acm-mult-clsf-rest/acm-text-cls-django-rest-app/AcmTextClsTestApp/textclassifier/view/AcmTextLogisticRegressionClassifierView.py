

import os
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import viewsets
from AcmTextClsTestApp.textclassifier.serializers import UserSerializer, GroupSerializer



import json
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql.types import StringType, IntegerType, DateType, StructType, StructField, DoubleType


from acm.util.DictionaryAsNestedObjectSerializer import DictionaryAsNestedObjectSerializer
from acm.config.ConfigManager import ConfigManager
from pywebhdfs.webhdfs import PyWebHdfsClient


class AcmTextLogisticRegressionClassifierView(APIView):
    """
    List all snippets, or create a new snippet.
    """


    def hdfsizePath(self, path):
        return self.hdfsServerUrl+path



    def classify(self, inputJson):
        pass

        self.hdfs = PyWebHdfsClient(host=self.config.acm.servers.hdfs.host,port=self.config.acm.servers.hdfs.restPort, user_name=self.config.acm.servers.hdfs.fileOwner)
        self.hdfsServerUrl = "hdfs://"+self.config.acm.servers.hdfs.host+":"+str(self.config.acm.servers.hdfs.port)

        if hasattr(self, 'sc')==False: 
            self.sc =SparkContext()
        if hasattr(self, 'sqlContext')==False:
            self.sqlContext = SQLContext(self.sc)


        schema = StructType([StructField('Category', StringType(), True),
                     StructField('Descript', StringType(), True),
                     StructField('Dates', StringType(), True),
                     StructField('DayOfWeek', StringType(), True),
                     StructField('PdDistrict', StringType(), True),
                     StructField('Resolution', StringType(), True),
                     StructField('Address', StringType(), True),
                     StructField('X', DoubleType(), True),
                     StructField('Y', DoubleType(), True)
                    ])
        test = self.sqlContext.createDataFrame(inputJson, schema)

        #pipeline= PipelineModel.load("/home/halil/gitlab/acm/pyspark/acm-text-classification-rest/lr.model.pipeline.savepoint")
        pipeline= PipelineModel.load(self.pipelineHdfsPath)


        testData = pipeline.transform(test)
        print("Test Dataset Count: " + str(testData.count()))

        ########################################################## 
        ################## Train/load the model ################## 
        ########################################################## 

        #lrModel = LogisticRegressionModel.load("/home/halil/gitlab/acm/pyspark/acm-text-classification-rest/lr.model.savepoint")
        lrModel = LogisticRegressionModel.load(self.modelHdfsPath)

        predictions = lrModel.transform(testData)

        predictions.filter(predictions['prediction'] == 7)  \
            .select("Descript","Category","probability","label","prediction") \
            .orderBy("probability", ascending=False) \
            .show(n = 10, truncate = 30)

        #.select("probability","label","prediction") \
        resultJson = predictions.filter(predictions['prediction'] == 7)  \
            .select("prediction") \
            .orderBy("probability", ascending=False) \
            .toJSON().collect()
        self.sc.stop()

        return ["al sana ML!", resultJson]

    def get(self, request, format=None):
        print ("django-root:",  settings.BASE_DIR)
        self.configFile= os.path.join(settings.BASE_DIR, "acm.config.dev.yml")
        self.configManager = ConfigManager(params={"config.file":self.configFile})
        self.config = self.configManager.read()
        self.hdfsServerUrl = "hdfs://"+self.config.acm.servers.hdfs.host+":"+str(self.config.acm.servers.hdfs.port)

        #jsonFile = '/home/halil/gitlab/acm/pyspark/acm-text-classification-rest/jsontordd.test.json'
        jsonFile =  os.path.join(settings.BASE_DIR, self.config.acm.test.test001.jsonRequestPath)
        self.modelHdfsPath = self.hdfsizePath(self.config.acm.test.test001.modelHdfsPath)
        self.pipelineHdfsPath = self.hdfsizePath(self.config.acm.test.test001.pipelineHdfsPath)

        json_ = None
        with open(jsonFile, 'r') as f:
            content = f.read()
            json_ = json.loads(content)
        ret_ = self.classify(json_)
        return Response(["hello","world!", ret_])

    def post(self, request, format=None):
        return self.get(request, format)
