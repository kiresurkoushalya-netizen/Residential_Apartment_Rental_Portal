import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({ providedIn: 'root' })
export class AuthService {
private api = 'http://localhost:5000/api';


constructor(private http: HttpClient) {}


login(data:any){ return this.http.post(`${this.api}/auth/login`, data); }
register(data:any){ return this.http.post(`${this.api}/auth/register`, data); }


saveToken(token:string){ localStorage.setItem('token', token); }
getToken(){ return localStorage.getItem('token'); }


getRole(){
const token:any = this.getToken();
return JSON.parse(atob(token.split('.')[1])).role;
}
}