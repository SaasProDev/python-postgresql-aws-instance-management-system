import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '@environments/environment';
// import { User } from '@app/_models';

@Injectable({ providedIn: 'root' })
export class CredentialService {
    constructor(private http: HttpClient) { }

    getData() {
        return this.http.get(`${environment.apiUrl}/api/v1/usercredentials/`);
    }
    getHtml() {
        return this.http.get(`${environment.apiUrl}/frontend/usercredentials/list/`);
    }
}

