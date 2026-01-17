import { Injectable } from '@angular/core';
import { HttpInterceptor } from '@angular/common/http';
import { AuthService } from '../services/auth.service';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {
constructor(private auth: AuthService) {}


intercept(req:any, next:any){
const token = this.auth.getToken();
if(token){
req = req.clone({
headers: req.headers.set('Authorization', `Bearer ${token}`)
});
}
return next.handle(req);
}
}