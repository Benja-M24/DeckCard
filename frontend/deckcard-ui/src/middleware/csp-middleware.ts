import { defineMiddleware } from 'astro:middleware';
import { generateNonce } from '../utils/csp-nonce';

export const onRequest = defineMiddleware(async (context, next) => {
  // Generate a new nonce for each request
  const nonce = generateNonce();
  
  // Set the nonce in global state for access during rendering
  globalThis.nonce = nonce;
  
  // Process the request
  const response = await next();
  
  // Clone the response to modify headers
  const newResponse = new Response(response.body, response);
  
  // Get existing CSP header if any
  const existingCsp = newResponse.headers.get('Content-Security-Policy');
  
  // Build new CSP with nonce
  const scriptSrc = `script-src 'self' 'nonce-${nonce}'`;
  
  // If there's an existing CSP, replace script-src section
  let csp = '';
  if (existingCsp) {
    // Replace existing script-src directive or append if not present
    const hasScriptSrc = existingCsp.includes('script-src');
    if (hasScriptSrc) {
      csp = existingCsp.replace(/script-src [^;]+/, scriptSrc);
    } else {
      csp = `${existingCsp}; ${scriptSrc}`;
    }
  } else {
    // Create a basic CSP with our script-src
    csp = `default-src 'self'; ${scriptSrc}; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://* http://*; font-src 'self' data:; connect-src 'self' https://* http://*; frame-src 'self'; base-uri 'self'; form-action 'self'`;
  }
  
  // Set the updated CSP header
  newResponse.headers.set('Content-Security-Policy', csp);
  
  return newResponse;
});
