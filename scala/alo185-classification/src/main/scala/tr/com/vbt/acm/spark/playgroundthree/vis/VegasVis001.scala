package tr.com.vbt.acm.spark.playgroundthree.vis

import vegas._
import vegas.data.External._
import javafx.scene.canvas.Canvas
import vegas.render.WindowRenderer







object VegasVis001  {
  
  def main(args:Array[String]): Unit = {
    val plot = Vegas("Country Pop").
      withData(
        Seq(
          Map("country" -> "USA", "population" -> 314),
          Map("country" -> "UK", "population" -> 64),
          Map("country" -> "DK", "population" -> 80)
        )
      ).
      encodeX("country", Nom).
      encodeY("population", Quant).
      mark(Bar)
      

      plot.show
      println("done!")
    
  }
}