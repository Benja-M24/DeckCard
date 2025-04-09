import type { Version, Participant, CartaPersonaje, CartaNegocio, CartaEspecial, CartaObjetivo, CartaEvento, Room, BusinessIndustry, BusinessUpgrade } from '../models/types';

// Datos de muestra como fallback para versiones
export const sampleVersion: Version = {
  id: 1,
  nombre: "Versión de Prueba",
  version: "1.0",
  fecha_creacion: "2025-03-27",
};

// Datos de muestra como fallback para cartas de personaje
export const sampleCartaPersonaje: CartaPersonaje = {
  id: 1,
  nombre: "Personaje de Prueba",
  descripcion: "Un personaje para pruebas",
  historia: "Historia de prueba",
  imagen: "/assets/default-character.png",
  dinero: 1000,
  karma: 50,
  fama: 50,
  consignas_juego: ["Consigna 1", "Consigna 2"],
  version: 1,
};

// Datos de muestra como fallback para participantes
export const sampleAdminParticipant: Participant = {
  id: 1,
  name: "Admin",
  admin: true,
  room: null,
  carta_personaje: null,
  cartas_negocios: [],
  cartas_especiales: [],
  dinero: 0,
  karma: 0,
  fama: 0,
};

export const sampleParticipant: Participant = {
  id: 2,
  name: "Jugador",
  admin: false,
  room: null,
  carta_personaje: null,
  cartas_negocios: [],
  cartas_especiales: [],
  dinero: 0,
  karma: 0,
  fama: 0,
};

// Datos de muestra para industrias de negocio
export const sampleBusinessIndustry: BusinessIndustry = {
  id: 1,
  industry_name: "Restaurante"
};

// Datos de muestra para mejoras de negocio
export const sampleBusinessUpgrade: BusinessUpgrade = {
  id: 1,
  upgrade_name: "Mejora básica",
  n_wachines_necesarios: 2,
  costo_mejora: 1000,
  version: 1
};

// Datos de muestra como fallback para cartas de negocio
export const sampleCartaNegocio: CartaNegocio = {
  id: 1,
  nombre: "Negocio de Prueba",
  frase: "Un negocio para pruebas",
  precio: 5000,
  business_class_name: "Bronze",
  business_industry: sampleBusinessIndustry,
  business_upgrade: [sampleBusinessUpgrade],
  beneficio_base: 1000,
  beneficio_mejorado: 1500,
  consignas_juego: ["Consigna 1", "Consigna 2"],
  version: 1
};

// Datos de muestra como fallback para cartas especiales
export const sampleCartaEspecial: CartaEspecial = {
  id: 1,
  titulo: "Carta Especial de Prueba",
  frase: "Una carta especial para pruebas",
  descripcion: "Descripción de la carta especial de prueba", // Ahora es un campo opcional
  efecto: "Efecto de prueba", // Ahora es un campo opcional
  consignas_juego: ["Consigna 1", "Consigna 2"],
  imagen: "/assets/default-special.png",
  version: 1,
};

// Datos de muestra como fallback para cartas de objetivo
export const sampleCartaObjetivo: CartaObjetivo = {
  id: 1,
  titulo: "Objetivo de Prueba",
  objetivo: "Completar todas las tareas", // Ahora es un campo opcional
  consignas_juego: "Consiga 3 negocios y complete el nivel 2", // Es string, no array
  imagen: "/assets/default-objective.png",
  version: 1,
};

// Datos de muestra como fallback para cartas de evento
export const sampleCartaEvento: CartaEvento = {
  id: 1,
  titulo: "Evento de Prueba",
  frase: "Un evento inesperado",
  tipo_evento: "económico", // Ahora es un campo opcional
  consignas_juego: ["Pierda $1000", "Gane 5 puntos de karma"],
  imagen: "/assets/default-event.png",
  version: 1,
};

// Datos de muestra como fallback para salas
export const sampleRoom: Room = {
  code: "000ABC",
  name: "Sala de Prueba",
  version: sampleVersion, // Ahora es de tipo Version | number
  status: "created",
  fecha_creacion: "2025-03-27",
  max_participants: 6,
  participants: [sampleAdminParticipant],
};
