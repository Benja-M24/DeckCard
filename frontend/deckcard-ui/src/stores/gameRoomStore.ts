/**
 * Store para gestionar el estado global del juego utilizando nanostores
 * Este enfoque sigue el patrón de gestión de estado para componentes interactivos
 * alineado con la arquitectura API-first
 */

import { atom } from 'nanostores';
import type { Room as RoomType, Participant as ParticipantType } from '../models/types';

// Definición del estado global de una sala de juego
export interface GameRoomState {
  room: RoomType | null;
  participant: ParticipantType | null;
  loading?: boolean;
  error?: string | null;
}

// Estado inicial
const initialState: GameRoomState = {
  room: null,
  participant: null,
  loading: false,
  error: null
};

// Creación del store utilizando atom de nanostores
export const gameRoomStore = atom<GameRoomState>(initialState);

// Acciones para manipular el estado
export const gameRoomActions = {
  setRoom: (room: RoomType | null) => {
    const currentState = gameRoomStore.get();
    gameRoomStore.set({
      ...currentState,
      room
    });
  },

  setParticipant: (participant: ParticipantType | null) => {
    const currentState = gameRoomStore.get();
    gameRoomStore.set({
      ...currentState,
      participant
    });
  },

  setLoading: (loading: boolean) => {
    const currentState = gameRoomStore.get();
    gameRoomStore.set({
      ...currentState,
      loading
    });
  },

  setError: (error: string | null) => {
    const currentState = gameRoomStore.get();
    gameRoomStore.set({
      ...currentState,
      error
    });
  },

  clearRoom: () => {
    gameRoomStore.set(initialState);
  }
};
