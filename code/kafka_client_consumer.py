
from kafka import KafkaConsumer

consumer =  KafkaConsumer('customer_log', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
for msg in consumer:
    print (msg)
