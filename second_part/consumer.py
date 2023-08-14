import pika
import connect
from models import Contact

import time
import sys
import pickle

def main():

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)


    def send_email_to_contact(contact):
        ...

    def callback(ch, method, properties, body):
        contact = pickle.loads(body)
        print('---------------')
        print(' || The contact was received')
        time.sleep(1)
        send_email_to_contact(contact)
        print(' || The email was sent successfully')
        contact.update(status=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted!')
        sys.exit(0)