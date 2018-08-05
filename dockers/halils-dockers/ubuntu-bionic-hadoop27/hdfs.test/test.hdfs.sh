
hdfs dfs -mkdir -p /acm
hdfs dfs -chown -R jovyan:jovyan /acm
#curl -i -X PUT http://namenode:50070/webhdfs/v1/acmf?op=MKDIRS\&user.name=jovyan
#hdfs dfs -chown -R jovyan:jovyan /acm
curl -i  http://namenode:50070/webhdfs/v1/acm?op=LISTSTATUS\&user.name=jovyan
curl -i -X PUT -T /etc/screenrc -L http://namenode:50070/webhdfs/v1/acm/testfile?op=CREATE\&overwrite=true\&user.name=jovyan
curl -i -L  http://namenode:50070/webhdfs/v1/acm/testfile?op=OPEN\&user.name=jovyan
curl -i -X DELETE -L  http://namenode:50070/webhdfs/v1/acm/testfile?op=DELETE\&user.name=jovyan
curl -i  http://namenode:50070/webhdfs/v1/acm?op=LISTSTATUS\&user.name=jovyan
