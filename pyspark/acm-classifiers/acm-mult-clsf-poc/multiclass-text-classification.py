#!/usr/bin/env python

# see: https://stackoverflow.com/questions/50987944/key-not-found-pyspark-driver-callback-host
# see: data set: https://www.kaggle.com/c/sf-crime/data
# see: https://arrow.apache.org/docs/python/filesystems.html 
# see: https://pythonhosted.org/pywebhdfs/
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, CountVectorizerModel
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pywebhdfs.webhdfs import PyWebHdfsClient
import os

hdfs = PyWebHdfsClient(host='namenode',port='50070', user_name='root')

def hdfsPut(local_path, hdfs_path):
    with open(local_path) as file_data:
        hdfs.create_file(hdfs_path, file_data=file_data, overwrite=True)


def hdfsPutTrainDataToDir(filePath, dir_):
    fname= os.path.basename(filePath)
    hdfsPut(filePath, dir_+"/"+fname)

conf = SparkConf()
conf.setMaster("spark://acm-spark-master:7077")
conf.setAppName("batch-multiclass-text-classification")

sc =SparkContext()
sqlContext = SQLContext(sc)

trainDataFile="./data/sanfrancisco-crime/train.csv"
hdfsPath="/acm/ml/clsf/data/test001"
modelsPath=hdfsPath+"/models"
hdfs.make_dir(hdfsPath)
hdfs.make_dir(modelsPath)
hdfsPutTrainDataToDir(trainDataFile,hdfsPath)


data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load("hdfs://namenode:9000/"+hdfsPath).limit(1000)
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


pipelineFit.write().overwrite().save("hdfs://namenode:9000/"+modelsPath+ "/lr.model.pipeline.savepoint")
#trainingData.write.mode("overwrite").parquet("lr.model.data.savepoint")
lrModel.write().overwrite().save("hdfs://namenode:9000/"+modelsPath+"/lr.model.savepoint")
predictions = lrModel.transform(testData)

#predictions.filter(predictions['prediction'] == 0) \
#predictions\
predictions.filter(predictions['prediction'] == 7)  \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)
