name := "spark-ml-streaming"

version := "0.1.0"

scalaVersion := "2.11.8"



ivyXML := <dependency org="org.eclipse.jetty.orbit" name="javax.servlet" rev="3.0.0.v201112011016">
<artifact name="javax.servlet" type="orbit" ext="jar"/>
</dependency>


libraryDependencies += "org.apache.hadoop" % "hadoop-client" % "3.1.0"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.3.1" 

libraryDependencies += "org.apache.spark" %% "spark-streaming" % "2.3.1" 

libraryDependencies += "org.apache.spark" % "spark-mllib_2.11" % "2.3.1"

libraryDependencies += "org.scalatest" % "scalatest_2.11" % "3.2.0-SNAP10" % "test"

libraryDependencies += "io.spray" %% "spray-json" % "1.3.4"

libraryDependencies += "org.jblas" % "jblas" % "1.2.3"

//our kafka server's version is 1.1.0
libraryDependencies += "org.apache.kafka" % "kafka_2.11" % "1.1.0"
libraryDependencies += "org.apache.kafka" % "kafka-clients" % "1.1.0"
libraryDependencies += "org.apache.kafka" % "kafka-streams" % "1.1.0"

resolvers += "spray" at "http://repo.spray.io/"

//resolvers ++= Seq( "Akka Repository" at "http://repo.akka.io/releases/")
