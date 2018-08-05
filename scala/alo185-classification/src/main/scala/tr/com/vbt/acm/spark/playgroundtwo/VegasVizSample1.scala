package tr.com.vbt.acm.spark.playgroundtwo

import vegas._
import vegas.data.External._
import vegas.render.WindowRenderer._

object VV {
  def main(args: Array[String]): Unit = {
//    val plot = Vegas("Country Pop").
//      withData(
//        Seq(
//          Map("country" -> "USA", "population" -> 314),
//          Map("country" -> "UK", "population" -> 64),
//          Map("country" -> "DK", "population" -> 80))).
//        encodeX("country", Nom).
//        encodeY("population", Quant).
//        mark(Bar)
//
//    plot.show

    
    
    Vegas("A scatterplot showing horsepower and miles per gallons with binned acceleration on color.").
  withURL(Cars).
  mark(Point).
  encodeX("Horsepower", Quantitative).
  encodeY("Miles_per_Gallon", Quantitative).
  encodeColor(field="Acceleration", dataType=Quantitative, bin=Bin(maxbins=5.0)).
  show
  }
}
