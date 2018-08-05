package tr.com.vbt.acm.spark.playgroundthree.vis

import scalafx.Includes._
import scalafx.application.JFXApp
import scalafx.scene.Scene
import scalafx.scene.chart.ScatterChart
import scalafx.scene.chart.NumberAxis
import scalafx.scene.chart.XYChart
import scalafx.collections.ObservableBuffer
import tr.com.vbt.acm.spark.TempData



object RemotePlotTempsJFX2 extends JFXApp {
  
 //val source = scala.io.Source.fromFile("/Users/halil/git/BigDataAnalyticswithSpark/MN212142_9392.csv")
 val source = scala.io.Source.fromFile("/home/halil/gitlab/acm/spark/data/MN212142_9392.csv")
 
    val lines = source.getLines().drop(1)
    
    val data = lines.filterNot(_.contains(",.,")).map{ line => 
      val line_ = line.replace('.', '0').replace("'", "")
      var p = line_.split(",")
      
      
      TempData(p(0).toInt, p(1).toInt, p(2).toInt, p(4).toInt, TempData.toDoubleOrNeg( p(5) ), p(6).toDouble,p(7).toDouble,p(8).toDouble,p(9).toDouble)
      //TempData(p(0).toInt)
    }.toArray
    source.close()
  
    stage = new JFXApp.PrimaryStage{
      title = "Temp Plot"
      scene = new Scene(500,500) {
        val xAxis = NumberAxis()
        val yAxis = NumberAxis()
        val pData = XYChart.Series[Number,Number]("Temps",
            ObservableBuffer(data.map(td=>XYChart.Data[Number,Number](td.doy,td.tmax)):_* ))
        val plot = new ScatterChart(xAxis, yAxis, ObservableBuffer(pData))
        root = plot
      }
    }
    
    
  }
  