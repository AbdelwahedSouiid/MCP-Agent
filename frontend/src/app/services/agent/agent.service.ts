import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environments';
import { HttpClient, HttpParams } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private apiUrl = environment.agent_url + '/api/mcp/ask';

  constructor(private http: HttpClient) { }

  ask_agent(question: string): Observable<string> {
    // Utilisation de HttpParams pour les paramètres de requête
    const params = new HttpParams().set('question', question);
    
    return this.http.post(this.apiUrl, null, { 
      params: params,
      responseType: 'text'
    }).pipe(
      catchError(error => {
        console.error('API Error:', error);
        return throwError(() => new Error('Erreur de communication avec l\'agent'));
      })
    );
  }
}