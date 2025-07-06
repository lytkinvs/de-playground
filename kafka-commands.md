### 

Start a Kafka broker:

`docker run -d --name broker apache/kafka:latest`

Open a shell in the broker container:

```bash
docker exec --workdir /opt/kafka/bin/ -it broker sh
```

Topic is a logical grouping of events in Kafka. From inside the container, create a topic called `test-topic`:

```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic
```

```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic 'test-topic’
```

Write two string events into the `test-topic' topic using the console producer that ships with Kafka:

```bash
./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
```

This command will wait for input at a `>` prompt. Enter `hello`, press `Enter`, then `world`, and press `Enter` again. Enter `Ctrl+C` to exit the console producer.

Now read the events in the `test-topic` topic from the beginning of the log:

```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic customer_log --from-beginning
```

You will see the two strings that you previously produced:

`hello
world`

The consumer will continue to run until you exit out of it by entering `Ctrl+C`.

When you are finished, stop and remove the container by running the following command on your host machine:

`docker rm -f broker`