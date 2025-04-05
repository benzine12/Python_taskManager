import pika
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_notifications')
        
    def send_notification(self, user_id, task_id, notification_type, message):
        """Send notification to RabbitMQ queue"""
        notification = {
            'user_id': user_id,
            'task_id': task_id,
            'type': notification_type,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='task_notifications',
                body=json.dumps(notification)
            )
            logger.info(f"Notification sent: {notification}")
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            
    def close(self):
        """Close the connection"""
        self.connection.close()

# Create a global instance
notification_service = NotificationService() 