/**
 * Servicio principal de API que actúa como fachada
 * Implementa el patrón Facade para simplificar el acceso a los servicios específicos
 * Sigue el principio de inversión de dependencias al depender de abstracciones (interfaces)
 */

// Importar los tipos desde el módulo centralizado
import type {
  Version,
  CartaPersonaje,
  CartaNegocio,
  CartaEspecial,
  CartaEvento,
  CartaObjetivo,
  Room,
  Participant,
  ApiResponse,
  BusinessIndustry,
  BusinessUpgrade
} from '../models/types';

// Importar los servicios específicos
import { VersionService } from '../services/VersionService';
import { RoomService } from '../services/RoomService';
import { ParticipantService } from '../services/ParticipantService';

// Importar utilidades para las peticiones HTTP
import { dynamicApiUrl, HttpClient } from './ApiConfig';

// Importar datos de muestra como fallback
import {
  sampleVersion,
  sampleCartaPersonaje,
  sampleCartaNegocio,
  sampleCartaEspecial,
  sampleRoom,
  sampleParticipant
} from '../services/MockData';

/**
 * Clase principal de servicios de API que integra todos los servicios específicos
 * Proporciona una interfaz unificada para acceder a todas las funcionalidades de la API
 */
export class ApiService {
  // Servicios de Versión
  static getVersions(): Promise<Version[]> {
    return VersionService.getVersions();
  }

  static getCartasPersonaje(versionId: string | number | null): Promise<CartaPersonaje[]> {
    return VersionService.getCartasPersonaje(versionId);
  }

  static getCartasNegocio(versionId: string | number | null): Promise<CartaNegocio[]> {
    return VersionService.getCartasNegocio(versionId);
  }

  static getCartasEspeciales(versionId: string | number | null): Promise<CartaEspecial[]> {
    return VersionService.getCartasEspeciales(versionId);
  }

  static getCartasEvento(versionId: string | number | null): Promise<CartaEvento[]> {
    return VersionService.getCartasEvento(versionId);
  }

  static getCartasObjetivo(versionId: string | number | null): Promise<CartaObjetivo[]> {
    return VersionService.getCartasObjetivo(versionId);
  }

  static getAllCartas(versionId: string | number) {
    return VersionService.getAllCartas(versionId);
  }

  // Servicios de Room
  static getRooms(): Promise<Room[]> {
    return RoomService.getRooms();
  }

  static getRoom(roomId: string): Promise<Room | null> {
    return RoomService.getRoom(roomId);
  }

  static createRoom(
    adminName: string,
    roomName: string,
    versionId: number,
    maxParticipants: number = 6
  ): Promise<Room> {
    return RoomService.createRoom(adminName, roomName, versionId, maxParticipants);
  }

  static getCurrentRoomId(): string | null {
    return RoomService.getCurrentRoomId();
  }

  static setCurrentRoomId(roomId: string): void {
    RoomService.setCurrentRoomId(roomId);
  }

  static clearCurrentRoomId(): void {
    RoomService.clearCurrentRoomId();
  }

  // Servicios de Participant
  static getParticipantsByRoom(roomCode: string): Promise<Participant[]> {
    return ParticipantService.getParticipantsByRoom(roomCode);
  }

  static getParticipant(participantId: number): Promise<Participant | null> {
    return ParticipantService.getParticipant(participantId);
  }

  static createParticipant(name: string, roomCode: string): Promise<Participant> {
    return ParticipantService.createParticipant(name, roomCode);
  }

  static assignCharacterCard(
    participantId: number,
    cartaPersonajeId: number
  ): Promise<Participant> {
    return ParticipantService.assignCharacterCard(participantId, cartaPersonajeId);
  }

  static assignBusinessCard(
    participantId: number,
    cartaNegocioId: number
  ): Promise<Participant> {
    return ParticipantService.assignBusinessCard(participantId, cartaNegocioId);
  }

  static getCurrentParticipantId(): number | null {
    return ParticipantService.getCurrentParticipantId();
  }

  static setCurrentParticipantId(participantId: number): void {
    ParticipantService.setCurrentParticipantId(participantId);
  }

  static clearCurrentParticipantId(): void {
    ParticipantService.clearCurrentParticipantId();
  }
}

// Función para obtener las cartas de personaje desde la API según la versión seleccionada
export async function getCartasPersonajeFromAPI(versionId: string | null): Promise<CartaPersonaje[]> {
  try {
    // Construir la URL dependiendo de si hay una versión seleccionada
    const url = dynamicApiUrl(`personajes/?version=${versionId}`);

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
export async function getCartasNegocioFromAPI(versionId: string | null): Promise<CartaNegocio[]> {
  try {
    const url = dynamicApiUrl(`negocios/?version=${versionId}`)

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
export async function getCartasEspecialesFromAPI(versionId: string | null): Promise<CartaEspecial[]> {
  try {
    const url = dynamicApiUrl(`especiales/?version=${versionId}`);
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
    const response = await fetch(dynamicApiUrl('rooms'));
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const roomList: Room[] = await response.json();
    return roomList;
  } catch (error) {
    console.error("Error al obtener las salas:", error);
    return null;
  }
}

export async function getRoomFromAPI(roomId: string | null): Promise<Room | null> {
  try {
    const url = dynamicApiUrl(`rooms/${roomId}`);
    console.log(`Fetching room from URL: ${url}`);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const roomData: Room = await response.json();
    console.log("Room data received:", roomData);
    return roomData;
  } catch (error) {
    console.error("Error al obtener la sala:", error);
    return null;
  }
}

export async function joinRoomFromAPI(roomId: string, playerName: string): Promise<Participant | null> {
  const normalizedRoomId = roomId.trim().toUpperCase();
  try {
    const currentRoom: Room | null = await getRoomFromAPI(normalizedRoomId);

    // Verificar si la respuesta tiene la estructura esperada
    if (!currentRoom) {
      console.error("Datos de sala inválidos:", currentRoom);
      throw new Error("Datos de sala inválidos o formato inesperado");
    }
    // sessionStorage.setItem(
    //   "currentParticipantId",
    //   currentParticipant.id.toString(),
    // );
    sessionStorage.setItem(
      "currentRoom",
      JSON.stringify(currentRoom),
    );
    // Datos adicionales opcionales
    const userAgent = navigator.userAgent;
    const connectionTime = new Date().toISOString();
    // Agregar el participante a la sala
    const participantUrl = dynamicApiUrl(`rooms/${roomId}/participants`);
    console.log(`Adding participant at URL: ${participantUrl}`);

    // Preparar datos para la solicitud
    const participantData = {
      name: playerName,
      // Note: admin is handled by the backend and set to false by default
      // Note: room is already known from the URL path
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
      let errorMessage = `Error al agregar participante: ${joinResponse.status}`;
      throw new Error(errorMessage);
    }

    const responseData: Participant = await joinResponse.json();
    console.log("Respuesta del servidor al crear participante:", responseData);

    if (responseData) {
      return responseData;
    } else {
      throw new Error("Formato de respuesta inesperado al crear participante");
    }

  } catch (error) {
    console.error("Error al unirse a la sala:", error);
    // Asegurarnos de devolver un Error con mensaje en lugar de re-lanzar directamente
    if (error instanceof Error) {
      throw new Error(error.message || "Error desconocido al unirse a la sala");
    } else {
      throw new Error("Error desconocido al unirse a la sala");
    }
  }
}

// Función para obtener versiones desde la API
export async function getVersionsFromAPI(): Promise<Version[]> {
  try {
    const url = dynamicApiUrl('versions');
    console.log(`Fetching versions from URL: ${url}`);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const versions = await response.json();
    console.log("Versions data received:", versions);
    return versions;
  } catch (error) {
    console.error("Error al obtener las versiones:", error);
    return [sampleVersion];
  }
}

export async function createRoomOnAPI(
  adminName: string,
  roomName: string,
  versionId: number,
  maxParticipants: number = 6
): Promise<Room> {
  try {
    const response = await fetch(dynamicApiUrl('rooms'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: roomName,
        admin_name: adminName,
        version: versionId,
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
    throw error;
  }
}

export async function createParticipantOnAPI(roomId: string | null): Promise<Participant> {
  try {
    const response = await fetch(dynamicApiUrl(`rooms/${roomId}/participants`), {
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
    throw new Error("Error al crear el participante");
  }
}

export async function getCurrentParticipantFromAPI(): Promise<Participant | null> {
  try {
    if (!sessionStorage.getItem("currentRoomId") || !sessionStorage.getItem("currentParticipantId")) {
      return null;
    }
    const response = await fetch(dynamicApiUrl(`rooms/${sessionStorage.getItem("currentRoomId")}/participants/${sessionStorage.getItem("currentParticipantId")}`));
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const participant: Participant = await response.json();
    return participant;
  } catch (error) {
    console.error("Error al obtener el participante:", error);
    return null;
  }
}

export async function getCurrentRoomIdFromAPI(): Promise<Room> {
  try {
    const response = await fetch(dynamicApiUrl(`rooms/${sessionStorage.getItem("currentRoomId")}`));
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const room: Room = await response.json();
    return room;
  } catch (error) {
    console.error("Error al obtener la sala actual:", error);
    return sampleRoom;
  }
}

export async function getParticipantsFromAPI(roomId: string | null): Promise<Participant[]> {
  try {
    if (!roomId) {
      throw new Error("No se proporciona un ID de sala");
    }
    const response = await fetch(dynamicApiUrl(`rooms/${roomId}/participants`));
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const participants: Participant[] = await response.json();
    return participants;
  } catch (error) {
    console.error("Error al obtener los participantes:", error);
    return [sampleParticipant];
  }
}