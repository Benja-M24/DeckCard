/// <reference types="astro/client" />

// Ampliar el contexto de Astro para incluir el nonce
declare namespace App {
  interface Locals {
    nonce: string;
  }
}
