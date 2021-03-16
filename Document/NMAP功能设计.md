## NMAP功能设计

### 输入参数要求

**IP地址**

域名或者IP段或者IP加掩码

```
'scanme.nmap.org' or '198.116.0-255.1-127' or '216.163.128.20/20'
```

**端口**

多个分离的端口或者连续的端口

```
'22,53,110,143-4564'
```

**扫描类型**

```
'-sU -sX -sC -sV'
```

-sV 默认使用，版本检测，能够扫描运行软件的版本

-sS TCP的SYN扫描，不完成TCP连接，只发送第一次握手的包

-sT TCP的连接检测，需要建立TCP连接

-sN TCP不设标志位

-sW TCP窗口扫描

-sU 使用UDP进行端口扫描

-O 操作系统检测

**识别结果**

open : 应用程序正在接受来自该端口的访问
 closed : 可访问，但是没有程序在监听
 filtered : 包被阻止了，不知道是什么情况
 unfiltered : 端口可访问，但是不确定是否开放
 open|filtered : 特殊状态，不确定
 colsed:filterd : 特殊状态，不确定

### NMAP主要功能

#### 1、主机发现

（1）-sn 只进行主机发现，不进行端口扫描S

#### 2、端口扫描

（1）-sS 使用TCP SYN进行TCP端口扫描

（2）-sT 使用TCP connect进行TCP端口扫描

（3）-sU 使用UDP扫描检测UDP端口的开放情况

（4）-F 表示快速扫描，只选择TOP 100的端口

#### 3、版本侦测

```
-sV: 指定让Nmap进行版本侦测
--version-intensity <level>: 指定版本侦测强度（0-9），默认为7。数值越高，探测出的服务越准确，但是运行时间会比较长。
--version-light: 指定使用轻量侦测方式 (intensity 2)
--version-all: 尝试使用所有的probes进行侦测 (intensity 9)
--version-trace: 显示出详细的版本侦测过程信息。
```

#### 4、OS侦测

```
-O: 指定Nmap进行OS侦测。
--osscan-limit: 限制Nmap只对确定的主机的进行OS探测（至少需确知该主机分别有一个open和closed的端口）。
--osscan-guess: 大胆猜测对方的主机的系统类型。由此准确性会下降不少，但会尽可能多为用户提供潜在的操作系统。
```

### 扫描结果

**第一级**

nmap：扫描信息（可忽略，不作为有用信息反馈）

scan：扫描结果

​	**在scan下一级**

​	扫描主机的IP地址（例如192.168.1.203）

​		**IP地址下一级**

​		1）hostname：主机信息

​			name,type

​		2）status：状态信息

​			reason(扫描方式)，state(状态)

​		3）address：地址

​			ipv4,mac

​		4）vendor：供应商信息

​			mac地址：供应商

​		5）tcp：开放的TCP端口

​			端口号（例如22）

​				extrainfo：额外信息

​				cpe：未知

​				conf:未知

​				product : 未知

​				name:协议名称(例如ssh)

​				version：版本信息

​				state：状态

​				reason：扫描方式

​		6）udp：开放的UDP端口

​			下方内容跟tcp类似

​	以下为操作系统检测特有的属性

​		7）uptime：登录时间

​				seconds,lastboot

​		8）osmatch：操作系统匹配

​				name（主机类型）

​				accuracy（未知）

​				osclass（可能的操作系统类型）

​					vendor,cpe,type,osgen,accuracy,osfamily

​				line（未知）

​			9）portused：使用的端口

​					portid，proto，state

