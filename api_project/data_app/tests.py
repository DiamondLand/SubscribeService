import pika
import json

from loguru import logger

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

message = {'id': 1}
channel.basic_publish(
    exchange='',
    routing_key='data_updates',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)

logger.success("Сообщение отправлено")
connection.close()
