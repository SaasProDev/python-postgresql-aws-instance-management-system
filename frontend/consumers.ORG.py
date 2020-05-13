from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import logging

import json

from django.template.loader import render_to_string

from subprocess import Popen, PIPE

logger_ = logging.getLogger(__name__)


class NotificationConsumer(WebsocketConsumer):

    # def connect(self):

    #     async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)

    
    def connect(self):

        self.broadcast = 'notifications'

        async_to_sync(self.channel_layer.group_add)(
            self.broadcast,
            self.channel_name
        )

        self.accept()

        # logger.error('Entry is not a float')
        

    def disconnect(self, close_code):
        pass


    def receive(self, text_data=None, bytes_data=None):
        
        data = json.loads(text_data)
        data.update(dict(
            message=self.render(data),
                )
            )

        # message = self.render(data)
        # task_id = data.get('task_id')

        # Send message to group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.broadcast,
        #     {
        #         'type': 'notification',
        #         'message': message,
        #         'task_id': task_id,
        #     }
        # )

        async_to_sync(self.channel_layer.group_send)(
            self.broadcast,
            data)


    # Receive message from group
    def notification(self, event):

        message = self.render(event)

        task_id = event.get('task_id')

        event.update(dict(
                message = self.render(event),
                )
            )

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': message,
        #     'task_id': task_id,
        #     })
        # )

        self.send( text_data=json.dumps(event) )


    def render(self, context=dict()):
        # context = {'message': message}
        output = render_to_string('frontend/includes/helpers/websocket-notification.tpl.html', context)
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