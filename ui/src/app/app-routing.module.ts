import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AhomeTermComponent } from './ahome-term/ahome-term.component';
import { CredentialsComponent } from './components/credentials/credentials.component';
import { InstantloggingComponent } from './components/instantlogging/instantlogging.component';
import { ExternaltoolsComponent } from './components/externaltools/externaltools.component';
import { AppComponent } from './app.component';
import { IaasComponent } from './iaas/iaas.component';

import { HomeComponent } from './home';
import { LoginComponent } from './login';
import { AuthGuard } from './_helpers';

const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },

  { path: "credentials", component: CredentialsComponent },

  { path: "instantlogging", component: InstantloggingComponent },
  { path: "admin/externaltools", component: ExternaltoolsComponent },
  { path: "terminal", component: AhomeTermComponent, canActivate: [AuthGuard] },
  { path: "iaas", component: IaasComponent, canActivate: [AuthGuard] },

  // otherwise redirect to home
  { path: '**', redirectTo: '' }

];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }

