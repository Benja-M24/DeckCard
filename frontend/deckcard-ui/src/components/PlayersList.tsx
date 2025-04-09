/**
 * Componente interactivo para mostrar y gestionar la lista de jugadores
 * Este componente utiliza client:load para tener interactividad inmediata
 */
import { useStore } from '@nanostores/react';
import { useState, useEffect } from 'react';
import { gameRoomStore } from '../stores/gameRoomStore';
import type { Participant } from '../models/types';

interface PlayersListProps {
  initialParticipants?: Participant[];
}

export default function PlayersList({ initialParticipants = [] }: PlayersListProps) {
  const { room } = useStore(gameRoomStore);
  const [participants, setParticipants] = useState<Participant[]>(initialParticipants);
  const [isUpdating, setIsUpdating] = useState(false);

  // Sincronizar con el store global cuando cambie
  useEffect(() => {
    if (room?.participants) {
      setParticipants(room.participants);
    }
  }, [room]);

  // Colores para los nombres de jugadores
  const colors = [
    "text-red-500", "text-blue-600", "text-green-600", 
    "text-purple-600", "text-amber-600", "text-indigo-600", "text-yellow-400"
  ];

  return (
    <div className="flex flex-col p-2 sm:w-1/2 h-full">
      <div className="flex justify-start mx-auto w-full h-full p-2 mb-6 border-1 border-gray-300 rounded-2xl shadow-sm">
        <ul className="flex flex-col w-full">
          {participants.length === 0 && (
            <li className="text-gray-400 text-center py-2">No hay jugadores conectados</li>
          )}
          
          {participants.map((participant, index) => (
            <li key={participant.id} className="flex flex-row items-center">
              <span className="inline-block h-2 w-2 rounded-full bg-green-600 animate-pulse mr-1"></span>
              <span className={`block text-md font-medium p-1 ${colors[index % colors.length]}`}>
                {participant.name}
                {participant.admin && (
                  <span className="ml-2 px-1 py-0.5 bg-amber-200 text-amber-800 text-xs rounded">
                    Admin
                  </span>
                )}
              </span>
            </li>
          ))}
        </ul>
      </div>
      
      {isUpdating && (
        <div className="absolute inset-0 bg-black bg-opacity-20 flex items-center justify-center">
          <div className="animate-spin h-8 w-8 border-4 border-amber-500 rounded-full border-t-transparent"></div>
        </div>
      )}
    </div>
  );
}
