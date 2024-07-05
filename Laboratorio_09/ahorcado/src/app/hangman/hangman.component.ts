import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-hangman',
  templateUrl: './hangman.component.html',
  styleUrls: ['./hangman.component.css']
})
export class HangmanComponent implements OnInit {
  palabras: string[] = ['palabraPrueba', 'mensaje', 'unsa', 'programa', 'developer'];
  palabraActual: string = '';
  letrasAdivinadas: string[] = [];
  intentosRestantes: number = 7;
  imagenAhorcado: string = '';

  constructor() { }


}
