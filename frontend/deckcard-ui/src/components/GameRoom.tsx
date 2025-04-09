/**
 * Componente interactivo para la gestión de salas de juego
 * Utiliza el patrón Islands de Astro con client:load para interactividad inmediata
 */
import { useStore } from '@nanostores/react';
import { useEffect, useState } from 'react';
import { gameRoomStore, gameRoomActions } from '../stores/gameRoomStore';
import type { Room, Participant } from '../models/types';
import { ApiService } from '../utils/ApiService';

interface GameRoomProps {
  initialRoom?: Room | null;
  initialParticipant?: Participant | null;
}

export default function GameRoom({ initialRoom, initialParticipant }: GameRoomProps) {
  const gameRoom = useStore(gameRoomStore);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roomCode, setRoomCode] = useState('');
  const [playerName, setPlayerName] = useState('');

  // Inicializar el store con los valores iniciales si existen
  useEffect(() => {
    if (initialRoom) {
      gameRoomActions.setRoom(initialRoom);
    }
    if (initialParticipant) {
      gameRoomActions.setParticipant(initialParticipant);
    }
  }, [initialRoom, initialParticipant]);

  // Función para crear una nueva sala
  const createRoom = async () => {
    if (!playerName) {
      setError('Por favor, ingresa tu nombre para crear una sala');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      // Crear la sala y luego unirse como administrador
      const room = await ApiService.createRoom();
      
      if (room) {
        // Unirse como admin a la sala recién creada
        const participant = await ApiService.joinRoom({
          room_id: room.id,
          name: playerName,
          admin: true
        });
        
        // Actualizar el store con los nuevos datos
        gameRoomActions.setRoom(room);
        gameRoomActions.setParticipant(participant);
        
        // Redirigir a la página de la sala
        window.location.href = `/room/${room.code}`;
      }
    } catch (err) {
      setError('Error al crear la sala. Por favor intenta nuevamente.');
      console.error('Error creating room:', err);
    } finally {
      setLoading(false);
    }
  };

  // Función para unirse a una sala existente
  const joinRoom = async () => {
    if (!playerName || !roomCode) {
      setError('Por favor, completa todos los campos para unirte a una sala');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      // Buscar la sala por código
      const room = await ApiService.getRoomByCode(roomCode);
      
      if (room) {
        // Unirse como participante normal a la sala existente
        const participant = await ApiService.joinRoom({
          room_id: room.id,
          name: playerName,
          admin: false
        });
        
        // Actualizar el store con los nuevos datos
        gameRoomActions.setRoom(room);
        gameRoomActions.setParticipant(participant);
        
        // Redirigir a la página de la sala
        window.location.href = `/room/${room.code}`;
      } else {
        setError('No se encontró la sala con el código proporcionado');
      }
    } catch (err) {
      setError('Error al unirse a la sala. Por favor verifica el código e intenta nuevamente.');
      console.error('Error joining room:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="playerName">
            Tu nombre
          </label>
          <input
            id="playerName"
            type="text"
            placeholder="Ingresa tu nombre"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        
        <div className="flex flex-col space-y-4">
          <button
            onClick={createRoom}
            disabled={loading}
            className="bg-amber-500 hover:bg-amber-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            {loading ? 'Creando...' : 'Crear nueva sala'}
          </button>
          
          <div className="text-center font-bold text-gray-700 my-2">O</div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="roomCode">
              Código de sala
            </label>
            <input
              id="roomCode"
              type="text"
              placeholder="Ingresa el código de la sala"
              value={roomCode}
              onChange={(e) => setRoomCode(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>
          
          <button
            onClick={joinRoom}
            disabled={loading}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            {loading ? 'Uniéndose...' : 'Unirse a sala'}
          </button>
        </div>
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
