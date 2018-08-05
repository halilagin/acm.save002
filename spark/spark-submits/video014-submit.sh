
set -x
rootdir="/Users/halil/git/acm/scala/alo185-classification"
target=$rootdir"/target"
echo $target


clazz_=tr.com.vbt.acm.spark.playground.video014.RDDTempData
host=spark://acm:7077
jar_=$HOME/original-alo185-classification-0.0.1.jar
corenum=2

#function callss
callss () {
#spark-submit --class $clazz_ --master $host --executor-memory 470M --total-executor-cores $corenum $jar_
spark-submit --class $clazz_ --master $host --executor-memory 1G  --executor-cores 1 --driver-memory 1G $jar_
}





#call function callss
callss 
