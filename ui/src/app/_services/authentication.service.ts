import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { tap } from 'rxjs/operators';

import { environment } from '@environments/environment';
import { User, Token } from '@app/_models';

@Injectable({ providedIn: 'root' })

export class AuthenticationService {
    private currentTokenSubject: BehaviorSubject<Token>;
    public currentToken: Observable<Token>;

    constructor(private http: HttpClient) {
        this.currentTokenSubject = new BehaviorSubject<Token>(JSON.parse(localStorage.getItem('access_token')));
        this.currentToken = this.currentTokenSubject.asObservable();
    }

    public get currentTokenValue(): Token {
        return this.currentTokenSubject.value;
    }

    login(username: string, password: string) {
        return this.http.post<any>(`${environment.apiUrl}/api/token/`, { username, password })
            // store user details and jwt token in local storage to keep user logged in between page refreshesh
            .pipe(tap(res => {
                res.username = username;
                localStorage.setItem('access_token', JSON.stringify(res));
                // console.log(JSON.stringify(res));
                this.currentTokenSubject.next(res);
                return res;
            }
            ));

    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('access_token');
        this.currentTokenSubject.next(null);
    }

}



// export class AuthService {
//   endpoint: string = 'http://localhost:4000/api';
//   headers = new HttpHeaders().set('Content-Type', 'application/json');
//   currentUser = {};

//   constructor(
//     private http: HttpClient,
//     public router: Router
//   ) {
//   }

//   // Sign-up
//   signUp(user: User): Observable<any> {
//     let api = `${this.endpoint}/register-user`;
//     return this.http.post(api, user)
//       .pipe(
//         catchError(this.handleError)
//       )
//   }

//   // Sign-in
//   signIn(user: User) {
//     return this.http.post<any>(`${this.endpoint}/signin`, user)
//       .subscribe((res: any) => {
//         localStorage.setItem('access_token', res.token)
//         this.getUserProfile(res._id).subscribe((res) => {
//           this.currentUser = res;
//           this.router.navigate(['user-profile/' + res.msg._id]);
//         })
//       })
//   }

//   getToken() {
//     return localStorage.getItem('access_token');
//   }

//   get isLoggedIn(): boolean {
//     let authToken = localStorage.getItem('access_token');
//     return (authToken !== null) ? true : false;
//   }

//   doLogout() {
//     let removeToken = localStorage.removeItem('access_token');
//     if (removeToken == null) {
//       this.router.navigate(['log-in']);
//     }
//   }

//   // User profile
//   getUserProfile(id): Observable<any> {
//     let api = `${this.endpoint}/user-profile/${id}`;
//     return this.http.get(api, { headers: this.headers }).pipe(
//       map((res: Response) => {
//         return res || {}
//       }),
//       catchError(this.handleError)
//     )
//   }

//   // Error 
//   handleError(error: HttpErrorResponse) {
//     let msg = '';
//     if (error.error instanceof ErrorEvent) {
//       // client-side error
//       msg = error.error.message;
//     } else {
//       // server-side error
//       msg = `Error Code: ${error.status}\nMessage: ${error.message}`;
//     }
//     return throwError(msg);
//   }
// }