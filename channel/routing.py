#
# from channels.routing import route
# from channel.consumers import ws_connect, ws_disconnect
#
#
# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.disconnect', ws_disconnect),
# ]


from channels.routing import route
from .consumers import websocket_receive, ws_connect, ws_disconnect, ws_message

channel_routing = [
    route("websocket.receive", ws_message),
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]

