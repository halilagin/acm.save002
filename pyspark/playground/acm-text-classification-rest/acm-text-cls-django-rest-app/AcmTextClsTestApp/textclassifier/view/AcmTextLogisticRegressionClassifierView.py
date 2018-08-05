from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.models import User, Group
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


class AcmTextLogisticRegressionClassifierView(APIView):
    """
    List all snippets, or create a new snippet.
    """


    def classify(self, inputJson):
        pass
        sc =SparkContext()
        sqlContext = SQLContext(sc)


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
        test = sqlContext.createDataFrame(inputJson, schema)

        pipeline= PipelineModel.load("/home/halil/gitlab/acm/pyspark/acm-text-classification-rest/lr.model.pipeline.savepoint")

        testData = pipeline.transform(test)
        print("Test Dataset Count: " + str(testData.count()))

        ########################################################## 
        ################## Train/load the model ################## 
        ########################################################## 

        lrModel = LogisticRegressionModel.load("/home/halil/gitlab/acm/pyspark/acm-text-classification-rest/lr.model.savepoint")

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

        return ["al sana ML!", resultJson]

    def get(self, request, format=None):
        jsonFile = '/home/halil/gitlab/acm/pyspark/acm-text-classification-rest/jsontordd.test.json'
        json_ = None
        with open(jsonFile, 'r') as f:
            content = f.read()
            json_ = json.loads(content)
        ret_ = self.classify(json_)
        return Response(["hello","world!", ret_])

    def post(self, request, format=None):
        return self.get(request, format)
