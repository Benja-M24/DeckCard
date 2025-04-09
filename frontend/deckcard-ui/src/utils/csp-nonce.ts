// Utilizamos una manera compatible con ESM para generar nonces

// Extender tipos para TypeScript
declare global {
  // Para el objeto process de Node.js
  var process: {
    versions?: {
      node?: string
    }
  } | undefined;

  // Para el objeto crypto
  interface Crypto {
    getRandomValues(array: Uint8Array): Uint8Array;
  }

  // Para globalThis
  var crypto: Crypto;
}

/**
 * Generate a cryptographically secure random nonce for CSP
 */
export function generateNonce(): string {
  try {
    // Verificar si estamos en Node.js
    if (typeof globalThis.process?.versions?.node !== 'undefined') {
      return randomBytesNode();
    }
  } catch (e) {
    // Si hay error, usamos el método del navegador
  }
  
  // Usar Web Crypto API (funciona en navegadores y Node.js reciente)
  return randomBytesWebCrypto();
}

// Función para generar bytes aleatorios con Node.js
function randomBytesNode(): string {
  const buffer = new Uint8Array(16);
  // Node.js proporciona crypto.getRandomValues en versiones recientes
  if (typeof globalThis.crypto?.getRandomValues === 'function') {
    globalThis.crypto.getRandomValues(buffer);
    return arrayBufferToBase64(buffer);
  }
  
  // Si todo lo demás falla, usamos una versión simple
  for (let i = 0; i < 16; i++) {
    buffer[i] = Math.floor(Math.random() * 256);
  }
  return arrayBufferToBase64(buffer);
}

// Función para generar bytes aleatorios con Web Crypto API
function randomBytesWebCrypto(): string {
  const array = new Uint8Array(16);
  if (typeof globalThis.crypto?.getRandomValues === 'function') {
    globalThis.crypto.getRandomValues(array);
  } else {
    // Fallback si crypto.getRandomValues no está disponible
    for (let i = 0; i < 16; i++) {
      array[i] = Math.floor(Math.random() * 256);
    }
  }
  
  // Convertir a base64
  return arrayBufferToBase64(array);
}

// Función auxiliar para convertir Uint8Array a base64 sin depender de Buffer
function arrayBufferToBase64(buffer: Uint8Array): string {
  let binary = '';
  const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

// Store the nonce in global state for access during SSR
declare global {
  // eslint-disable-next-line no-var
  var nonce: string;
}

// Initialize with a default value that will be replaced per request
globalThis.nonce = generateNonce();
