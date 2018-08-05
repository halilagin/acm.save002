#!/usr/bin/env python
import json
import csv
import pandas as pd

from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline


def produceJson():
    csvfile = 'jsontordd.test.csv'
    csv_file = pd.DataFrame(pd.read_csv(csvfile, sep = ",", header = 0, index_col = False))
    csv_file.to_json("jsontordd.test.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)


def jsonToRdd():

    jsonFile = 'jsontordd.test.json'
    json_ = None
    with open(jsonFile, 'r') as f:
        content = f.read()
        json_ = json.loads(content)
    #data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(trainDataFile).limit(1000)
    sc =SparkContext()
    sqlContext = SQLContext(sc)
    data = sqlContext.createDataFrame(json_)



#produceJson()

jsonToRdd()
