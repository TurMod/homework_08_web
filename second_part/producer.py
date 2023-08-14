import pika
import connect
import faker
import pickle

fake_data = faker.Faker()

from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

def main(n):

    for _ in range(n):
        contact = Contact(fullname=fake_data.name(), email=fake_data.email()).save()
        print(' || The contact has been created')
        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=pickle.dumps(contact),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(' || The contact has been sent')
    connection.close()

if __name__ == '__main__':
    main(10)