#!/usr/bin/env python

import json
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql.types import StringType, IntegerType, DateType, StructType, StructField, DoubleType
################################################## 
################## Prepare data ################## 
################################################## 
jsonFile = 'jsontordd.test.json'
json_ = None
with open(jsonFile, 'r') as f:
    content = f.read()
    json_ = json.loads(content)
#data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(trainDataFile).limit(1000)


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
test = sqlContext.createDataFrame(json_, schema)

pipeline= PipelineModel.load("lr.model.pipeline.savepoint")

testData = pipeline.transform(test)
print("Test Dataset Count: " + str(testData.count()))


########################################################## 
################## Train/load the model ################## 
########################################################## 
lrModel = LogisticRegressionModel.load("lr.model.savepoint")

predictions = lrModel.transform(testData)

predictions.filter(predictions['prediction'] == 7)  \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)
