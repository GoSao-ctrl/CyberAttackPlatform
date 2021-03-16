# from kafka import KafkaConsumer
# from kafka import KafkaProducer
import time


def consumer1(topicname, type):
    consumer = []
    if (type == "history"):
        consumer = KafkaConsumer(topicname, auto_offset_reset="earliest", bootstrap_servers=['localhost:9092'],
                                 consumer_timeout_ms=1000)
    elif (type == "realtime"):
        consumer = KafkaConsumer(topicname, bootstrap_servers=['localhost:9092'])

    for msg in consumer:
        print(str(msg.value, encoding="utf-8"))


def consumer2(topic):
    consumer = KafkaConsumer(topicname, bootstrap_servers=['localhost:9092'])
    index = 0
    while True:
        msg = consumer.poll(timeout_ms=10, max_records=1)
        for key in msg:
            print(str(msg[key][0].value, encoding="utf-8"))
        time.sleep(2)
        index += 1
        print("poll index = %s" % index)


def producer1(topicname):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    future = producer.send(topicname, key=b'my_key', value=b'my_value', partition=0)
    result = future.get(timeout=10)
    print(result)


if __name__ == "__main__":
    topicname = "test"
    type = "history"
    producer1(topicname)
    consumer2(topicname)
