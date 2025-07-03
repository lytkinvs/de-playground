from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

topic = 'vl_lab02_in'
consumer = Consumer(conf)
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        print(f"Received message: {msg.value().decode('utf-8')} (key: {msg.key()})")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()