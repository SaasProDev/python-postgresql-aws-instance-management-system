

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import frontend.routing
import frontend.consumers


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            frontend.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
            "notifications":    frontend.consumers.NotificationConsumer,
             # "console": frontend.consumers.ConsoleConsumer,
        }),
})

