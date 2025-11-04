import { Component } from '@angular/core';
import { ChatService } from '../../services/chat.service';

interface Character {
  id: string;
  name: string;
  icon: string;
  description: string;
}

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent {

}