import pika
import argparse
import time

# Parse command-line arguments
parser = argparse.ArgumentParser(description='RabbitMQ Producer')
parser.add_argument('--queue', type=str, required=True, help='Queue name to publish to')
parser.add_argument('--txt', type=str, default="Message", help='Text message to publish')
parser.add_argument('--msg', type=int, default=1, help='Number of messages to send')
parser.add_argument('--sleep', type=float, default=1.0, help='Sleep interval between messages (in seconds)')
parser.add_argument('--port', type=int, default=5682, help='RabbitMQ port, default 5682')
parser.add_argument('--host', type=str, default='localhost', help='RabbitMQ host, default localhost')
parser.add_argument('--finite', action=argparse.BooleanOptionalAction, default=False, help='infinite loop, default False.')
args = parser.parse_args()

# Establish connection
credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(args.host, port=args.port, credentials=credentials)
)
channel = connection.channel()

# Declare queue
queue_name = args.queue
#channel.queue_declare(queue=queue_name)

finite = args.finite
txt = args.txt

print(finite)
while True:
    # Send messages in a loop with sleep
    print("#" * 20)
    for i in range(args.msg):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        message = f"{txt}: {i + 1} sent at {current_time}"  # Include timestamp in message
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f" [x] Sent '{message}' to queue '{queue_name}'")
        # time.sleep(args.sleep)  # Sleep for the specified interval

    time.sleep(args.sleep)
    if finite:
        break



connection.close()
