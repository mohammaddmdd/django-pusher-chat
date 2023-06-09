import json
import os

import pusher
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from werkzeug.security import generate_password_hash, check_password_hash
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework_jwt.utils import jwt_encode_handler
from textblob import TextBlob

from chat.models import Channel, Message


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        print(username)
        password = make_password(data.get("password"))
        print(password)

        try:
            new_user = User(username=username, password=password)
            new_user.save()
        except:
            return JsonResponse({
                "status": "error",
                "message": "Could not add user"
            }, status=400)

        return JsonResponse({
            "status": "success",
            "message": "User added successfully"
        }, status=201)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None or not check_password(password, user.password):
            return JsonResponse({
                "status": "failed",
                "message": "Failed getting user"
            }, status=401)

        # Generate a token
        payload = {
            "user_id": user.id,
            "username": user.username
        }
        token = jwt_encode_handler(payload)

        return JsonResponse({
            "status": "success",
            "message": "Login successful",
            "data": {
                "id": user.id,
                "token": token,
                "username": user.username
            }
        }, status=200)


pusher_client = pusher.Pusher(
    app_id=os.environ.get('PUSHER_APP_ID'),
    key=os.environ.get('PUSHER_KEY'),
    secret=os.environ.get('PUSHER_SECRET'),
    cluster=os.environ.get('PUSHER_CLUSTER'),
    ssl=True
)


@csrf_exempt
@login_required
def request_chat(request):
    request_data = request.POST  # Assuming the data is sent as form data

    from_user = request_data.get('from_user', '')
    to_user = request_data.get('to_user', '')

    to_user_channel = f"private-notification_user_{to_user}"
    from_user_channel = f"private-notification_user_{from_user}"

    # Check if there is a channel that already exists between these two users
    channel = Channel.objects.filter(from_user__in=[from_user, to_user], to_user__in=[from_user, to_user]).first()

    if not channel:
        # Generate a channel...
        chat_channel = f"private-chat_{from_user}_{to_user}"

        new_channel = Channel()
        new_channel.from_user = from_user
        new_channel.to_user = to_user
        new_channel.name = chat_channel
        new_channel.save()
    else:
        # Use the channel name stored in the database
        chat_channel = channel.name

    data = {
        "from_user": from_user,
        "to_user": to_user,
        "from_user_notification_channel": from_user_channel,
        "to_user_notification_channel": to_user_channel,
        "channel_name": chat_channel,
    }

    # Trigger an event to the other user
    pusher_client.trigger(to_user_channel, 'new_chat', data)

    return JsonResponse(data)


@csrf_exempt
@require_POST
@login_required
def pusher_authentication(request):
    channel_name = request.POST.get('channel_name')
    socket_id = request.POST.get('socket_id')

    auth = pusher_client.authenticate(
        channel=channel_name,
        socket_id=socket_id
    )

    return JsonResponse(auth)


@csrf_exempt
@require_POST
@login_required
def send_message(request):
    request_data = json.loads(request.body.decode('utf-8'))
    from_user = request_data.get('from_user', '')
    to_user = request_data.get('to_user', '')
    message = request_data.get('message', '')
    channel = request_data.get('channel')

    new_message = Message.objects.create(
        message=message,
        channel_id=channel,
        from_user=from_user,
        to_user=to_user
    )
    sentiment = getSentiment(message)
    message_data = {
        "from_user": from_user,
        "to_user": to_user,
        "message": message,
        "channel": channel,
        "sentiment": sentiment
    }

    pusher_client.trigger(channel, 'new_message', message_data)

    return JsonResponse(message_data)


@login_required
def users(request):
    users = User.objects.all()
    user_data = [{"id": user.id, "userName": user.username} for user in users]
    return JsonResponse(user_data, safe=False)


@login_required
def user_messages(request, channel_id):
    messages = Message.objects.filter(channel_id=channel_id)
    message_data = [
        {
            "id": message.id,
            "message": message.message,
            "to_user": message.to_user,
            "channel_id": message.channel_id,
            "from_user": message.from_user,
        }
        for message in messages
    ]
    return JsonResponse(message_data, safe=False)


def getSentiment(message):
    text = TextBlob(message)
    return {'polarity': text.polarity}


@login_required
def user_messages(request, channel_id):
    messages = Message.objects.filter(channel_id=channel_id)
    message_data = [
        {
            "id": message.id,
            "message": message.message,
            "to_user": message.to_user,
            "channel_id": message.channel_id,
            "from_user": message.from_user,
            "sentiment": getSentiment(message.message)
        }
        for message in messages
    ]
    return JsonResponse(message_data, safe=False)

@csrf_exempt
@login_required
def pusher_authentication(request):
    channel_name = request.POST.get('channel_name')
    socket_id = request.POST.get('socket_id')

    user_id = request.user.id
    username = request.user.username

    auth = pusher_client.authenticate(
        channel=channel_name,
        socket_id=socket_id,
        custom_data={
            'user_id': user_id,
            'user_info': {
                'username': username,
            }
        }
    )

    return JsonResponse(auth)