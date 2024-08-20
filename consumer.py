import threading
import time
import pika
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='RabbitMQ Consumer')
parser.add_argument('--queue', type=str, required=True, help='Queue name to consume from')
parser.add_argument('--consumers', type=int, default=1, help='Concurrent consumers, default 1')
parser.add_argument('--port', type=int, default=5672, help='RabbitMQ port, default 5682')
parser.add_argument('--qos', type=int, default=1, help='Prefetch/Qos count, default 1')
parser.add_argument('--host', type=str, default='localhost', help='RabbitMQ host, default localhost')
parser.add_argument('--delay', type=int, default=0, help='Process dekay in seconds, default 0')
args = parser.parse_args()

# Callback function to process messages
def on_message(ch, method, properties, body):
    print(f"Consumer '{method.consumer_tag}': Received {body}")
    # Simulate message processing time
    time.sleep(args.delay) 
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Manual acknowledgment


# Establish connection
credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters(args.host, port=args.port, credentials=credentials)


print(' [*] Waiting for messages. To exit press CTRL+C')

def start_consumer(consumer_number):
    consumer_tag = f"consumer-{consumer_number}"
    def on_connection_open_with_tag(connection):
        # Capture the consumer_tag in the closure
        def on_channel_open_with_tag(channel):
            channel.basic_qos(prefetch_count=args.qos) 
            channel.basic_consume(queue=args.queue, on_message_callback=on_message, consumer_tag=consumer_tag, auto_ack=False)

        connection.channel(on_open_callback=on_channel_open_with_tag)

    connection = pika.SelectConnection(parameters, on_open_callback=on_connection_open_with_tag)

    # Start the IOLoop in a separate thread for each consumer
    t = threading.Thread(target=connection.ioloop.start)
    t.start()


# Start multiple consumers
for i in range(args.consumers):
    start_consumer(i +1)