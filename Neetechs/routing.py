from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from chat.consumers import ChatConsumer

#defult url websocket
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/<str:authkey>/', ChatConsumer.as_asgi())
        #path('ws/chat/', ChatConsumer.as_asgi())
    ])

})