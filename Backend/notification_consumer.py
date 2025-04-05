import pika
import json
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_notifications')
        
    def callback(self, ch, method, properties, body):
        """Process received notification"""
        try:
            notification = json.loads(body)
            logger.info(f"Received notification: {notification}")
            
            # Here you can implement different notification types
            # For example: email, push notification, etc.
            self.process_notification(notification)
            
        except Exception as e:
            logger.error(f"Error processing notification: {str(e)}")
            
    def process_notification(self, notification):
        """Process different types of notifications"""
        notification_type = notification['type']
        message = notification['message']
        
        if notification_type == 'task_created':
            logger.info(f"New task created: {message}")
            # Implement email notification
            # Implement push notification
            # etc.
            
        elif notification_type == 'task_completed':
            logger.info(f"Task completed: {message}")
            # Implement completion notification
            
        elif notification_type == 'task_updated':
            logger.info(f"Task updated: {message}")
            # Implement update notification
            
    def start_consuming(self):
        """Start consuming notifications"""
        self.channel.basic_consume(
            queue='task_notifications',
            on_message_callback=self.callback,
            auto_ack=True
        )
        
        logger.info('Started consuming notifications')
        self.channel.start_consuming()
        
    def close(self):
        """Close the connection"""
        self.connection.close()

if __name__ == '__main__':
    consumer = NotificationConsumer()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        consumer.close() 