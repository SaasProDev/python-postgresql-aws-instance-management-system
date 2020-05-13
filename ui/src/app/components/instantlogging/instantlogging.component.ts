import { Component, OnInit } from '@angular/core';
import { environment } from '@environments/environment';

import { SocketioService } from '@app/services/socketio.service';
import { Message } from './message_model'

@Component({
  selector: 'app-instantlogging',
  templateUrl: './instantlogging.component.html',
  styleUrls: ['./instantlogging.component.css']
})
export class InstantloggingComponent implements OnInit {
  private sio: SocketioService;
  private messages: Message[];
  constructor() {
    const url = environment.websocketUrl;
    this.sio = new SocketioService(url);
  }

  ngOnInit() {
    const socket = this.sio.socket();

    socket.emit('test_event', {data: 'TEST 0001'});
    socket.emit('notification', {data: 'NOTIFICATION 0001'});

    socket.on('my_response', (msg) => {
        socket.emit('test_event', {data: 'CONNECTED'});
        socket.emit('notification', {data: 'notifications - CONNECTED'});
        console.log("RECEIVED", msg)
    });
    this.initial_data();
    this.render()
  }
  render() {
  }

  initial_data() {
    if (environment.test_data.websocket_notifications) {
      import("./test-data").then(data => {
        this.messages = data.dummy_messages;
        console.log("DUMMY INITIAL DATA LOADED FOR WEBSOCKET")
      });
    }
  }

}
