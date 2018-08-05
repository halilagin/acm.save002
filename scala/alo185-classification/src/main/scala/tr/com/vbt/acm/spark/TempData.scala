package tr.com.vbt.acm.spark


// see: https://stackoverflow.com/questions/3614041/in-scala-how-to-read-a-simple-csv-file-having-a-header-in-its-first-line

case class TempData(day:Int, doy:Int, month:Int, year:Int, precip:Double, snow:Double, tave:Double, tmax:Double, tmin:Double)

//case class TempData(day:Int)

object TempData {
  
  def toDoubleOrNeg(s:String) :Double = {
    try{
      s.toDouble
    }catch{
      case _:NumberFormatException => -1
    }
  }
  
  
      
}