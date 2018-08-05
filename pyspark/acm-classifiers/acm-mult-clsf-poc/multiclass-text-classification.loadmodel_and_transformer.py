#!/usr/bin/env python


# we need to save countvectorizer model, the link below shows an example.
# see: https://stackoverflow.com/questions/48924308/countvectorizer-using-same-vocabulary-in-a-second-time

#see: https://spark.apache.org/docs/latest/ml-pipeline.html#pipeline
import json
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, CountVectorizerModel
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline, PipelineModel

sc =SparkContext()
sqlContext = SQLContext(sc)


################################################## 
################## read data ################## 
################################################## 
hdfsPath="/acm/ml/clsf/data/test001"
modelsPath=hdfsPath+"/models"
trainDataFile="./data/sanfrancisco-crime/train.csv"
#data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(trainDataFile).limit(1000)
data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("hdfs://namenode:9000/"+hdfsPath).limit(1000)

print(data.columns)
(training, test) = data.randomSplit([0.7, 0.3], seed = 100)


pipeline= PipelineModel.read().load("hdfs://namenode:9000/"+modelsPath+"/lr.model.pipeline.savepoint")

testData = pipeline.transform(test)
print("Test Dataset Count: " + str(testData.count()))

testData.show(5)


########################################################## 
################## Train/load the model ################## 
########################################################## 
lrModel = LogisticRegressionModel.load("hdfs://namenode:9000/"+modelsPath+"/lr.model.savepoint")

predictions = lrModel.transform(testData)

predictions.filter(predictions['prediction'] == 7)  \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)
