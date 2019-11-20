# manually assign the partition list for the consumer
from kafka import TopicPartition
from kafka import KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
consumer.assign([TopicPartition('foobar', 2)])
msg = next(consumer)