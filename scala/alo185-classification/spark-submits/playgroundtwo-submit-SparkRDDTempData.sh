
cd ../
mvn package
cd spark-submits

set -x
alias ss=/Users/halil/Yandex.Disk.localized/root/projects/vizyon-akıllı-çözüm-tübitak/0050-devenv/programs/spark230/bin/spark-submit
rootdir="/Users/halil/git/acm/scala/alo185-classification"
target=$rootdir"/target"
echo $target


clazz_=tr.com.vbt.acm.spark.playgroundtwo.SparkRDDTempData
host=spark://acm:7077
jarname=original-alo185-classification-0.0.1.jar
jar_=$target/$jarname
remotejar_=/home/halil/$jarname
corenum=1
memory=570Mw

#function callss
callss () {
scp $jar_ halil@acm:
ssh halil@acm <<'ENDSSH'
/home/halil/programs/spark230/bin/spark-submit --class tr.com.vbt.acm.spark.playgroundtwo.SparkRDDTempData --master spark://acm:7077 --executor-memory 1G /home/halil/original-alo185-classification-0.0.1.jar
ENDSSH
#/Users/halil/Yandex.Disk.localized/root/projects/vizyon-akıllı-çözüm-tübitak/0050-devenv/programs/spark230/bin/spark-submit --class $clazz_ --master $host --executor-memory $memory  $jar_
}





#call function callss
callss 
