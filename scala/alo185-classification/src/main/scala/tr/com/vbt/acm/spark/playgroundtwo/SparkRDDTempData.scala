package tr.com.vbt.acm.spark.playgroundtwo

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import tr.com.vbt.acm.spark.TempData



// see: https://stackoverflow.com/questions/3614041/in-scala-how-to-read-a-simple-csv-file-having-a-header-in-its-first-line

case class SparkRDDTempData(day:Int, doy:Int, month:Int, year:Int, precip:Double, snow:Double, tave:Double, tmax:Double, tmin:Double)

//case class TempData(day:Int)

object SparkRDDTempData {
  
  def toDoubleOrNeg(s:String) :Double = {
    try{
      s.toDouble
    }catch{
      case _:NumberFormatException => -1
    }
  }
  
  def main(args:Array[String]): Unit = {
    
    val conf = new SparkConf().setAppName("Temp Data").setMaster("spark://acm:7077")
    val sc = new SparkContext(conf)
    sc.setLogLevel("WARN")
    
    //val source = scala.io.Source.fromFile("/Users/halil/git/BigDataAnalyticswithSpark/MN212142_9392.csv")
    //val lines = sc.textFile("/home/halil/gitlab/acm/spark/data/MN212142_9392.csv")
    val lines = sc.textFile("/home/halil/gitlab/acm/spark/data/MN212142_9392.csv").filter(!_.contains("Day"))
    lines.take(5) foreach println
    println("we have done it 3!")
    
    val data = lines.flatMap{ line =>
      if (line.contains(",.,")) Seq.empty
      else {
        val line_ = line.replace('.', '0').replace("'", "")
        var p = line_.split(",")
        
        Seq(SparkRDDTempData(p(0).toInt,p(1).toInt,p(2).toInt,p(3).toInt, TempData.toDoubleOrNeg(p(4)), TempData.toDoubleOrNeg(p(5)), TempData.toDoubleOrNeg(p(6)), TempData.toDoubleOrNeg(p(7)), TempData.toDoubleOrNeg(p(8)) ))

        //TempData(p(0).toInt, p(1).toInt, p(2).toInt, p(4).toInt, toDoubleOrNeg( p(5) ), p(6).toDouble,p(7).toDouble,p(8).toDouble,p(9).toDouble)
        //TempData(p(0).toInt)
      }
    }.cache()
    
    data.take(5) foreach println
    println(data.count())
    
    println(data.max()(Ordering.by(_.tmax)))
    
    val max_ = data.reduce((d1,d2) => if (d1.tmax>d2.tmax) d1 else d2)
    println(max_)
    
    
    data.filter(_.precip>=1.0)
    
//    
//    
//    val maxTemp = data.map(_.tmax).max
//    val hotDays = data.filter(_.tmax==maxTemp)
//    println(maxTemp)
//    
    
//    val hotDay = data.maxBy(_.tmax)
//    println(s"hot day 1 ${hotDay}")
//    
//    val hotDay2 = data.reduceLeft((d1,d2) => if (d1.tmax>=d2.tmax) d1 else d2)
//    println(s"hot day 2 ${hotDay2}")
//    
//    
//    val rainyCount = data.count(_.precip>=1.0)
//    println(s"There are $rainyCount rainy days. The percentage is ${100.0*rainyCount/data.length}")
//    
//    
//    
//    val (rainySum, rainyCount2) = data.foldLeft((0.0 -> 0)) {
//      case ((sum, cnt),td) => if (td.precip>=1.0) (sum+td.tmax,cnt+1) else (sum,cnt)
//    }
//    
//    println(s"average temp in rainy temps ${1.0*rainySum/rainyCount2}")
//    
//    val rainyTemps = data.flatMap(td=> if (td.precip>=1.0) Seq(td.tmax) else Seq.empty)
//    println(s"average temp in rainy temps ${1.0*rainyTemps.sum/rainyTemps.length}")
    
  }
      
}