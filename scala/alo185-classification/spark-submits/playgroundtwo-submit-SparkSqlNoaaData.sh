

set -x
alias ss=/Users/halil/Yandex.Disk.localized/root/projects/vizyon-akıllı-çözüm-tübitak/0050-devenv/programs/spark230/bin/spark-submit
rootdir="/Users/halil/git/acm/scala/alo185-classification"
target=$rootdir"/target"
echo $target


clazz_=tr.com.vbt.acm.spark.playgroundtwo.SparkSqlNoaaData
host=spark://acm:7077
jarname=original-alo185-classification-0.0.1.jar
jar_=$target/$jarname
remotejar_=/home/halil/$jarname
corenum=1
memory=570M







compile() { 
	cd ../
	mvn package
	cd spark-submits
}	
	

run() { 
scp $jar_ halil@acm:
# we have a virtual x server: sudo Xvfb :1 -s "-screen 0 1024x768x16" </dev/null &
# we need :1 x server for jfx java application
# -Y option is for X client of macos sierra, linux needs -X option
ssh  halil@acm <<'ENDSSH'
export DISPLAY=:1
/home/halil/programs/spark230/bin/spark-submit --class tr.com.vbt.acm.spark.playgroundtwo.SparkSqlNoaaData --master spark://acm:7077 --executor-memory 1G /home/halil/original-alo185-classification-0.0.1.jar
ENDSSH

}

#function callss
callss () {
if [ $1 == "compile" ] || [ $1 == "install" ]; then
compile
fi

if [ $1 == "install" ] || [ $1 == "run" ]; then
run
fi

}





#call function callss
callss $1

