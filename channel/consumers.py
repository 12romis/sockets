import json

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from channel.models import LoggedInUser, Messages
from django.utils.formats import localize


@channel_session_user_from_http
def ws_connect(message):
    LoggedInUser.objects.get_or_create(user=message.user)
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })


@channel_session_user
def ws_disconnect(message):
    LoggedInUser.objects.filter(user=message.user).delete()
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)


def websocket_receive(message):
    text = message.content.get('body')
    if text:
        message.reply_channel.send({"text": "You said: {}".format(text)})


@channel_session_user
def ws_message(message):
    # Stick the message onto the processing queue
    msg = Messages.objects.create(user=message.user, body=message['text'])
    Group('users').add(message.reply_channel)
    Group("users").send({
        'text': json.dumps({
            'username': message.user.username,
            'message': True,
            'body': message['text'],
            'date': localize(msg.created_at)
        })
    })
