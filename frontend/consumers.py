from channels.generic.websocket import JsonWebsocketConsumer
from  paramiko import SSHClient, AutoAddPolicy
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import logging
from pprint import pprint

from django.template.loader import render_to_string

from subprocess import Popen, PIPE

_logger = logging.getLogger(__name__)


class NotificationConsumer(WebsocketConsumer):
    """ Performs Web Socket connection and Channel communication """

    HTML_TEMPLATE_FOR_INJECT = 'frontend/includes/helpers/websocket-notification.tpl.html'
    GROUP = 'notifications'

    def connect(self):
        """WebSocket connection establish """
        self.broadcast = self.GROUP

        async_to_sync(self.channel_layer.group_add)(
            self.broadcast,
            self.channel_name
        )

        self.accept()
        _logger.debug("Websocket Connected. Channel: '{}' Group: '{}'".format(
            self.channel_name, self.broadcast))

    def disconnect(self, close_code):
        """WebSocket disconnect"""
        pass

    def receive(self, text_data=None, bytes_data=None):
        """ Receive message FROM WEBSOCKET and sends it TO THE CHANNEL """
        if text_data(text_data):
            data = json.loads(text_data)
            data = self.inject_html_code(data)
            self.send_to_channel(data)

    def send_to_channel(self, data):
        """ Sends message to the channel """
        async_to_sync(self.channel_layer.group_send)(self.broadcast, data)

    def notification(self, event):
        """
        Receive message FROM THE CHANNEL and sent it TO WEBSOCKET
        For invoking this method:
         - the name of this method (i.e. 'notification') should br used as a 'type' of message
         - self.broadcast (i.e. 'notifications') should br used as a 'group' of message

        so, this method receives messages only if:
        {
            "group": "notifications",
            "type": "notification",
            ...
         }
        """
        event = self.inject_html_code(event)
        self.send(text_data=json.dumps(event))

    def instatantlogg(self, event):
        """
        Receive message FROM THE CHANNEL and sent it TO WEBSOCKET
        more details see 'notification' docstring above
        """
        event['kind'] = 'logging'
        self.send(text_data=json.dumps(event))

    def inject_html_code(self, data):
        """Expand message by HTML/Javascript code for frontend"""
        data.update(dict(message=self.render(data)))
        return data

    def render(self, context=None):
        context = context or dict()
        output = render_to_string(self.HTML_TEMPLATE_FOR_INJECT, context)
        return output



# class NotificationConsumer(JsonWebsocketConsumer):

#     groups = ["notifications"]

#     def connect(self):

#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to group
#         async_to_sync(self.channel_layer.group_send)(
#             self.groups,
#             {
#                 'type': 'notifications.message',
#                 'message': message
#             }
#         )

#     # # Receive message from room group
#     # def chat_message(self, event):
#     #     message = event['message']

#     #     # Send message to WebSocket
#     #     self.send(text_data=json.dumps({
#     #         'message': message
#     #     }))



class ConsoleConsumer(JsonWebsocketConsumer):
    def connect(self):

        # self.room_name = 'console' #self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        self.accept()
        pass

    def disconnect(self, close_code):
        # # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        pass

    # # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["operators"]
        #pass

    # Receive message from WebSocket
    def receive(self, text_data):

        sub_id = 'ping'
        job_name = 'keepalive'

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        script = 'ping -c 5 google.com' #text_data['message']

        print(job_name)

        process = Popen(script, stdout=PIPE, shell=True)
        print (process)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            self.conWrite( ('<samp>'+str(line)+'</samp>'), ('console' + str(sub_id)), 'Green')
            # yield line
        
        print(text_data)
        self.conWrite( ('<samp>'+job_name+'</samp>'), ('console' + str(sub_id)), 'Green')
        
        # ssh.connect('192.168.1.117', username='osmc', password='osmc')
        
        # print('connection successfuly')

        # self.send({'console': 'connection successfuly'})

        # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(script)

        # print(ssh_stdout)
        # print('ssh_stdout')

        # self.groupAlert('<div class=\"alert alert-info alert-dismissible\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button><strong>Info!</strong> The job \'%s\' started.</div>' % job_name)
        # for line in iter(ssh_stdout.readline, ''):
        #     # self.conWrite( ('<samp>'+line+'</samp>'), ('console' + str(sub_id)), 'Green')
        #     pass
        # for line in iter(ssh_stderr.readline, ''):
        #     # self.conWrite( ('<samp>'+line+'</samp>'), ('console' + str(sub_id)), 'Red')
        #     pass
        # if ssh_stdout.channel.recv_exit_status() == 0:
        #     # self.groupAlert('<div class=\"alert alert-success alert-dismissible\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button><strong>Success!</strong> The job \'%s\' completed successfuly.</div>' % job_name)
        #     # self.conWrite( '<p class="bg-success">The job completed OK!</p>', ('console' + str(sub_id)), 'Black')
        #     pass
        # else:
        #     # self.groupAlert('<div class=\"alert alert-danger alert-dismissible\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button><strong>Attention!</strong> The job \'%s\' failed.</div>' % job_name)
        #     # self.conWrite( '<p class="bg-danger">The job failed!</p>', ('console' + str(sub_id)), 'Red')
        #     pass
        # ssh.close()

    def conCreate(self, div_id, **kwargs):
        self.send({'div_id': div_id})

    def conWrite(self, line=None, div_id='console', color='Black', **kwargs):
        self.send(json.dumps({'console': line, 'div_id': div_id, 'color': color}))

    def groupAlert(self, alert, **kwargs):
        self.channel_layer.group_send('operators', {'alert': alert })


# {'text': json.dumps(my_data_dict)}

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ConsoleConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'console' #self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))