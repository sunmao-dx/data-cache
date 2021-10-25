import pika
import os

RMQ_HOST = os.environ.get('RMQ_HOST', 'localhost')
RMQ_VHOST = os.environ.get('RMQ_VHOST', '/')
RMQ_USER = os.environ.get('RMQ_USER', 'event-platform')
RMQ_PASS = os.environ.get('RMQ_PASS', 'opensource_at_123')
QUEUE_NAME = os.environ.get('RMQ_QUEUE_NAME', 'gitee_data_processing')
EXCHANGE_NAME = 'delayed_exchange'

credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASS)

channel = None
def init():
    global channel
    conn = pika.BlockingConnection(pika.ConnectionParameters(RMQ_HOST, virtual_host=RMQ_VHOST, credentials=credentials))
    channel = conn.channel()

    channel.exchange_declare(EXCHANGE_NAME, 'x-delayed-message', arguments={'x-delayed-type':'direct'})
    channel.queue_declare(queue=QUEUE_NAME)

def push_event(event_body, delay=0):
    delay_props = pika.BasicProperties(headers={'x-delay': delay})
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=QUEUE_NAME, body=event_body, properties=delay_props)

