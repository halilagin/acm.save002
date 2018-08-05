package com.zhuinden.sparkexperiment;


import org.apache.spark.SparkContext;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.DataType;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import scala.Tuple2;
import scala.collection.JavaConversions;
import scala.collection.Seq;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import static org.apache.spark.sql.functions.col;
import org.apache.spark.ml.classification.LogisticRegressionModel;
import org.apache.spark.ml.classification.LogisticRegression;
import org.apache.spark.sql.Dataset;

import org.apache.spark.ml.feature.VectorAssembler;
import org.apache.spark.ml.regression.LinearRegression;
import org.apache.spark.mllib.linalg.VectorUDT;
import org.apache.spark.sql.SparkSession;
//import org.apache.spark.sql.functions.udf;
import org.apache.spark.sql.types.StructType;
import scala.Tuple2;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.mllib.regression.LabeledPoint;
import org.apache.spark.mllib.util.MLUtils;
// see: https://elbauldelprogramador.com/en/how-to-convert-column-to-vectorudt-densevector-spark/

/**
 * Created by achat1 on 9/23/15.
 * Just an example to see if it works.
 */
@Component
public class AcmTextClassifier {
    @Autowired
    private SparkSession sparkSession;

    public String predict() {
            String modelPath = "/home/halil/gitlab/acm/pyspark/multiclass-classification/lr.model.savepoint";
           LogisticRegressionModel lrModel = LogisticRegressionModel.load(modelPath);


            Dataset<Row> test = sparkSession.read().json("/tmp/lr.model.testdata.txt");
            test.show();



            
            

            StructType schema = new StructType().add("features", new VectorUDT());
            VectorAssembler assembler = new VectorAssembler().setInputCols(new String[]{"features"}).setOutputCol("label");
            Dataset<Row> out = assembler.transform(test);

            Dataset<Row> predictions = lrModel.transform(out);


/*
            JavaRDD<Row> items = predictions.toJavaRDD();
 
            items.foreach(item -> {
                System.out.println(item); 
            });
            */
            
            /*
            List<String> names = predictions.javaRDD().map(new org.apache.spark.api.java.function.Function<Row, Object>() {
              public String call(Row row) {
                return "Name: " + row.getString(0);
              }
            }).collect();
            */

            return "halil";

    }
}
