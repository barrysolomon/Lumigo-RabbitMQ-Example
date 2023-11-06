import pika
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQProducer:

    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='hello')
        self.targeted_messages = [
            "TARGET: Critical system alert!",
            "TARGET: New VIP user signup!",
            "TARGET: Large transaction detected!",
            "TARGET: Application error rate spiked!"
        ]

    def publish_message(self):
        while True:
            if random.randint(1, 10) == 1:  # 10% chance to send targeted message
                message = random.choice(self.targeted_messages) + f" Timestamp: {time.time()}"
            else:
                message = f"Hello RabbitMQ - {time.time()}"
            
            self.channel.basic_publish(exchange='', routing_key='hello', body=message)
            logger.info(f" [x] Sent '{message}'")
            time.sleep(5)

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    logger.info("Producer started")
    producer = RabbitMQProducer(host='rabbitmq-service')
    try:
        producer.publish_message()
    except KeyboardInterrupt:
        logger.info("Producer interrupted by user. Exiting...")
    finally:
        producer.close()
        logger.info("Producer exited")
