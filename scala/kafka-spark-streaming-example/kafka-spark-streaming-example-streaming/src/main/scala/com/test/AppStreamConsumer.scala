package com.test

import java.util.Properties
import java.util.Arrays

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.{SparkConf, SparkContext}
import java.util

import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import com.test.config.ConfigurationFactory

/**
  * The most basic streaming example: starts a Kafka server, creates a topic, creates a stream
  * to process that topic, and publishes some data using the SparkKafkaSink.
  *
  * Notice there's quite a lot of waiting. It takes some time for streaming to get going,
  * and data published too early tends to be missed by the stream. (No doubt, this is partly
  * because this example uses the simplest method to create the stream, and thus doesn't
  * get an opportunity to set auto.offset.reset to "earliest".
  *
  * Also, data that is published takes some time to propagate to the stream.
  * This seems inevitable, and is almost guaranteed to be slower
  * in a self-contained example like this.
  */
object AppStreamConsumer {
  private[this] val config = ConfigurationFactory.load()

  
  
  def main (args: Array[String]) {

    val topic = "dashboard"




    val conf = new SparkConf().setAppName("AppStreamConsumer").setMaster("spark://acm:7077")
    val sc = new SparkContext(conf)

    // streams will produce data every second
    val ssc = new StreamingContext(sc, Seconds(1))

    // this many messages
    val max = 1000

    val servers = config.getProducer.getHosts.toArray.mkString(",")
    val topics = Array(config.getProducer.getTopic)

    // Create the stream.
 val params = Map[String, Object](
      "bootstrap.servers" -> servers,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "auto.offset.reset" -> "latest",
      "group.id" -> "dashboard",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    
    val kafkaStream =
      KafkaUtils.createDirectStream(
        ssc,
        LocationStrategies.PreferConsistent,
        Subscribe[String, String](
          topics,
          params
        )

      )

    // now, whenever this Kafka stream produces data the resulting RDD will be printed
    kafkaStream.foreachRDD(r => {
      println("*** got an RDD, size = " + r.count())
      r.foreach(s => println(s))
      if (r.count() > 0) {
        // let's see how many partitions the resulting RDD has -- notice that it has nothing
        // to do with the number of partitions in the RDD used to publish the data (4), nor
        // the number of partitions of the topic (which also happens to be four.)
        println("*** " + r.getNumPartitions + " partitions")
        r.glom().foreach(a => println("*** partition size = " + a.size))
      }
    })

    ssc.start()

    println("*** started termination monitor")

    // streams seem to need some time to get going
    Thread.sleep(5000)

    

    try {
      ssc.awaitTermination()
      println("*** streaming terminated")
    } catch {
      case e: Exception => {
        println("*** streaming exception caught in monitor thread")
      }
    }

    // stop Spark
    sc.stop()


    println("*** done")
  }
}