import type { Version, CartaPersonaje, CartaNegocio, CartaEspecial, CartaEvento, CartaObjetivo, BusinessIndustry, BusinessUpgrade } from '../models/types';
import { dynamicApiUrl, HttpClient } from '../utils/ApiConfig';

// Datos de muestra como fallback
import { sampleVersion } from './MockData';

/**
 * Servicio para manejar todas las operaciones relacionadas con las versiones
 * Sigue el principio de responsabilidad única enfocándose solo en la entidad Version
 */
export class VersionService {
  /**
   * Obtiene todas las versiones desde la API
   * @returns Promise con el array de versiones
   */
  static async getVersions(): Promise<Version[]> {
    try {
      return await HttpClient.get<Version[]>(dynamicApiUrl('versions'));
    } catch (error) {
      console.error("Error al obtener las versiones:", error);
      // Si hay un error, devolver los datos de muestra como fallback
      return [sampleVersion];
    }
  }

  /**
   * Obtiene las cartas de personaje de una versión específica
   * @param versionId ID de la versión
   * @returns Promise con el array de cartas de personaje
   */
  static async getCartasPersonaje(versionId: string | number | null): Promise<CartaPersonaje[]> {
    try {
      const endpoint = versionId 
        ? `personajes?version=${versionId}` 
        : 'personajes';
      
      return await HttpClient.get<CartaPersonaje[]>(dynamicApiUrl(endpoint));
    } catch (error) {
      console.error("Error al obtener cartas de personaje:", error);
      return [];
    }
  }

  /**
   * Obtiene las cartas de negocio de una versión específica
   * @param versionId ID de la versión
   * @returns Promise con el array de cartas de negocio
   */
  static async getCartasNegocio(versionId: string | number | null): Promise<CartaNegocio[]> {
    try {
      const endpoint = versionId 
        ? `negocios?version=${versionId}` 
        : 'negocios';
      
      return await HttpClient.get<CartaNegocio[]>(dynamicApiUrl(endpoint));
    } catch (error) {
      console.error("Error al obtener cartas de negocio:", error);
      return [];
    }
  }

  /**
   * Obtiene las cartas especiales de una versión específica
   * @param versionId ID de la versión
   * @returns Promise con el array de cartas especiales
   */
  static async getCartasEspeciales(versionId: string | number | null): Promise<CartaEspecial[]> {
    try {
      const endpoint = versionId 
        ? `especiales?version=${versionId}` 
        : 'especiales';
      
      return await HttpClient.get<CartaEspecial[]>(dynamicApiUrl(endpoint));
    } catch (error) {
      console.error("Error al obtener cartas especiales:", error);
      return [];
    }
  }

  /**
   * Obtiene las cartas de evento de una versión específica
   * @param versionId ID de la versión
   * @returns Promise con el array de cartas de evento
   */
  static async getCartasEvento(versionId: string | number | null): Promise<CartaEvento[]> {
    try {
      const endpoint = versionId 
        ? `eventos?version=${versionId}` 
        : 'eventos';
      
      return await HttpClient.get<CartaEvento[]>(dynamicApiUrl(endpoint));
    } catch (error) {
      console.error("Error al obtener cartas de evento:", error);
      return [];
    }
  }

  /**
   * Obtiene las cartas de objetivo de una versión específica
   * @param versionId ID de la versión
   * @returns Promise con el array de cartas de objetivo
   */
  static async getCartasObjetivo(versionId: string | number | null): Promise<CartaObjetivo[]> {
    try {
      const endpoint = versionId 
        ? `objetivos?version=${versionId}` 
        : 'objetivos';
      
      return await HttpClient.get<CartaObjetivo[]>(dynamicApiUrl(endpoint));
    } catch (error) {
      console.error("Error al obtener cartas de objetivo:", error);
      return [];
    }
  }

  /**
   * Obtiene todas las cartas de una versión específica
   * @param versionId ID de la versión
   * @returns Promise con un objeto que contiene todos los tipos de cartas
   */
  static async getAllCartas(versionId: string | number) {
    try {
      return await HttpClient.get(dynamicApiUrl(`versions/${versionId}/cards`));
    } catch (error) {
      console.error("Error al obtener todas las cartas:", error);
      return {
        personajes: [],
        negocios: [],
        especiales: [],
        eventos: [],
        objetivos: []
      };
    }
  }
}
