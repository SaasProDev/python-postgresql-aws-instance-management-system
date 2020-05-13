import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

// used to create fake backend
import { fakeBackendProvider } from './_helpers';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { VerticalNavigationModule } from 'patternfly-ng/navigation';
import { ListModule } from 'patternfly-ng/list';

// NGX Bootstrap
import { BsDropdownConfig, BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { TooltipConfig, TooltipModule } from 'ngx-bootstrap/tooltip';


import { JwtInterceptor, ErrorInterceptor } from './_helpers';
import { HomeComponent } from './home';
import { LoginComponent } from './login';

import { AhomeTermComponent } from './ahome-term/ahome-term.component';
import { IaasComponent } from './iaas/iaas.component';

// socketio
import { SocketioService } from './services/socketio.service';
import { InstantloggingComponent } from './components/instantlogging/instantlogging.component';
import { ExternaltoolsComponent } from './components/externaltools/externaltools.component'
import {InfoStatusCardModule} from "patternfly-ng/card";
import { CredentialsComponent } from './components/credentials/credentials.component';


@NgModule({
  declarations: [
    AppComponent,
    AhomeTermComponent,
    IaasComponent,
    HomeComponent,
    LoginComponent,
    InstantloggingComponent,
    ExternaltoolsComponent,
    CredentialsComponent
  ],
  imports: [
    VerticalNavigationModule,
    BsDropdownModule.forRoot(),
    TooltipModule.forRoot(),
    BrowserModule,
    AppRoutingModule,
    ListModule,
    ReactiveFormsModule,
    HttpClientModule,
    InfoStatusCardModule,
  ],

  providers: [
      { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
      { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
      BsDropdownConfig,
      TooltipConfig,
      SocketioService
      // provider used to create fake backend
      // fakeBackendProvider
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }


