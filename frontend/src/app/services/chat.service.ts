import { Injectable, NgZone } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environments';
import { QueryType } from '../enum/queryType.enum';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private activeCharacter = new BehaviorSubject<string>('default');
  private baseUrl = environment.url + '/bot';

  constructor(private ngZone: NgZone) {}

  setActiveCharacter(character: string) {
    this.activeCharacter.next(character);
  }

  getActiveCharacter() {
    return this.activeCharacter.asObservable();
  }

  streamMessage(query: string): Observable<string> {
    return new Observable<string>(observer => {
      if (typeof EventSource === 'undefined') {
        this.ngZone.run(() => {
          observer.error('Votre navigateur ne supporte pas les Server-Sent Events');
        });
        return;
      }

      const url = new URL(`${this.baseUrl}/bot-query`);
      url.searchParams.append('query', query);
      const es = new EventSource(url.toString());

      es.onmessage = (event) => {
        this.ngZone.run(() => {
          try {
            if (event.data === '[DONE]') {
              es.close();
              observer.complete();
            } else {
              observer.next(event.data);
            }
          } catch (err) {
            console.error('Error processing message:', err);
            observer.error('Erreur de traitement du message');
          }
        });
      };

      es.onerror = (error) => {
        this.ngZone.run(() => {
          console.error('SSE Error:', error);
          if (es.readyState !== EventSource.CLOSED) {
            es.close();
          }
          if (es.readyState === EventSource.CLOSED) {
            observer.complete();
          } else {
            observer.error(this.getErrorMessage(es.readyState));
          }
        });
      };

      return () => {
        if (es.readyState !== EventSource.CLOSED) {
          es.close();
        }
      };
    });
  }

  private getErrorMessage(readyState: number): string {
    switch (readyState) {
      case EventSource.CONNECTING:
        return 'Connexion au serveur en cours...';
      case EventSource.OPEN:
        return 'Erreur pendant la communication';
      case EventSource.CLOSED:
        return 'Connexion fermée par le serveur';
      default:
        return 'Erreur inconnue';
    }
  }

  testSSEConnection(): void {
    const testUrl = new URL(`${this.baseUrl}/health-check`);
    const es = new EventSource(testUrl.toString());

    es.onmessage = (e) => console.log('Test SSE Message:', e.data);
    es.onopen = () => console.log('Test SSE Connection: OPEN');
    es.onerror = (e) => console.error('Test SSE Error:', e);
  }
}
