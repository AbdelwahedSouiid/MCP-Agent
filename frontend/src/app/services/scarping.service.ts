import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Product } from '../model/product.model';
import { environment } from '../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class ScrapingService {
  private apiUrl = environment.urlForm + '/scrapy/product' ;
  constructor(private http: HttpClient) { }

  scrapeProduct(url: string): Observable<Product> {
    // Nettoyage initial de l'URL
    let cleanedUrl = url.trim();
    
    // Suppression du fragment (#) si présent
    cleanedUrl = cleanedUrl.split('#')[0];
    
    // Vérification du protocole
    if (!cleanedUrl.match(/^https?:\/\//i)) {
      return throwError(() => new Error('URL doit commencer par http:// ou https://'));
    }
    
    // Encodage UNIQUE de l'URL
    const encodedUrl = encodeURI(cleanedUrl); // encodeURI au lieu de encodeURIComponent
    
    // Utilisation de HttpParams pour une meilleure gestion
    const params = new HttpParams().set('url', cleanedUrl); // Envoyez l'URL non encodée
    
    return this.http.get<Product>(this.apiUrl, { params }).pipe(
      catchError(error => {
        console.error('Erreur complète:', error);
        const errorMsg = error.error?.detail || 
                        error.message || 
                        'Erreur inconnue lors du scraping';
        return throwError(() => new Error(errorMsg));
      })
    );
  }
}