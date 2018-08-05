#!/bin/bash


rm -f /tmp/*.pid

#service sshd start
/etc/init.d/ssh start



HN=`hostname`
IP=`ifconfig eth0 |grep "inet"|awk -F\   '{print $2}'`
ssh namenode "grep -q -F $HN /etc/hosts || ( echo $IP $HN >> /etc/hosts && service dnsmasq restart )"

NN=`grep namenode /etc/hosts | awk '{print $1}'`
grep namenode /etc/resolv.conf && echo nameserver $NN > /etc/resolv.conf



while true; do ssh namenode cat /etc/hosts | grep -v localhost | grep -v :: | grep -v namenode | grep -v `hostname` | while read line ; do grep "$line" /etc/hosts > /dev/null 2>&1 || (echo "$line" >> /etc/hosts); done ; sleep 60 ; done
