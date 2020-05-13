import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';

// socketio
import { SocketioService } from '../services/socketio.service';

@Component({
  selector: 'app-ahome-term',
  templateUrl: './ahome-term.component.html',
  styleUrls: ['./ahome-term.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class AhomeTermComponent implements OnInit {

  public terminal: Terminal;
  container: HTMLElement;

  constructor( socketioService: SocketioService ) { }

  ngOnInit() {
    this.terminal = new Terminal({ cursorBlink: true });
    const fitAddon = new FitAddon();

    this.terminal.loadAddon(fitAddon);

    this.container = document.getElementById('terminal');
    this.terminal.open(this.container);
    fitAddon.fit();

    this.terminal.write('Welcome to xterm.js !!!');
  }

}
