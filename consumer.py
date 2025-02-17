import json
import requests
import pika

from loguru import logger

API_URL = "http://localhost:8000/api/data/"

def process_message(ch, method, properties, body):
    message = json.loads(body)
    response = requests.get(
        url=f"{API_URL}{message['id']}/"
    )
    
    if response.status_code != 200:
        print(f"Ошибка запроса API для ID {message['id']}: {response.status_code}")
    else:
        data = response.json()
        print(f"Получены новые данные: {data}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.queue_declare(
    queue='data_updates', 
    durable=True
)
channel.basic_consume(
    queue='data_updates', 
    on_message_callback=process_message
)

logger.info("WAITING...")
channel.start_consuming()
