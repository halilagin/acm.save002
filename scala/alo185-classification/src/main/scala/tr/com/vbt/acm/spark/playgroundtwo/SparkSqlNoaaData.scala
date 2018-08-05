package tr.com.vbt.acm.spark.playgroundtwo

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.types.StructField
import org.apache.spark.sql.types.DateType
import org.apache.spark.sql.types.DoubleType
import org.apache.spark.sql.types.StringType
import org.apache.spark.sql.Row
import org.apache.spark.sql.functions._
import swiftvis2.plotting
import swiftvis2.plotting._
import swiftvis2.plotting.renderer._
import scalafx.application.JFXApp
import java.io.File
import scalafx.embed.swing.SwingFXUtils
import scalafx.scene.canvas.Canvas
import javax.imageio.ImageIO
import java.io.FileOutputStream

//see: http://www.nber.org/noaa/ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
//see: http://www.nber.org/noaa/ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/
// see: https://stackoverflow.com/questions/3614041/in-scala-how-to-read-a-simple-csv-file-having-a-header-in-its-first-line

//case class SparkRDDTempData(day:Int, doy:Int, month:Int, year:Int, precip:Double, snow:Double, tave:Double, tmax:Double, tmin:Double)

//case class TempData(day:Int)

object SparkSqlNoaaData  extends JFXApp {
  

   
//    val spark = SparkSession.builder().master("spark://acm:7077").appName("NOAA data").getOrCreate()
  val spark = SparkSession.builder().master("local[*]").appName("NOAA data").getOrCreate()
    import spark.implicits._

    spark.sparkContext.setLogLevel("WARN")
    
    val tschema = StructType(Array(
      StructField("sid", StringType),
      StructField("date", DateType),
      StructField("mtype", StringType),
      StructField("value", DoubleType)
    ))
    
    val sschema = StructType(Array(
      StructField("sid", StringType),
      StructField("lat", DoubleType),
      StructField("lon", DoubleType),
      StructField("name", StringType)
    ))
    
    //val stationRDD = spark.sparkContext.textFile("/Users/halil/Downloads/ghcnd-stations.txt").map{ line =>
    val stationRDD = spark.sparkContext.textFile("/home/halil/gitlab/acm/spark/data/ghcnd-stations.txt").map{ line =>
      val id = line.substring(0,11)
      val lat = line.substring(12,20).toDouble
      val lon = line.substring(21,30).toDouble
      val name = line.substring(41,71)
      Row(id,lat,lon,name)
    }
    
    val stations = spark.createDataFrame(stationRDD, sschema).cache()
    
    
    val data = spark.read.schema(tschema).option("dateFormat", "yyyyMMdd").csv("/home/halil/gitlab/acm/spark/data/noaa-2014.csv").cache()
    //val data = spark.read.schema(tschema).option("dateFormat", "yyyyMMdd").csv("/Users/halil/Downloads/noaa-2014.csv").cache()
    
    //data.show()
    data.schema.printTreeString()
    
    
    val tmax = data.filter($"mtype"==="TMAX").limit(1000).drop("mtype").withColumnRenamed("value", "tmax")
    val tmin = data.filter('mtype==="TMIN").limit(1000).drop("mtype").withColumnRenamed("value", "tmin")

    val joined = tmax.join(tmin, Seq("sid","date"))
    val ave = joined.select('sid,'date, ('tmax+'tmin)/20*1.8+32).withColumnRenamed("((((tmax + tmin) / 20) * 1.8) + 32)", "tave")

    val sidave = ave.groupBy('sid).agg(avg('tave))
    //sidave.show()
    
    val stationsAll = stations.join(sidave,"sid").limit(100)
    stationsAll.show()
    val stationsAllArray = stationsAll.collect()
    println("1")
    val lats = stationsAllArray.map(_.getDouble(1))
    println("2")
    val lons = stationsAllArray.map(_.getDouble(2))
    println("3")
    val temps = stationsAllArray.map(_.getDouble(4))

    val cg = ColorGradient(0.0->BlueARGB, 50.0->GreenARGB, 100.0->RedARGB)
    println("4")
    val plot = Plot.scatterPlot(lons, lats, "Global Temps","Longititude", "Latitude", 3, temps.map(cg))
   
    println("5")
    FXRenderer(plot,400,300)
    //val pngFile = new File("/Users/halil/Downloads/stations.plot.png")
    val fileName= "/tmp/stations.plot.png" 
    val pngFile = new File(fileName)
    FXRenderer.saveToImage(plot, 800, 600, pngFile )
    //println("6")
//    
//    
//    
//    
//    val canvas = new Canvas(800, 600)
//    val gc = canvas.graphicsContext2D
//    val renderer = new FXRenderer(gc)
//    plot.render(renderer, Bounds(0, 0, 800, 600))
//    val img = SwingFXUtils.fromFXImage(canvas.snapshot(null, null), null)
//    ImageIO.write(img, "PNG", new FileOutputStream(pngFile))
    

    
    
//    ave.show()
    //tmin.show()
    //stationsAll.show()
    spark.stop()
   
      
    //org.apache.spark.mllib.classification.StreamingLogisticRegressionWithSGD


    
}