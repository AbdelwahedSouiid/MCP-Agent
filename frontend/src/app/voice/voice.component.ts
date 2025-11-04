import { Component, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { TranscribeService } from '../services/transcribe.service';

@Component({
  selector: 'app-voice',
  templateUrl: './voice.component.html',
  styleUrl: './voice.component.css',
})
export class VoiceComponent implements OnDestroy {
  isRecording = false;
  isProcessing = false;
  error = '';
  transcription = '';
  mediaRecorder: MediaRecorder | null = null;
  audioChunks: Blob[] = [];
  subscription: Subscription | null = null;

  constructor(private voiceService: TranscribeService) {}

  async toggleRecording() {
    if (this.isRecording) {
      await this.stopRecording();
    } else {
      await this.startRecording();
    }
  }

  private async startRecording() {
    try {
      // Réinitialiser les états
      this.error = '';
      this.audioChunks = [];
      
      // Demander l'accès au microphone d'abord
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Configuration du MediaRecorder une fois l'accès accordé
      this.mediaRecorder = new MediaRecorder(stream);
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };
      
      // Démarrer l'enregistrement après configuration
      this.mediaRecorder.start(100);
      this.isRecording = true;
    } catch (err) {
      this.error = 'Accès au microphone refusé';
      this.isRecording = false;
    }
  }

  private async stopRecording(): Promise<void> {
    return new Promise((resolve) => {
      if (!this.mediaRecorder) {
        resolve();
        return;
      }
      
      this.isRecording = false;
      
      // Gestion explicite de la fin d'enregistrement
      this.mediaRecorder.onstop = async () => {
        this.isProcessing = true;
        
        // S'assurer qu'il y a des données audio à traiter
        if (this.audioChunks.length > 0) {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
          
          this.subscription = this.voiceService.transcribeAudio(audioBlob).subscribe({
            next: (response) => {
              const fullText = response.segments.map(segment => segment.text).join(' ');
              this.transcription = fullText;
              this.isProcessing = false;
              resolve();
            },
            error: (err) => {
              this.error = 'Erreur de transcription: ' + err.message;
              this.isProcessing = false;
              resolve();
            }
          });
        } else {
          this.error = 'Aucun audio enregistré';
          this.isProcessing = false;
          resolve();
        }
      };
      
      // Arrêter l'enregistrement seulement après avoir configuré l'événement onstop
      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    });
  }

  ngOnDestroy() {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
    
    if (this.mediaRecorder) {
      if (this.isRecording) {
        this.mediaRecorder.stop();
      }
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
  }
}