# myapp/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'message': 'Notification received!'
        }))

    def user_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
