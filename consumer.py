import pika
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='RabbitMQ Consumer')
parser.add_argument('--queue', type=str, required=True, help='Queue name to consume from')
parser.add_argument('--port', type=int, default=5672, help='RabbitMQ port, default 5682')
parser.add_argument('--host', type=str, default='localhost', help='RabbitMQ host, default localhost')
args = parser.parse_args()

# Establish connection
credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(args.host, port=args.port, credentials=credentials))  # Connect to local RabbitMQ server
channel = connection.channel()

# Declare queue (if it doesn't exist yet)
queue_name = args.queue  # Replace with your queue name


#channel.queue_declare(queue=queue_name)

# Define callback function to process messages
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # Simulate message processing time
    # time.sleep(5)  # Uncomment if you want to simulate a longer processing time
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Manual acknowledgment


# QoS
channel.basic_qos(prefetch_count=1)

# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
