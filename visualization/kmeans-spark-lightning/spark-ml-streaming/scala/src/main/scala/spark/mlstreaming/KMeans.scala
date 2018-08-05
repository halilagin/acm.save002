package spark.mlstreaming

import java.util.Calendar

import org.apache.spark.{SparkConf, SparkContext}

import org.apache.spark.mllib.clustering.StreamingKMeans
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.streaming.{Seconds, StreamingContext}

//see: https://stackoverflow.com/questions/31590592/how-to-write-to-kafka-from-spark-streaming
import org.apache.kafka.clients.producer.ProducerConfig
import spark.mlstreaming._
import java.util.{Properties, UUID}
import org.apache.kafka.common.serialization.{ByteArraySerializer, StringSerializer}
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.spark.broadcast.Broadcast

/**
 * Demo of streaming k-means with Spark Streaming.
 * Reads data from one directory, and prints models and predictions to another.
 *
 * Run via Python executable in the top-level project directory
 *
 */

object KMeans {

  def main(args: Array[String]) {
    if (args.length != 7) {
      System.err.println(
        "Usage: KMeans " +
          "<inputDir> <outputDir> <batchDuration> <numClusters> <numDimensions> <halfLife> <batchUnit>")
      System.exit(1)
    }

    val (inputDir, outputDir, batchDuration, numClusters, numDimensions, halfLife, timeUnit) =
      (args(0), args(1), args(2).toLong, args(3).toInt, args(4).toInt, args(5).toFloat, args(6))

    val conf = new SparkConf().setMaster("spark://acm:7077").setAppName("KMeansDemo")

    val sc = new SparkContext(conf)
    sc.setLogLevel("ERROR")
    val ssc = new StreamingContext(sc, Seconds(10))

    //periodically check the dicretory for streaming context to ahve fault tolerance syreaming context
    ssc.checkpoint("checkpoint-directory")


    val kafkaProducer: Broadcast[SparkKafkaProducer[Array[Byte], String]] = {
      val kafkaProducerConfig = {
        val p = new Properties()
        p.setProperty("bootstrap.servers", "acm:9092")
        p.setProperty("key.serializer", classOf[ByteArraySerializer].getName)
        p.setProperty("value.serializer", classOf[StringSerializer].getName)
        p
      }
      ssc.sparkContext.broadcast(SparkKafkaProducer[Array[Byte], String](kafkaProducerConfig))
    }



    val trainingData = ssc.textFileStream(inputDir).map(Vectors.parse)

    val model = new StreamingKMeans()
      .setK(numClusters)
      .setHalfLife(halfLife, timeUnit)
      .setRandomCenters(numDimensions, 0.0)

    model.trainOn(trainingData)

    val predictions = model.predictOn(trainingData)

    predictions.foreachRDD { rdd =>
      val modelString = model.latestModel().clusterCenters
        .map(c => c.toString.slice(1, c.toString.length-1)).mkString("\n")
      val predictString = rdd.map(p => p.toString).collect().mkString("\n")
      val dateString = Calendar.getInstance().getTime.toString.replace(" ", "-").replace(":", "-")
      Utils.printToFile(outputDir, dateString + "-model", modelString)
      Utils.printToFile(outputDir, dateString + "-predictions", predictString)
      kafkaProducer.value.send("kmeans-output-topic", modelString+"-----"+predictString)
    }

    ssc.start()
    ssc.awaitTermination()
  }
}
