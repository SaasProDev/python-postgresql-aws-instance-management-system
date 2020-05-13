import { Component, OnInit } from '@angular/core';
import {UserService} from "@app/_services";
import {CredentialService} from "@app/_services";
import {filter, first} from "rxjs/operators";
import {every} from "rxjs/operators";

@Component({
  selector: 'app-credentials',
  templateUrl: './credentials.component.html',
  styleUrls: ['./credentials.component.css']
})

export class CredentialsComponent implements OnInit {
  _credentials = [];


  constructor(private credentialService: CredentialService) { }

  load_data() {
    console.log("LOADING CREDENTIALS...", this._credentials);
    this.credentialService.getHtml().pipe(first()).subscribe(item => {
        console.log("CREDENTIAL ITEM", item);
        this._credentials.push(item)
    });
    console.log("CREDENTIALS DATA:", this._credentials);
  }

  ngOnInit() {
    this.load_data()
  }
}
