package spark.classification

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.mllib.classification.SVMModel
import org.apache.spark.mllib.evaluation.BinaryClassificationMetrics
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.optimization.HingeGradient
import org.apache.spark.mllib.optimization.LBFGS
import org.apache.spark.mllib.optimization.SimpleUpdater
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.sql.{DataFrame, Row, SparkSession}



//see: https://stackoverflow.com/questions/43920111/convert-dataframe-to-libsvm-format
//see: https://github.com/mcapuccini/spark-tutorial
//see: https://github.com/mcapuccini/TheSparkBox
object FarmbioSVMWithLBFGS {

  def main(args: Array[String]) = {
    /*
    val spark = SparkSession
      .builder
      .appName(s"DataFrameExample")
      .getOrCreate()

    //Start the Spark context


    val df: DataFrame = spark.read.format("libsvm").load("pubchem.svm").cache()
    println (df.count)
    println ("halil")
    */
    val x=11

    if (x>10) {
    val conf = new SparkConf()
      .setAppName("SVM")
      .setMaster("local[*]")
    val sc = new SparkContext(conf)

    //Load examples
    val data = MLUtils.loadLibSVMFile(sc, "pubchem.svm")
    val numFeatures = data.take(1)(0).features.size //Compute number of features for LBFGS

    //Split the data
    val splits = data.randomSplit(Array(0.8, 0.2), seed = 11L)
    val training = splits(0)
      .map(x => (x.label, MLUtils.appendBias(x.features))) //adapt to LBFGS API (see Spark docs for further details)
      .cache() 
    val test = splits(1)

    /*
     * Train the model using linear SVM. LBFGS 
     * (http://spark.apache.org/docs/latest/mllib-optimization.html#l-bfgs) is used
     * as underlying optimization algorithm here. LBFGS is a relatively new feature
     * in Spark, and it can be accessed only through low level functions.
     */
    
    //Solve the optimization problem using LBFGS. 
    //Some knowledge in Optimization is needed to actually understand this, but you can just use it as it :-)
    val (weightsWithIntercept, _) = LBFGS.runLBFGS(
      training,
      new HingeGradient(), //The Hinge objective function is what we aim to optimize in SVM
      new SimpleUpdater(), //No regularization
      //Use default paramenters for LBFGS
      numCorrections=10,
      convergenceTol=1e-4,
      maxNumIterations=100,
      regParam=0, //No regularization
      initialWeights=Vectors.dense(new Array[Double](numFeatures + 1))) //Use (0,0 ...) vector as first guess

    //Create a SVM model using the weights computed in the previous step  
    val model = new SVMModel(
      Vectors.dense(weightsWithIntercept.toArray.slice(0, weightsWithIntercept.size - 1)),
      weightsWithIntercept(weightsWithIntercept.size - 1))

    //Clear the threshold
    model.clearThreshold()

    //Compute the distance from the separating hyperplane for each of the test examples
    val distAndLabels = test.map { testExample =>
      val distance = model.predict(testExample.features)
      (distance, testExample.label)
    }

    //Compute the area under the ROC curve using the Spark's BinaryClassificationMetrics class
    val metrics = new BinaryClassificationMetrics(distAndLabels)
    val auROC = metrics.areaUnderROC()

    println("Area under ROC = " + auROC) //print the area under the ROC

    //Stop the Spark context
    sc.stop
    }

  }

}
