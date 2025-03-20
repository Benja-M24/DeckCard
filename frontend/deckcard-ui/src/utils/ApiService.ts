// Servicio para manejar todas las llamadas a la API

// Interfaces para los tipos de datos
export interface Mazo {
  id: number;
  nombre: string;
  version: string;
  fecha_creacion: string;
}

export interface CartaPersonaje {
  id: number;
  nombre: string;
  descripcion: string;
  historia: string;
  imagen: string;
  dinero: number;
  karma: number;
  fama: number;
  consignas_juego: string[];
  mazo: number;
}

export interface CartaNegocio {
  id: number;
  nombre: string;
  frase: string;
  tipo: number;
  precio: number;
  beneficio_base: number;
  beneficio_final: number;
  consignas_juego: string[];
  niveles_soportados: number[];
  mazo: number;
}

export interface CartaEspecial {
  id: number;
  titulo: string;
  frase: string;
  consignas_juego: string[];
  imagen: string;
  mazo: number;
}

// Datos de muestra como fallback
export const sampleCartaPersonaje: CartaPersonaje = {
  id: 1,
  nombre: "Carlos Emprendedor",
  descripcion: "Visionario de negocios con gran carisma",
  historia: "Comenzó desde abajo y ahora es dueño de varios negocios en la ciudad",
  imagen: "/placeholder-character.jpg",
  dinero: 3600,
  karma: 700,
  fama: 500,
  consignas_juego: [
    "Comienza con +$500 extra",
    "Puede comprar un negocio extra por turno",
  ],
  mazo: 1,
};

export const sampleCartaNegocio: CartaNegocio = {
  id: 1,
  nombre: "Café Internet",
  frase: "Local de servicios digitales",
  tipo: 1,
  precio: 5000,
  beneficio_base: 5,
  beneficio_final: 8,
  consignas_juego: [
    "Cobras +2 por cada negocio tecnológico que poseas",
    "Puedes mejorar este negocio por $1000 menos",
  ],
  niveles_soportados: [1, 2, 3],
  mazo: 1,
};

export const sampleCartaEspecial: CartaEspecial = {
  id: 1,
  titulo: "Evento Inesperado",
  frase: "La fortuna favorece a los audaces",
  consignas_juego: [
    "Roba 2 cartas adicionales en tu próximo turno",
    "Puedes descartar esta carta para evitar un evento negativo",
  ],
  imagen: "/placeholder-special.jpg",
  mazo: 1,
};

export const sampleMazo: Mazo = {
  id: 1,
  nombre: "None",
  version: "0.0",
  fecha_creacion: "2024-03-17",
};

// Función para obtener los mazos desde la API
export async function getMazosFromAPI(): Promise<Mazo[]> {
  try {
    const response = await fetch(`${import.meta.env.API_URL}/api/mazos/`);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error al obtener los mazos:", error);
    // Si hay un error, devolver los datos de muestra como fallback
    return [sampleMazo];
  }
}

// Función para obtener las cartas de personaje desde la API según el mazo seleccionado
export async function getCartasPersonajeFromAPI(mazoId: string | null): Promise<CartaPersonaje[]> {
  try {
    // Construir la URL dependiendo de si hay un mazo seleccionado
    let url = `${import.meta.env.API_URL}/api/personajes/`;
    if (mazoId) {
      url += `?mazo=${mazoId}`;
    }

    console.log(`Fetching from URL: ${url}`);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const data = await response.json();
    console.log("API Response for cartas personaje:", data);
    console.log("Data length:", Array.isArray(data) ? data.length : "Not an array");

    return data;
  } catch (error) {
    console.error("Error al obtener las cartas de personaje:", error);
    // Si hay un error, devolver un dato de muestra como fallback
    return [sampleCartaPersonaje];
  }
}

// Función para obtener cartas de negocio
export async function getCartasNegocioFromAPI(mazoId: string | null): Promise<CartaNegocio[]> {
  try {
    let url = `${import.meta.env.API_URL}/api/negocios/`;
    if (mazoId) {
      url += `?mazo=${mazoId}`;
    }

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error al obtener las cartas de negocio:", error);
    return [sampleCartaNegocio];
  }
}

// Función para obtener cartas especiales
export async function getCartasEspecialesFromAPI(mazoId: string | null): Promise<CartaEspecial[]> {
  try {
    let url = `${import.meta.env.API_URL}/api/especiales/`;
    if (mazoId) {
      url += `?mazo=${mazoId}`;
    }

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error al obtener las cartas especiales:", error);
    return [sampleCartaEspecial];
  }
}
