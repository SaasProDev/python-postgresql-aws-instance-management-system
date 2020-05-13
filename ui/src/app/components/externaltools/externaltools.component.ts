import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import {InfoStatusCardConfig} from "patternfly-ng";


@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'app-externaltools',
  templateUrl: './externaltools.component.html',
  styleUrls: ['./externaltools.component.css']
})
export class ExternaltoolsComponent implements OnInit {

  constructor() { }
  ngOnInit() {
  }
  rabbitmq_card: InfoStatusCardConfig = {
    showTopBorder: true,
    htmlContent: true,
    title: 'RabbitMQ',
    href: 'http://192.168.1.97:15672',
    iconStyleClass: 'fa fa-rabbit',
    iconImageSrc: 'https://hackr.io/tutorials/rabbitmq/logo-rabbitmq.svg?ver=1557508241',
    info: [
      'Kind: Service',
      'Environment: Development',
    ]
  };
  ui_card: InfoStatusCardConfig = {
    showTopBorder: true,
    htmlContent: true,
    title: 'Patternfly UI',
    href: 'https://patternfly.github.io/patternfly-ng/',
    iconStyleClass: 'fa fa-rabbit',
    iconImageSrc: 'https://www.patternfly.org/v3/assets/img/patternfly-orb.svg',
    info: [
      'Kind: Web Development',
      'Environment: Development',
    ]
  };

  icons_card: InfoStatusCardConfig = {
    showTopBorder: true,
    htmlContent: true,
    title: 'Icons',
    href: 'https://www.patternfly.org/v3/styles/icons/',
    iconStyleClass: 'fa fa-icon',
    iconImageSrc: 'https://www.patternfly.org/v3/assets/img/patternfly-orb.svg',
    info: [
      'Kind: Web Development',
      'Environment: Development',
    ]
  }
}


