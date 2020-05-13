import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { environment } from '@environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SocketioService {

  private _default_url = environment.websocketUrl;
  private _socket;

  constructor(url?: String) {
    const _url = url === 'undefined' ? this._default_url : url;
  	this._socket = io(url);
    console.log("SOCKET URL: [" + url + "]")
  }
  socket() {
    return this._socket
  }
}
