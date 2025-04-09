/**
 * TypeScript interfaces for the DeckCard project models
 * Aligned with Django backend models and serializers
 */

// Base interfaces
export interface Version {
  id: number;
  nombre: string;
  version: string;
  fecha_creacion: string;
}

// Business model interfaces (renamed from NivelDeNegocio/TipoDeNegocio)
export interface BusinessIndustry {
  id: number;
  industry_name: string; // Renamed from 'nombre'
}

export interface BusinessUpgrade {
  id: number;
  upgrade_name: string; // Renamed from 'n_nivel'
  n_wachines_necesarios: number;
  costo_mejora: number;
  version: number;
}

// Type aliases for type guards in components
export type CartaPersonajeType = {
  id: number;
  nombre: string;
  descripcion: string;
  historia: string;
  imagen: string;
  dinero: number;
  karma: number;
  fama: number;
  consignas_juego: string[];
  version: number;
};

export type CartaNegocioType = {
  id: number;
  nombre: string;
  frase: string;
  precio: number;
  tipo: string; // Used in type guard (legacy property)
  business_class_name: string; 
  business_industry: BusinessIndustry;
  business_industry_name?: string;
  business_upgrade: BusinessUpgrade[];
  beneficio_base: number;
  beneficio_mejorado: number;
  consignas_juego: string[];
  version: number;
};

export type CartaEspecialType = {
  id: number;
  titulo: string;
  frase: string;
  descripcion?: string;
  efecto?: string;
  consignas_juego: string[];
  imagen: string;
  version: number;
};

// Card interfaces based on Django models
export interface CartaPersonaje extends CartaPersonajeType {}

export interface CartaNegocio {
  id: number;
  nombre: string;
  frase: string;
  precio: number;
  tipo?: string; // Legacy field for compatibility with type guards
  business_class_name: string; // New structure for business class
  business_industry: BusinessIndustry;
  business_industry_name?: string; // ReadOnlyField from serializer
  business_upgrade: BusinessUpgrade[];
  beneficio_base: number;
  beneficio_mejorado: number;
  beneficio_final?: number; // Para compatibilidad con versiones anteriores
  niveles_soportados?: string[]; // Para compatibilidad con versiones anteriores
  consignas_juego: string[];
  version: number;
}

export interface CartaEspecial extends CartaEspecialType {}

export interface CartaEvento {
  id: number;
  titulo: string;
  frase: string;
  tipo_evento?: string;
  consignas_juego: string[];
  imagen: string;
  version: number;
}

export interface CartaObjetivo {
  id: number;
  titulo: string;
  objetivo?: string;
  consignas_juego: string; // TextField in Django, not JSONField
  imagen: string;
  version: number;
}

// Game session interfaces
export interface Participant {
  id: number;
  name: string;
  admin: boolean;
  dinero: number | null;
  karma: number | null;
  fama: number | null;
  userAgent?: Record<string, any>;
  room: string | null;
  carta_personaje: CartaPersonaje | null;
  cartas_negocios: CartaNegocio[] | null;
  cartas_especiales: CartaEspecial[] | null;
}

export interface Room {
  code: string;    // Código de la sala (clave primaria en la base de datos)
  name: string;
  version: Version | number; // ID de la versión o objeto Version completo
  status: 'created' | 'waiting' | 'in_progress' | 'finished';
  fecha_creacion: string;
  participants: Participant[];
  max_participants: number;
}

// API response types
export interface ApiError {
  success: false;
  error: string;
  errors?: Record<string, string[]>;
}

export interface ApiSuccess<T> {
  success: true;
  data: T;
}

export type ApiResponse<T> = ApiSuccess<T> | ApiError;
