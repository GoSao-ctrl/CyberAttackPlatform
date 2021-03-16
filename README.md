# NetAttack
一个分布式用于进行网络攻击的平台

#### Kafka.py

用于创建分布式的消息处理系统，由主节点发送消息，攻击节点接受节点解析，发起攻击（暂时未实现，只做了一个demo用于生成数据消费数据）

#### NetScan.py

构建了一个类NetScanType用于存储可用扫描的类型

构建类NmapScan用于定义扫描所需参数，解析攻击指令，发起扫描

#### NetAttack.py

构建了一个类NetAttackType，用于存储攻击类型

构建类ScapyAttack，定义攻击需要的IP地址，端口信息，解析攻击指令，发起攻击

#### CentralManager.py

构造了一个AnalyzeCommand函数，可以用于解析指令，对两个方向不同的类进行调用

构造一个嗅探类，用于嗅探发送出的攻击包（暂未实现）