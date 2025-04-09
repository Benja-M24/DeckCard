import type { Participant, CartaPersonaje, CartaNegocio, CartaEspecial } from '../models/types';
import { dynamicApiUrl, HttpClient } from '../utils/ApiConfig';

/**
 * Servicio para manejar todas las operaciones relacionadas con los participantes
 * Sigue el principio de responsabilidad única enfocándose solo en la entidad Participant
 */
export class ParticipantService {
  /**
   * Obtiene todos los participantes de una sala específica
   * @param roomCode Código de la sala
   * @returns Promise con la lista de participantes
   */
  static async getParticipantsByRoom(roomCode: string): Promise<Participant[]> {
    try {
      const response = await HttpClient.get<{ success: boolean; participants: Participant[] }>(
        dynamicApiUrl(`participants?room=${roomCode}`)
      );
      return response.success ? response.participants : [];
    } catch (error) {
      console.error(`Error al obtener participantes de la sala ${roomCode}:`, error);
      return [];
    }
  }

  /**
   * Obtiene un participante por su ID
   * @param participantId ID del participante
   * @returns Promise con el participante o null si no existe
   */
  static async getParticipant(participantId: number): Promise<Participant | null> {
    try {
      const response = await HttpClient.get<{ success: boolean; participant: Participant }>(
        dynamicApiUrl(`participants/${participantId}`)
      );
      return response.success ? response.participant : null;
    } catch (error) {
      console.error(`Error al obtener el participante ${participantId}:`, error);
      return null;
    }
  }

  /**
   * Crea un nuevo participante en una sala
   * @param name Nombre del participante
   * @param roomCode Código de la sala (string, clave primaria)
   * @returns Promise con el participante creado
   */
  static async createParticipant(name: string, roomCode: string): Promise<Participant> {
    try {
      // Obtener user agent del navegador para la identificación
      const userAgent = typeof navigator !== 'undefined' ? navigator.userAgent : 'Unknown';
      
      // Enviar todos los campos requeridos por el backend
      const response = await HttpClient.post<{ success: boolean; participant: Participant }>(
        dynamicApiUrl('participants'),
        {
          name: name,
          room: roomCode,    // Enviamos el código (string) que es la clave primaria
          admin: false,
          // Valores iniciales para los campos requeridos
          dinero: 1500,  // Dinero inicial
          karma: 0,      // Karma inicial
          fama: 0,       // Fama inicial
          userAgent: userAgent // Identificador del dispositivo
        }
      );

      if (!response.success) {
        throw new Error('Error al crear el participante');
      }

      return response.participant;
    } catch (error) {
      console.error("Error al crear el participante:", error);
      throw error;
    }
  }

  /**
   * Asigna una carta de personaje a un participante
   * @param participantId ID del participante
   * @param cartaPersonajeId ID de la carta de personaje
   * @returns Promise con el participante actualizado
   */
  static async assignCharacterCard(
    participantId: number,
    cartaPersonajeId: number
  ): Promise<Participant> {
    try {
      const response = await HttpClient.post<{ success: boolean; participant: Participant }>(
        dynamicApiUrl(`participants/${participantId}/assign-character`),
        { carta_personaje_id: cartaPersonajeId }
      );

      if (!response.success) {
        throw new Error('Error al asignar la carta de personaje');
      }

      return response.participant;
    } catch (error) {
      console.error("Error al asignar la carta de personaje:", error);
      throw error;
    }
  }

  /**
   * Asigna una carta de negocio a un participante
   * @param participantId ID del participante
   * @param cartaNegocioId ID de la carta de negocio
   * @returns Promise con el participante actualizado
   */
  static async assignBusinessCard(
    participantId: number,
    cartaNegocioId: number
  ): Promise<Participant> {
    try {
      const response = await HttpClient.post<{ success: boolean; participant: Participant }>(
        dynamicApiUrl(`participants/${participantId}/assign-business`),
        { carta_negocio_id: cartaNegocioId }
      );

      if (!response.success) {
        throw new Error('Error al asignar la carta de negocio');
      }

      return response.participant;
    } catch (error) {
      console.error("Error al asignar la carta de negocio:", error);
      throw error;
    }
  }

  /**
   * Obtiene el participante actual almacenado en localStorage (si existe)
   * @returns ID del participante o null
   */
  static getCurrentParticipantId(): number | null {
    if (typeof window === 'undefined') return null;
    const id = localStorage.getItem('currentParticipant');
    return id ? parseInt(id, 10) : null;
  }

  /**
   * Guarda el ID del participante actual en localStorage
   * @param participantId ID del participante
   */
  static setCurrentParticipantId(participantId: number): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('currentParticipant', participantId.toString());
  }

  /**
   * Elimina el ID del participante actual de localStorage
   */
  static clearCurrentParticipantId(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('currentParticipant');
  }
}
