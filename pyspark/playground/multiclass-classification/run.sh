export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:$PYTHONPATH

#./bin/streaming-kmeans -p /tmp/mlstreaming-tmp -l http://localhost:3010
#./multiclass-text-classification.py

python $1 
