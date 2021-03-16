#!/bin/bash
case $1 in
"start"){

	for i in 192.168.1.201 192.168.1.202 192.168.1.203
		do
			echo "***************$i***************"
			sshpass -p "allen" ssh -p 22 $i "/root/xia/kafka/kafka_2.13-2.6.0/bin/kafka-server-start.sh -daemon /root/xia/kafka/kafka_2.13-2.6.0/config/server.properties"
		done

};;
"stop"){

	for i in 192.168.1.201 192.168.1.202 192.168.1.203
		do
			echo "***************$i***************"
			sshpass -p "allen" ssh -p 22 $i "/root/xia/kafka/kafka_2.13-2.6.0/bin/kafka-server-stop.sh"
		done

};;

esac
