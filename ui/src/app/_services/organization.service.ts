import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '@environments/environment';
import { Organization } from '@app/_models';

@Injectable({ providedIn: 'root' })
export class OrganizationService {
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<Organization[]>(`${environment.apiUrl}/api/v1/organizations/`);
    }
}

