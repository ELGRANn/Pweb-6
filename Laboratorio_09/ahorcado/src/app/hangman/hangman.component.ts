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

  ngOnInit(): void {
    this.nuevaPalabra();
  }

  nuevaPalabra() {
    this.palabraActual = this.palabras[Math.floor(Math.random() * this.palabras.length)];
    this.letrasAdivinadas = Array(this.palabraActual.length).fill('_');
    this.intentosRestantes = 7;
    this.actualizarImagenAhorcado();
  }

  adivinar(letra: string) {
    if (this.palabraActual.includes(letra)) {
      for (let i = 0; i < this.palabraActual.length; i++) {
        if (this.palabraActual[i] === letra) {
          this.letrasAdivinadas[i] = letra;
        }
      }
    } else {
      this.intentosRestantes--;
      this.actualizarImagenAhorcado();
    }
  }

  actualizarImagenAhorcado() {
    this.imagenAhorcado = `assets/images/${7 - this.intentosRestantes}.svg`;
  }
}