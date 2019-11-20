from kafka import KafkaProducer
import random
import time
producer = KafkaProducer(bootstrap_servers='localhost:9092')
for _ in range(1000000):
    print(_)
    producer.send('foobar', b'some_message_bytes2 %d' % _)
    time.sleep(0.01)
