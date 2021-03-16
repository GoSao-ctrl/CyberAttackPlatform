#!/bin/bash
case $1 in
"start"){

	for i in 192.168.1.201 192.168.1.202 192.168.1.203
		do
			echo "***************$i***************"
			sshpass -p "allen" ssh -p 22 $i "/root/xia/zookeeper/zookeeper-3.4.12/bin/zkServer.sh start" 
		done

};;
"stop"){

	for i in 192.168.1.201 192.168.1.202 192.168.1.203
		do
			echo "***************$i***************"
			sshpass -p "allen" ssh -p 22 $i "/root/xia/zookeeper/zookeeper-3.4.12/bin/zkServer.sh stop"
		done

};;

esac
