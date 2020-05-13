import { Injectable } from '@angular/core';
import { catchError, map, tap } from 'rxjs/operators';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';

import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { environment } from '@environments/environment';
import { User, Snippet } from '@app/_models';


@Injectable({ providedIn: 'root' })
export class FrontendService {

	// headers = new HttpHeaders().set('Content-Type', 'application/json');
	headers = new HttpHeaders().set('Content-Type', 'text/html');

	log;
	logError;
	htmlSnippet: string = '';
	// token = localStorage.getItem('access_token');


    constructor(
    	private http: HttpClient,
    	private sanitizer: DomSanitizer
    	) { }

    getIaas() {

	    // return this.http.get(`${environment.apiUrl}/frontend/organizations/list/`, { headers: {'Accept': 'text/html', 'Content-Type': 'text/html', 'Authorization': 'Bearer '+localStorage.getItem('access_token')} });

	    const url = `${environment.apiUrl}/frontend/organizations/list/`;

	    // console.log(url);
	    // this.htmlSnippet = this.sanitizer.bypassSecurityTrustHtml(this.jquerySnippet);

	    // const trustedUrl = this.sanitizer.bypassSecurityTrustUrl(url);

	    return this.http.get(url, {responseType: 'text'})
	        .pipe(
	          tap( // Log the result or error
	            data => { data; }
	          )
	        );


	    // this.http.get(url, {responseType: 'text'})
	    //     .subscribe(
	    //         data => { 
	    //         	// console.log(data);
	    //         	this.htmlSnippet = data; 
	    //         }
	    //     );

	    // return this.htmlSnippet;





	  //   return this.http.get(url, {responseType: 'text'}).subscribe(data => {
			// 	  console.log(data);
			// 	  return data;
			// });

	    // return this.http.get( url, {responseType: 'text', headers :{'Accept': 'text/html', 'Authorization': 'Bearer '+localStorage.getItem('access_token')}} );

	    // return this.http.get(url, {responseType: 'text'})
	    //     .pipe(
	    //       tap( // Log the result or error
	    //         data => data
	    //       )
	    //     );

	    // return this.http.get('...', { responseType: 'text' }); 
    }
}



