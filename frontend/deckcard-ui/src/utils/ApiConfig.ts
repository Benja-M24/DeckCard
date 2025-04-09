/**
 * Módulo para manejar la configuración de la API y las utilidades HTTP
 * Aplica el principio de responsabilidad única separando la configuración de la lógica de negocio
 * Última actualización: 04/04/2025
 */

/**
 * Genera una URL dinámica para las llamadas a la API, adaptándose al entorno (servidor o cliente)
 * @param endpoint - Ruta relativa de la API sin el prefijo
 * @returns URL completa y válida para la API
 */
export function dynamicApiUrl(endpoint: string): string {
  let apiUrl = '';
  
  // Asegurar que el endpoint no tenga ya una barra al final
  const cleanEndpoint = endpoint.endsWith('/') ? endpoint.slice(0, -1) : endpoint;

  // Comprobar si se ejecuta en servidor (sin objeto window) o cliente
  if (typeof window === 'undefined') {
    // Contexto de servidor (SSR)
    // En el servidor, usa la ruta interna de Docker
    apiUrl = `http://backend:8800/${cleanEndpoint}/`;
  } else {
    // Contexto de cliente (navegador)
    // ARQUITECTURA: Cuando el código se ejecuta en el navegador del cliente,
    // debe usar el dominio público para que Traefik redirija al contenedor backend
    const domain = window.location.hostname;
    
    // Construir la URL completa con el subdominio api
    // Si estamos en localhost durante desarrollo, usar un puerto diferente o la ruta completa
    if (domain === 'localhost' || domain.includes('127.0.0.1')) {
      // En desarrollo local (sin Traefik), usamos una ruta a la API en el mismo host
      apiUrl = `http://${domain}:8800/${cleanEndpoint}/`;
    } else {
      // En producción, usamos el subdominio api configurado en Traefik
      // Preservamos el protocolo (http/https) del sitio principal
      const protocol = window.location.protocol;
      apiUrl = `${protocol}//api.${domain}/${cleanEndpoint}/`;
    }
    
    // Debug logging para depuración
    console.log(`[Browser] Generando URL de API: ${apiUrl} para endpoint: ${endpoint}`);
  }

  // Debug logging solo en desarrollo
  if (import.meta.env.DEV) {
    console.log(`API URL constructed: ${apiUrl} for path: ${endpoint}`);
  }
  
  return apiUrl;
}

/**
 * Función para obtener el token CSRF de las cookies
 */
export function getCSRFToken(): string | null {
  if (typeof document === 'undefined') return null;
  
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    // Django usa 'csrftoken' como nombre de la cookie
    if (cookie.startsWith('csrftoken=')) {
      return cookie.substring('csrftoken='.length, cookie.length);
    }
  }
  
  console.warn('No se encontró token CSRF en las cookies');
  return null;
}

/**
 * Opciones por defecto para las peticiones fetch
 */
export const defaultFetchOptions: RequestInit = {
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  credentials: 'include',
};

/**
 * Tipos de errores HTTP personalizados
 */
export enum HttpErrorType {
  NETWORK = 'NETWORK_ERROR',
  TIMEOUT = 'TIMEOUT_ERROR',
  AUTH = 'AUTH_ERROR',
  NOT_FOUND = 'NOT_FOUND',
  VALIDATION = 'VALIDATION_ERROR',
  SERVER = 'SERVER_ERROR',
  UNKNOWN = 'UNKNOWN_ERROR'
}

/**
 * Clase base para gestionar errores HTTP con tipos específicos
 */
export class HttpError extends Error {
  status: number;
  type: HttpErrorType;
  details?: Record<string, any>;
  
  constructor(message: string, status: number, type = HttpErrorType.UNKNOWN, details?: Record<string, any>) {
    super(message);
    this.name = 'HttpError';
    this.status = status;
    this.type = type;
    this.details = details;
  }
}

/**
 * Configuración para las opciones del cliente HTTP
 */
interface HttpClientConfig {
  /** Tiempo máximo de espera en ms antes de abortar la petición */
  timeout?: number;
  /** Número de reintentos ante fallos de red */
  retries?: number;
  /** Tiempo entre reintentos en ms */
  retryDelay?: number;
  /** Si debe usar caché para peticiones GET */
  useCache?: boolean;
  /** Tiempo de vida de la caché en ms */
  cacheTTL?: number;
}

/**
 * Configuración por defecto para el cliente HTTP
 */
const DEFAULT_CONFIG: HttpClientConfig = {
  timeout: 10000,  // 10 segundos
  retries: 2,
  retryDelay: 1000, // 1 segundo
  useCache: true,
  cacheTTL: 60000    // 1 minuto
};

/**
 * Caché simple para resultados de peticiones GET
 */
class RequestCache {
  private cache: Map<string, {data: any, timestamp: number}> = new Map();
  
  get<T>(key: string, ttl: number): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;
    
    // Comprobar si la entrada ha expirado
    if (Date.now() - entry.timestamp > ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return entry.data as T;
  }
  
  set<T>(key: string, data: T): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
  
  clear(): void {
    this.cache.clear();
  }
}

// Instancia global de caché
const globalCache = new RequestCache();

/**
 * Cliente HTTP mejorado para realizar peticiones a la API
 * Ofrece manejo de errores avanzado, reintentos, timeouts y caché
 */
export class HttpClient {
  private static config: HttpClientConfig = DEFAULT_CONFIG;
  
  /**
   * Configura las opciones globales del cliente HTTP
   */
  static configure(config: Partial<HttpClientConfig>): void {
    HttpClient.config = { ...DEFAULT_CONFIG, ...config };
  }
  
  /**
   * Gestiona la deserialización y validación de respuestas
   */
  private static async handleResponse<T>(response: Response): Promise<T> {
    // Para respuestas 204 No Content, devolver objeto vacío
    if (response.status === 204) {
      return {} as T;
    }
    
    // Intentar deserializar JSON
    try {
      const data = await response.json();
      
      // Si la API devuelve un formato específico de error
      if (!response.ok && data.errors) {
        throw new HttpError(
          data.message || 'Error procesando la solicitud',
          response.status,
          getErrorTypeFromStatus(response.status),
          data.errors
        );
      }
      
      return data as T;
    } catch (error) {
      // Si ya es un HttpError, lo propagamos
      if (error instanceof HttpError) throw error;
      
      // Error al parsear JSON
      throw new HttpError(
        'Error al procesar la respuesta del servidor',
        response.status,
        HttpErrorType.SERVER
      );
    }
  }
  
  /**
   * Ejecuta una petición con soporte para reintentos
   */
  private static async fetchWithRetry<T>(
    url: string, 
    options: RequestInit, 
    config: HttpClientConfig
  ): Promise<T> {
    let lastError: Error;
    const { retries = 0, retryDelay = 1000, timeout = 10000 } = config;
    
    // Intentar la petición el número de veces configurado
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        // Crear AbortController para manejar timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        
        const fetchOptions = {
          ...options,
          signal: controller.signal
        };
        
        try {
          const response = await fetch(url, fetchOptions);
          clearTimeout(timeoutId);
          return await HttpClient.handleResponse<T>(response);
        } catch (error) {
          clearTimeout(timeoutId);
          throw error;
        }
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        
        // Si es un error de timeout o red y hay más intentos, esperar y reintentar
        if (attempt < retries && (
          error instanceof DOMException && error.name === 'AbortError' || 
          !navigator.onLine
        )) {
          await new Promise(resolve => setTimeout(resolve, retryDelay));
          continue;
        }
        
        // Errores de timeout
        if (error instanceof DOMException && error.name === 'AbortError') {
          throw new HttpError(
            'La solicitud excedió el tiempo de espera',
            0,
            HttpErrorType.TIMEOUT
          );
        }
        
        // Errores de red
        if (!navigator.onLine || error instanceof TypeError) {
          throw new HttpError(
            'Error de conexión a la red',
            0,
            HttpErrorType.NETWORK
          );
        }
        
        throw lastError;
      }
    }
    
    // Este código nunca debería ejecutarse pero TypeScript lo requiere
    throw lastError!;
  }
  
  /**
   * Realiza una petición GET con soporte para caché
   * @param url URL completa para la petición
   * @param customConfig Configuración específica para esta petición
   * @returns Promesa con la respuesta deserializada
   */
  static async get<T>(url: string, customConfig?: Partial<HttpClientConfig>): Promise<T> {
    const config = { ...HttpClient.config, ...customConfig };
    
    // Comprobar caché si está habilitado
    if (config.useCache) {
      const cachedData = globalCache.get<T>(url, config.cacheTTL || DEFAULT_CONFIG.cacheTTL!);
      if (cachedData) return cachedData;
    }
    
    const response = await HttpClient.fetchWithRetry<T>(url, {
      ...defaultFetchOptions,
      method: 'GET',
    }, config);
    
    // Guardar en caché si está habilitado
    if (config.useCache) {
      globalCache.set(url, response);
    }
    
    return response;
  }

  /**
   * Realiza una petición POST
   * @param url URL completa para la petición
   * @param data Datos a enviar en el cuerpo de la petición
   * @param customConfig Configuración específica para esta petición
   * @returns Promesa con la respuesta deserializada
   */
  static async post<T>(url: string, data: any, customConfig?: Partial<HttpClientConfig>): Promise<T> {
    const config = { ...HttpClient.config, ...customConfig };
    
    // Obtener el token CSRF para incluirlo en la petición
    const csrfToken = getCSRFToken();
    const headers = {
      ...defaultFetchOptions.headers,
      // Django busca el token CSRF en X-CSRFToken
      'X-CSRFToken': csrfToken || '',
    };
    
    console.log(`Enviando petición POST a ${url} con token CSRF: ${csrfToken ? 'Presente' : 'No encontrado'}`);
    
    return HttpClient.fetchWithRetry<T>(url, {
      ...defaultFetchOptions,
      method: 'POST',
      headers,
      body: JSON.stringify(data),
      // Asegurarse de incluir credenciales para que las cookies se envíen
      credentials: 'include', 
    }, config);
  }
  
  /**
   * Realiza una petición PUT
   * @param url URL completa para la petición
   * @param data Datos a enviar en el cuerpo de la petición
   * @param customConfig Configuración específica para esta petición
   * @returns Promesa con la respuesta deserializada
   */
  static async put<T>(url: string, data: any, customConfig?: Partial<HttpClientConfig>): Promise<T> {
    const config = { ...HttpClient.config, ...customConfig };
    
    return HttpClient.fetchWithRetry<T>(url, {
      ...defaultFetchOptions,
      method: 'PUT',
      body: JSON.stringify(data),
    }, config);
  }
  
  /**
   * Realiza una petición DELETE
   * @param url URL completa para la petición
   * @param customConfig Configuración específica para esta petición
   * @returns Promesa con la respuesta deserializada
   */
  static async delete<T>(url: string, customConfig?: Partial<HttpClientConfig>): Promise<T> {
    const config = { ...HttpClient.config, ...customConfig };
    
    return HttpClient.fetchWithRetry<T>(url, {
      ...defaultFetchOptions,
      method: 'DELETE',
    }, config);
  }
  
  /**
   * Limpia la caché de peticiones
   */
  static clearCache(): void {
    globalCache.clear();
  }
}

/**
 * Determina el tipo de error basado en el código de estado HTTP
 */
function getErrorTypeFromStatus(status: number): HttpErrorType {
  if (status >= 500) return HttpErrorType.SERVER;
  if (status === 404) return HttpErrorType.NOT_FOUND;
  if (status === 401 || status === 403) return HttpErrorType.AUTH;
  if (status === 422 || status === 400) return HttpErrorType.VALIDATION;
  return HttpErrorType.UNKNOWN;
}
