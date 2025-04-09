import type { Room, Participant } from '../models/types';
import { dynamicApiUrl, HttpClient } from '../utils/ApiConfig';
import { sampleAdminParticipant, sampleVersion } from './MockData';

// Datos de muestra como fallback
export const sampleRoom: Room = {
  code: "000ABC",
  name: "Sala de Prueba",
  version: sampleVersion.id, // Using Version ID as required by Room interface
  status: "created",
  fecha_creacion: "2025-03-27",
  max_participants: 6,
  participants: [sampleAdminParticipant],
};

/**
 * Servicio para manejar todas las operaciones relacionadas con las salas
 * Sigue el principio de responsabilidad única enfocándose solo en la entidad Room
 */
export class RoomService {
  /**
   * Obtiene todas las salas disponibles
   * @returns Promise con la lista de salas
   */
  static async getRooms(): Promise<Room[]> {
    try {
      const response = await HttpClient.get<{ success: boolean; rooms: Room[] }>(dynamicApiUrl('rooms'));
      return response.success ? response.rooms : [];
    } catch (error) {
      console.error("Error al obtener las salas:", error);
      return [];
    }
  }

  /**
   * Obtiene una sala específica por su código
   * @param roomId Código único de la sala
   * @returns Promise con la sala o null si no existe
   */
  static async getRoom(roomId: string): Promise<Room | null> {
    try {
      const response = await HttpClient.get<{ success: boolean; room: Room }>(dynamicApiUrl(`rooms/${roomId}`));
      return response.success ? response.room : null;
    } catch (error) {
      console.error(`Error al obtener la sala ${roomId}:`, error);
      return null;
    }
  }

  /**
   * Crea una nueva sala con un administrador
   * @param adminName Nombre del administrador
   * @param roomName Nombre de la sala
   * @param versionId ID de la versión a utilizar
   * @param maxParticipants Número máximo de participantes (por defecto 6)
   * @returns Promise con la sala creada
   */
  static async createRoom(
    adminName: string,
    roomName: string,
    versionId: number,
    maxParticipants: number = 6
  ): Promise<Room> {
    try {
      const response = await HttpClient.post<{ success: boolean; room: Room }>(
        dynamicApiUrl('rooms'),
        {
          name: roomName,
          admin_name: adminName,
          version: versionId,
          max_participants: maxParticipants
        }
      );

      if (!response.success) {
        throw new Error('Error al crear la sala');
      }

      return response.room;
    } catch (error) {
      console.error("Error al crear la sala:", error);
      throw error;
    }
  }

  /**
   * Obtiene la sala actual almacenada en localStorage (si existe)
   * @returns Código de la sala o null
   */
  static getCurrentRoomId(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('currentRoom');
  }

  /**
   * Guarda el código de la sala actual en localStorage
   * @param roomId Código de la sala
   */
  static setCurrentRoomId(roomId: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('currentRoom', roomId);
  }

  /**
   * Elimina el código de la sala actual de localStorage
   */
  static clearCurrentRoomId(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('currentRoom');
  }
}
