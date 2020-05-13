import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthenticationService } from '@app/_services';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
    constructor(private authenticationService: AuthenticationService) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // add authorization header with jwt token if available
        let currentToken = this.authenticationService.currentTokenValue;
        if (currentToken && `${currentToken.access}`) {
            // console.log(`jwt: ${currentToken.access}`);
            request = request.clone({
                setHeaders: {
                    Authorization: `Bearer ${currentToken.access}`
                }
            });

        }

        // console.log(`req: ${request}`);
        return next.handle(request);
    }
}