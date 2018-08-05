package spark.classification

import java.util.Calendar

import org.apache.spark.{SparkConf, SparkContext}

import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.streaming.{Seconds, StreamingContext}

import org.apache.kafka.clients.producer.ProducerConfig
import spark.mlstreaming._
import java.util.{Properties, UUID}
import org.apache.kafka.common.serialization.{ByteArraySerializer, StringSerializer}
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.spark.broadcast.Broadcast

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.mllib.classification.{LogisticRegressionModel, LogisticRegressionWithLBFGS}
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.util.MLUtils


import org.apache.commons.io.FileUtils
import org.apache.commons.io.filefilter.WildcardFileFilter
import java.io.File

object LogisticRegressionWithLBFGSExample {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("LogisticRegressionWithLBFGSExample")
    val sc = new SparkContext(conf)
    sc.setLogLevel("ERROR")


    // $example on$
    // Load training data in LIBSVM format.
    val data = MLUtils.loadLibSVMFile(sc, "/home/halil/gitlab/acm/scala/scala-logistic-regression/data.txt")

    // Split data into training (60%) and test (40%).
    val splits = data.randomSplit(Array(0.6, 0.4), seed = 11L)
     
    val training = splits(0).cache()
    val test = splits(1)

    // Run training algorithm to build the model
    val model = new LogisticRegressionWithLBFGS()
      .setNumClasses(10)
      .run(training)

    // Compute raw scores on the test set.
    val predictionAndLabels = test.map { case LabeledPoint(label, features) =>
      val prediction = model.predict(features)
      (prediction, label)
    }

    // Get evaluation metrics.
    val metrics = new MulticlassMetrics(predictionAndLabels)
    val accuracy = metrics.accuracy
    println(s"Accuracy = $accuracy")

    // Save and load model
    val modelPath="/home/halil/gitlab/acm/scala/scala-logistic-regression/model-build/scalaLogisticRegressionWithLBFGSModel"
    FileUtils.deleteDirectory(new File(modelPath))
    model.save(sc, modelPath)
    val sameModel = LogisticRegressionModel.load(sc, modelPath)

    sc.stop()
  }
}
// scalastyle:on println
