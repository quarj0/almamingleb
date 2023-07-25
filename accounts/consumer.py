
import json
from cryptography.fernet import Fernet
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        message_history = await self.get_message_history()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Retrieve and send message history
        message_history = await self.get_message_history()
        await self.send(text_data=json.dumps({"message_history": message_history}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        encrypted_message = text_data_json["message"]

        # Decrypt the message
        decrypted_message = await self.decrypt_message(encrypted_message)

        # Get the authenticated user
        user = self.scope["user"]

        # Save the message to the database
        await self.save_message(user, decrypted_message)

        # Send the decrypted message to the room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": decrypted_message}
        )

    async def chat_message(self, event):
        message = event["message"]

        # Encrypt the message
        encrypted_message = await self.encrypt_message(message)

        # Send the encrypted message to the WebSocket
        await self.send(text_data=json.dumps({"message": encrypted_message}))

    @database_sync_to_async
    def encrypt_message(self, message):
        # Get the user's Fernet key from the database or any secure storage
        fernet_key = self.scope["user"].fernet_key.encode()

        # Encrypt the message using the Fernet key
        fernet = Fernet(fernet_key)
        encrypted_message = fernet.encrypt(message.encode()).decode()

        return encrypted_message

    @database_sync_to_async
    def decrypt_message(self, encrypted_message):
        # Get the user's Fernet key from the database or any secure storage
        fernet_key = self.scope["user"].fernet_key.encode()

        # Decrypt the message using the Fernet key
        fernet = Fernet(fernet_key)
        decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()

        return decrypted_message

    @database_sync_to_async
    def save_message(self, user, message):
        # Save the message to the database
        Message.objects.create(sender=user, recipient=user, content=message)

@database_sync_to_async
def get_message_history(self):
    # Retrieve all message history from the database
    message_history = Message.objects.filter(recipient=self.scope["user"]).order_by("-timestamp")

    # Decrypt the messages
    decrypted_history = []
    fernet_key = self.scope["user"].fernet_key.encode()
    fernet = Fernet(fernet_key)
    for message in message_history:
        decrypted_message = fernet.decrypt(message.content.encode()).decode()
        decrypted_history.append(decrypted_message)

    return decrypted_history

