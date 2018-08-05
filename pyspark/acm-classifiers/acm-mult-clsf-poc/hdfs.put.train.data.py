#!/usr/bin/env python
from pywebhdfs.webhdfs import PyWebHdfsClient
import os

hdfs = PyWebHdfsClient(host='namenode',port='50070', user_name='root')


def hdfsPut(local_path, hdfs_path):
    with open(local_path) as file_data:
        hdfs.create_file(hdfs_path, file_data=file_data, overwrite=True)


def hdfsPutTrainDataToDir(filePath, dir_):
    fname= os.path.basename(filePath)
    hdfsPath = dir_+"/"+fname
    hdfsPut(filePath, hdfsPath)


trainDataFile="./data/sanfrancisco-crime/train.csv"
hdfsPath="/acm/ml/clsf/data/test001"
hdfs.make_dir(hdfsPath)
hdfsPutTrainDataToDir(trainDataFile,hdfsPath)
