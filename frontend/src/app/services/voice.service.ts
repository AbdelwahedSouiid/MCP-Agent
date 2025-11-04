import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environments';

@Injectable({ providedIn: 'root' })
export class VoiceService {
  private apiUrl = environment.url + '/voice';

  constructor(private ngZone: NgZone) {}

  streamAudio(audioBlob: Blob): Observable<string> {
    return new Observable<string>(observer => {
      const audioFile = new File([audioBlob], `recording_${Date.now()}.wav`, {
        type: 'audio/wav'
      });

      const formData = new FormData();
      formData.append('file', audioFile);

      fetch(`${this.apiUrl}/bot_query`, { 
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'text/event-stream'
        }
      })
      .then(response => {
        if (!response.ok || !response.body) {
          throw new Error(response.statusText || 'Erreur serveur');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        const read = () => {
          reader.read().then(({ done, value }) => {
            if (done) {
              if (buffer.trim()) {
                this.ngZone.run(() => {
                  observer.next(buffer.trim());
                });
              }
              observer.complete();
              return;
            }

            buffer += decoder.decode(value, { stream: true });

            let lines = buffer.split('\n');
            buffer = lines.pop() || ''; // garde la dernière ligne incomplète

            for (const line of lines) {
              const cleaned = line.trim();
              if (cleaned.startsWith('event: messagedata:')) {
                const message = cleaned.replace('event: messagedata:', '').trim();
                if (message.length > 0) {
                  this.ngZone.run(() => {
                    observer.next(message);
                  });
                }
              }
              if (cleaned === 'stream-complete') {
                observer.complete();
              }
            }

            read();
          }).catch(err => {
            this.ngZone.run(() => observer.error(err));
          });
        };

        read();
      })
      .catch(err => {
        this.ngZone.run(() => observer.error(err));
      });
    });
  }
}
