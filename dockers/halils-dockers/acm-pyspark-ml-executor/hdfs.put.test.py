#!/usr/bin/env python

# see: https://stackoverflow.com/questions/50987944/key-not-found-pyspark-driver-callback-host
# see: data set: https://www.kaggle.com/c/sf-crime/data
# see: https://arrow.apache.org/docs/python/filesystems.html

#curl -i -X PUT -T /etc/screenrc -L http://namenode:50070/webhdfs/v1/acm/testfile?op=CREATE\&overwrite=true\&user.name=jovyan
#curl -i -L  http://namenode:50070/webhdfs/v1/acm/testfile?op=OPEN\&user.name=jovyan


from pywebhdfs.webhdfs import PyWebHdfsClient

hdfs = PyWebHdfsClient(host='namenode',port='50070', user_name='jovyan')

hdfs_path="/acm/ml/clsf/data/test001"
trainDataFile="./data/sanfrancisco-crime/train.csv"
with open(trainDataFile) as file_data:
    hdfs.create_file(hdfs_path, file_data=file_data, overwrite=True)


