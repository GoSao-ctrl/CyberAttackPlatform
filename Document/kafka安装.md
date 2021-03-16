### 在Linux环境下

1、安装jdk

（1）直接拷贝压缩包解压

（2）修改环境变量/etc/profile

```
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_131  
export JRE_HOME=${JAVA_HOME}/jre  
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib  
export  PATH=${JAVA_HOME}/bin:$PATH
```

（3）检查是否安装成功

```
java -version
```

2、安装kafka

（1）解压压缩包

（2）进入解压目录

（3）编写脚本开启kafka服务与zookeeper服务

```
#!/usr/bin/env bash
cd /home/xia/kafka/kafka_2.13-2.6.0
#后台运行zookeeper服务，并将运行信息写入文件zk.log
nohup bin/zookeeper-server-start.sh config/zookeeper.properties>>zk.log 2>&1 &
#后台运行kafka服务，并将运行信息写入文件kafka.log
nohup bin/kafka-server-start.sh config/server.properties>>kafka.log 2>&1 &
```

（4）关闭kafka服务

```
#!/usr/bin/env bash
cd /home/xia/kafka/kafka_2.13-2.6.0
./bin/kafka-server-stop.sh
rm kafka.log zk.log
```

（5）创建一个topic

```
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

（6）消费者与生产者的实现

```
#生产者
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
#消费者
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

### 在windows平台安装jdk

（1）下载jdk的exe版本

（2）运行安装

（3）修改环境变量

新增变量

```
JAVA_HOME=D:\JDK
```

Path变量

```
%JAVA_HOME%\bin
%JAVA_HOME%\jre\bin
```

（4）检查是否安装成功

```
java -version
```

2、在windows平台安装kafka

（1）解压文件

（2）修改config/server.properties

```
log.dirs=/tmp/kafka-logs->../../winlogs
```

### kafka的集群通信

1、kafka的集群是通过zookeeper来实现的

2、通过zookeeper实现3台主机的集群关系（每台主机都是通过如下步骤完成通信）

（1）下载zookeeper包并解压

（2）进入conf目录，并赋值zoo_sample.cfg文件拷贝为zoo.cfg（为配置文件）

```
cd conf
cp zoo_sample.cfg zoo.cfg
```

（3）修改zoo.cfg

```
dataDir=/root/xia/zookeeper/zookeeper-3.4.12/tmp #数据存储地址
#三个服务器0，1，2
#服务器ip地址：leader选举端口：通信端口
server.0=192.168.1.201:2888:3888 
server.1=192.168.1.202:2888:3888
server.2=192.168.1.203:2888:3888
```

（4）创建myid文件

在dataDir路径创建myid文件

myid中写入当前编号0，1，2

（5）配置环境变量

```
export ZK_HOME=/root/xia/zookeeper/zookeeper-3.4.12
export PATH=$PATH:$ZK_HOME/bin

source /etc/profile
```

（6）启动zookeeper

```
#启动
zkServer.sh start
#停止
zkServer.sh stop
#重启
zkServer.sh restart
#查看状态
zkServer.sh status
```

3、kafka的集群启动

（1）修改server.properties文件

```
broker.id=0
listeners=PLAINTEXT://192.168.1.203:9092
zookeeper.connect=192.168.1.201:2181,192.168.1.202:2181,192.168.1.203:2181
```

（2）直接运行，完成通信
