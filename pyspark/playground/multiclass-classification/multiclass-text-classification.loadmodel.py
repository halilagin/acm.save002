#!/usr/bin/env python


# we need to save countvectorizer model, the link below shows an example.
# see: https://stackoverflow.com/questions/48924308/countvectorizer-using-same-vocabulary-in-a-second-time

import json
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, CountVectorizerModel
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline

sc =SparkContext()
sqlContext = SQLContext(sc)




################################################## 
################## Prepare data ################## 
################################################## 
trainDataFile="./data/sanfrancisco-crime/train.csv"
data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(trainDataFile).limit(1000)
print(data.columns)

drop_list = ['Dates', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y']

data = data.select([column for column in data.columns if column not in drop_list])
data.show(5)
data.printSchema()

################################################## 
################## Transofrmers ################## 
################################################## 

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



### Randomly split data into training and test sets. set seed for reproducibility
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)
print("Training Dataset Count: " + str(trainingData.count()))
print("Test Dataset Count: " + str(testData.count()))

testData.show(5)

results = testData.toJSON().map(lambda j: json.loads(j)).collect()
#print (results)
file = open('/tmp/lr.model.testdata.txt', 'w')
file.write(json.dumps(results))
file.close()

########################################################## 
################## Train/load the model ################## 
########################################################## 
lrModel = LogisticRegressionModel.load("lr.model.savepoint")

predictions = lrModel.transform(testData)

predictions.filter(predictions['prediction'] == 7)  \
    .select("Descript","Category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)
