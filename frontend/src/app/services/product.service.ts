import { Injectable } from '@angular/core';
import { environment } from '../../environments/environments';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ProductSearchResult } from '../model/productSearchResult.model';

@Injectable({
  providedIn: 'root'
})
export class ProductService {


  private apiUrl = environment.url + '/handle-product';

  constructor(private http: HttpClient) { }

  getProducts(): Observable<ProductSearchResult[]> {
    return this.http.get<ProductSearchResult[]>(this.apiUrl + '/product-result');
  }
  deleteProduct(productId: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/delete-product/${productId}`);

  }
}
