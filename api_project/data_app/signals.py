import json
import pika

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DataRecord


def send_to_rabbitmq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='data_updates')

    channel.basic_publish(exchange='', routing_key='data_updates', body=json.dumps(message))
    connection.close()


@receiver(post_save, sender=DataRecord)
def data_record_saved(sender, instance, **kwargs):
    message = {
        'id': instance.id,
        'name': instance.name,
        'value': instance.value,
        'updated_at': instance.updated_at.isoformat(),
    }
    send_to_rabbitmq(message)
