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

export interface Room {
  code: string;
  name: string;
  mazo: Mazo;
  status: string;
  fecha_creacion: string;
  participants: Participant[];
  max_participants: number;
}

export interface Participant {
  id: number;
  name: string;
  admin: boolean;
  room: Room | null;
  carta_personaje: CartaPersonaje | null;
  cartas_negocios: CartaNegocio[] | null;
  cartas_especiales: CartaEspecial[] | null;
  dinero: number | null;
  karma: number | null;
  fama: number | null;
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


export const sampleParticipant: Participant = {
  id: 1,
  name: "Jugador 1",
  admin: false,
  room: null,
  carta_personaje: null,
  cartas_negocios: null,
  cartas_especiales: null,
  dinero: 1000,
  karma: 500,
  fama: 300,
};

export const sampleAdminParticipant: Participant = {
  id: 1,
  name: "Jugador 1",
  admin: true,
  room: null,
  carta_personaje: null,
  cartas_negocios: null,
  cartas_especiales: null,
  dinero: 1000,
  karma: 500,
  fama: 300,
};

export const sampleRoom: Room = {
  code: "000ABC",
  name: "Sala de Prueba",
  mazo: sampleMazo,
  status: "created",
  fecha_creacion: "2024-03-17",
  max_participants: 6,
  participants: [sampleAdminParticipant],
};

// Función para obtener los mazos desde la API
export async function getMazosFromAPI(): Promise<Mazo[]> {
  try {
    const response = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/mazos/`);
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
    let url = `${import.meta.env.PUBLIC_API_URL}/api/personajes/`;
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
    let url = `${import.meta.env.PUBLIC_API_URL}/api/negocios/`;
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
    let url = `${import.meta.env.PUBLIC_API_URL}/api/especiales/`;
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

export async function getRoomsFromAPI(): Promise<Room[] | null> {
  try {
    const response = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/rooms`);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error al obtener las salas:", error);
    return null;
  }
}

export async function getRoomFromAPI(roomId: string | null): Promise<Room | null> {
  try {
    const url = `${import.meta.env.PUBLIC_API_URL}/api/rooms/${roomId}`;
    console.log(`Fetching room from URL: ${url}`);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const roomData = await response.json();
    console.log("Room data received:", roomData);
    return roomData.Room;
  } catch (error) {
    console.error("Error al obtener la sala:", error);
    return null;
  }
}

export async function joinRoomFromAPI(roomId: string, playerName: string): Promise<Participant | null> {
  try {
    const url = `${import.meta.env.PUBLIC_API_URL}/api/rooms/${roomId}`;
    console.log(`Checking room at URL: ${url}`);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    // Verificar si la respuesta contiene datos de la sala
    const roomData = await response.json();
    console.log("Room data for join:", roomData);

    if (!roomData || !roomData.room) {
      console.error("Datos de sala inválidos:", roomData);
      throw new Error("Datos de sala inválidos");
    }

    // Datos adicionales opcionales
    const userAgent = navigator.userAgent;
    const connectionTime = new Date().toISOString();
    // Agregar el participante a la sala
    const participantUrl = `${import.meta.env.PUBLIC_API_URL}/api/rooms/${roomId}/participants`;
    console.log(`Adding participant at URL: ${participantUrl}`);

    // Preparar datos para la solicitud
    const participantData = {
      name: playerName,
      admin: false,
      room: roomData.room,
      userAgent: userAgent,
    };

    console.log("Enviando datos del participante:", participantData);

    const joinResponse = await fetch(participantUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(participantData),
    });

    if (!joinResponse.ok) {
      console.error(`Error al agregar participante: ${joinResponse.status}`);
      const errorText = await joinResponse.text();
      console.error("Detalles del error:", errorText);
      throw new Error(`Error al agregar participante: ${joinResponse.status}`);
    }

    const responseData = await joinResponse.json();
    console.log("Respuesta del servidor al crear participante:", responseData);

    if (responseData && responseData.participant) {
      return responseData.participant;
    } else {
      throw new Error("Formato de respuesta inesperado al crear participante");
    }

  } catch (error) {
    console.error("Error al unirse a la sala:", error);
    throw error; // Re-lanzamos el error para que la interfaz pueda manejarlo
  }
}

export async function createRoomOnAPI(
  name: string,
  adminName: string,
  mazoId: number,
  maxParticipants: number = 6
): Promise<Room> {
  try {
    const response = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/rooms/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        admin_name: adminName,
        mazo: mazoId,
        max_participants: maxParticipants
      }),
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const data = await response.json();
    return data.room;
  } catch (error) {
    console.error("Error al crear la sala:", error);
    return sampleRoom;
  }
}

export async function createParticipantOnAPI(roomId: string | null): Promise<Participant> {
  try {
    const response = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/rooms/${roomId}/participants`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error al crear el participante:", error);
    return sampleParticipant;
  }
}

export async function getParticipantsFromAPI(roomId: string | null): Promise<Participant[]> {
  try {
    const response = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/rooms/${roomId}/participants`);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error al obtener los participantes:", error);
    return [sampleParticipant];
  }
}