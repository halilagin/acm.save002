
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object Video014TempData {
  
  
  def main(args:Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Temp Data").setMaster("local[*]")
    val sc = new SparkContext(conf)
    
    val lines = sc.textFile("/home/halil/gitlab/acm/spark/data/MN212142_9392.csv")
    lines.take(5) foreach println   
  }
      
}
