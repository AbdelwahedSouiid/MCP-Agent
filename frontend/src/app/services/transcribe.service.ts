import { Injectable } from '@angular/core';
import { environment } from '../../environments/environments';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TranscriptionResponse } from '../model/TranscriptionResponse.model';
@Injectable({
  providedIn: 'root'
})
export class TranscribeService {
  private apiUrl = environment.url + '/voice/transcribe';

  constructor(private http: HttpClient) {}

  transcribeAudio(audioBlob: Blob): Observable<TranscriptionResponse> {
    const formData = new FormData();
    formData.append('file', audioBlob, `recording_${Date.now()}.wav`);
    
    return this.http.post<TranscriptionResponse>(this.apiUrl, formData);
  }
}