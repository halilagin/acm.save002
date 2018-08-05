
alias ss=/Users/halil/Yandex.Disk.localized/root/projects/vizyon-akıllı-çözüm-tübitak/0050-devenv/programs/spark230/bin/spark-submit
rootdir="/Users/halil/git/acm/scala/alo185-classification"
target=$rootdir"/target"
echo $target


clazz_=tr.com.vbt.acm.spark.playground.video014.RDDTempData
host=spark://acm:7077
jar_=$target/original-alo185-classification-0.0.1.jar
corenum=2

#function callss
callss () {
ss --class $claclazz_ss_ --master $host --executor-memory 1G --total-executor-cores $corenum_ $jar_
}





#call function callss
callss 
