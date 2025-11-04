import { Component, OnDestroy, OnInit, ViewChild, ElementRef} from '@angular/core';
import { ChatService } from '../services/chat.service';
import { Subscription } from 'rxjs';
import { ChatMessage } from '../model/chatMessage.model';
import { TranscribeService } from '../services/transcribe.service';

import { AgentService } from '../services/agent/agent.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, OnDestroy {
  @ViewChild('messageInput') messageInput!: ElementRef;
  @ViewChild('messageContainer') messageContainer!: ElementRef;

  // Variables pour la transcription vocale
  isRecording = false;
  isProcessing = false;
  mediaRecorder: MediaRecorder | null = null;
  audioChunks: Blob[] = [];

  // Variables pour le chat
  userQuery = '';
  messageHistory: ChatMessage[] = [];
  loading = false;
  error = '';
  activeCharacter = 'default';

  selectedAgentType: string = 'agent';

  // Abonnements
  private chatSubscription: Subscription | null = null;
  private transcribeSubscription: Subscription | null = null;


  constructor(
    private chatService: ChatService,
    private agentService: AgentService,
    private transcribeService: TranscribeService
  ) { }

  ngOnInit(): void {
    this.addBotMessage('Bonjour, comment puis-je vous aider aujourd\'hui ?');

  }
  private lastMessageCount = 0;

  ngAfterViewChecked() {
    if (this.messageHistory.length !== this.lastMessageCount) {
      this.lastMessageCount = this.messageHistory.length;
      this.scrollToBottom();
    }
  }

  private scrollToBottom(): void {
    try {
      this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Scroll error:', err);
    }
  }

  sendQuery(): void {
    const query = this.userQuery.trim();
  
    if (query && !this.loading) {
      this.addUserMessage(query);
      this.loading = true;
      this.error = '';
      this.userQuery = '';
  
      if (this.selectedAgentType === 'agent') {
        // Cas de l'agent (réponse simple)
        this.chatSubscription = this.agentService.ask_agent(query).subscribe({
          next: (response) => {
            console.log("reponse du chatbot : ",response) 
            this.addBotMessage(response);
            this.loading = false;
          },
          error: (err) => {
            this.error = `Erreur: ${err}`;
            this.loading = false;
          }
        });
      } else {
        // Cas de l'assistant (streaming)
        this.chatSubscription = this.chatService.streamMessage(query).subscribe({
          next: (chunk) => {
            this.updateLastBotMessage(chunk);
          },
          error: (err) => {
            this.error = `Erreur: ${err}`;
            this.loading = false;
          },
          complete: () => {
            this.loading = false;
          }
        });
      }
    } else if (!query) {
      this.error = "Veuillez entrer une question valide";
    }
  }

  private addUserMessage(content: string): void {
    this.messageHistory.push({
      content,
      isUser: true,
      timestamp: new Date()
    });
  }

  private addBotMessage(content: string): void {
    this.messageHistory.push({
      content,
      isUser: false,
      timestamp: new Date()
    });
  }

  private updateLastBotMessage(chunk: string): void {
    const lastMessage = this.messageHistory[this.messageHistory.length - 1];
    if (lastMessage && !lastMessage.isUser) {
      lastMessage.content += chunk;
    } else {
      this.addBotMessage(chunk);
    }
  }

  async toggleRecording(): Promise<void> {
    if (this.isRecording) {
      await this.stopRecording();
    } else {
      await this.startRecording();
    }
  }

  private async startRecording(): Promise<void> {
    try {
      this.error = '';
      this.audioChunks = [];

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

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

      this.mediaRecorder.onstop = async () => {
        this.isProcessing = true;

        if (this.audioChunks.length > 0) {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });

          this.transcribeSubscription = this.transcribeService.transcribeAudio(audioBlob).subscribe({
            next: (response) => {
              const fullText = response.segments.map(segment => segment.text).join(' ');
              this.userQuery = fullText;
              setTimeout(() => {
                this.messageInput.nativeElement.focus();
              }, 100);
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

      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    });
  }

  ngOnDestroy(): void {
    if (this.chatSubscription) {
      this.chatSubscription.unsubscribe();
    }

    if (this.transcribeSubscription) {
      this.transcribeSubscription.unsubscribe();
    }

    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
  }


  handleImageError(event: Event) {
    const img = event.target as HTMLImageElement;
    img.src = 'assets/images/default-product.jpg';
    img.classList.add('error-image');
  }

  @ViewChild('chatSection') chatSection!: ElementRef;


  isResizing = false;
  startX = 0;
  startWidth = 0;

}   
