# DeckCards
## Objetivo
Implementar funcionalidades del stack (Django, Django Rest Framework, Astro, TypeScript, Postgres, docker, traefik) en una aplicación web Sencilla para cualquier usuario pero robusta en su diseño de software siguiendo los principios SOLID.

## Aplicación
DeckCards is a card game platform with customizable game rooms where different players can join. In the room, the admin player can mix the cards and deal a variable number for each type to each player. Players can see their cards and CartaPersonaje (Character Cards) from other users' hands, but cannot see others. Upcoming cards from any type of deck card are hidden. Players can show a card when they use it.

### contenedores de docker
Traefik/dockercompose.yml
- traefik
Declares/dockercompose.yml
- frontend
- backend
- bd


#### Principios SOLID:

S - Single Responsibility: cada clase debe tener una única responsabilidad
O - Open/Closed: abierto para extensión, cerrado para modificación
L - Liskov Substitution: las subclases deben poder sustituir a sus clases base
I - Interface Segregation: muchas interfaces específicas son mejores que una general
D - Dependency Inversion: depender de abstracciones, no de implementaciones

### Funcionalidades

#### backend (python y django admin interface)
- Crear versiones
- Eliminar versión
- Renombrar versión
- Ver lista de versiones

- Añadir cartas al mazo
- Eliminar cartas del mazo
- Ver lista de cartas del mazo
- Editar cartas del mazo

- Mezclar mazos
- Repartir 'x' cartas del mazo a 'y' jugadores
- Tomar una nueva carta del mazo

#### Frontend
- Elegir versión
- Mezclar
- Tomar la siguiente carta
- Ver la carta en modo presentación
- Salir del modo presentación

### Tablas de la BD
- Versiones (ID, nombre, version, fecha automatica, DEFAULT_VERSION_ID)
- Cartas_negocios (ID, titulo, subtitulo, tipo, Costo, lista_De_niveles_Soportados, benefico_base = x - leng(nivles_Soportados), beneficio x turno en cada nivel= [a,b,c,d]) 
- Niveles_de_negocio (ID, n_Nivel, n_Wachines_necesarios, plus_De_Beneficio, )
- Cartas_Personajes (ID, Nombre, Historia, edad, sexo, imagen, Atributos_de_personaje)
- Atributos_de_personaje (ID, karma, dinero, fama, x)
- Cartas_Especiales (ID, Titulo, frase, consinga, imagen)

### Structure
#### Backend
- Cards
    - admin.py - Django admin interface customization
    - models.py - Database model definitions (Version, Cards, Room, Participant)
    - serializers.py - Data serialization for API responses
    - services.py - Business logic layer (VersionService, RoomService, ParticipantService)
    - views.py - Controller logic implementing REST API endpoints
    - urls.py - URL routing configuration
    - admin.py - Django admin interface customization
    - tests.py - Backend unit tests
  
#### Frontend
- services
    - VersionService.ts - Frontend service for deck operations
    - RoomService.ts - Frontend service for game room management
    - ParticipantService.ts - Frontend service for player interactions
- utils
    - ApiService.ts - Unified API client implementing Facade pattern
    - ApiConfig.ts - Configuration for API endpoints and HTTP requests

### BD Tables (Postgres)
#### Version
- id (PK)
- nombre
- version
- fecha_creacion
- DEFAULT_VERSION_ID (a class variable set to 3 for any new card creation)

#### CartaNegocio (Deck of Business Cards)
- id (PK)
- version (FK)
- nombre
- descripcion
- nivel_de_negocio
- tipo_de_negocio
- costo
- ingresos
- imagen

#### CartaPersonaje (Deck of Character Cards)
- id (PK)
- version (FK)
- nombre
- descripcion
- habilidad_especial
- karma_inicial
- fama_inicial
- dinero_inicial
- imagen

#### CartaEspecial (Deck of Special Cards)
- id (PK)
- version (FK)
- nombre
- descripcion
- tipo
- efecto
- imagen

#### CartaEvento (Deck of Event Cards)
- id (PK)
- version (FK)
- nombre
- descripcion
- efecto
- duracion
- imagen

#### CartaObjetivo (Deck of Objective Cards)
- id (PK)
- version (FK)
- nombre
- descripcion
- condicion
- recompensa
- imagen

#### Room
- code (PK)
- name
- version (FK)
- status
- fecha_creacion
- max_participants

#### Participant
- id (PK)
- name
- admin
- room (FK)
- carta_personaje (FK)
- cartas_negocios (M2M)
- cartas_especiales (M2M)
- dinero
- karma
- fama


### Current Features
#### Room Management
- Create rooms with unique codes
- Join existing rooms as participants
- Admin and player role management
- Configurable participant limits per room
- Room capacity validation

### Upcoming Features
#### Card Management
- Deal cards to participants
- Shuffle decks by type
- Draw new cards from the deck
- Use cards and reveal them to other players
- Discard cards from hand and draw replacements

#### Player Management
- Update player statistics (dinero, karma, fama)
- Turn-based gameplay (players click end turn, admin can force next turn)
- Apply card effects to player statistics

#### Security and Options
- Password-protected rooms
- Card visibility settings (private/public)

## Arquitectura Técnica: API-First con Astro Static Output

### Enfoque API-First

DeckCards implementa una arquitectura API-First, separando claramente las responsabilidades entre frontend y backend:

- **Backend (Django REST Framework)**: Concentra toda la lógica de negocio, validaciones, persistencia y seguridad.
- **Frontend (Astro)**: Enfocado en la presentación, interactividad y experiencia de usuario.

Este enfoque ofrece numerosas ventajas:

1. **Desacoplamiento**: Permite que frontend y backend evolucionen independientemente.
2. **Reutilización de API**: La misma API puede servir a múltiples clientes (web, móvil, etc.).
3. **Especialización de equipos**: Desarrolladores pueden enfocarse en sus áreas de experiencia.
4. **Testabilidad**: Facilita las pruebas automatizadas tanto en frontend como en backend.
5. **Escalabilidad**: Optimiza los recursos al escalar componentes por separado según necesidades.

### Astro con output: 'static'

Utilizamos Astro configurado con `output: 'static'` para generar un sitio estático que ofrece:

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'static',
  integrations: [tailwind()],
  devToolbar: {
    enabled: false
  }
});
```

**Ventajas de esta configuración:**

- **Rendimiento superior**: Páginas estáticas pre-renderizadas con carga instantánea.
- **SEO optimizado**: Contenido completamente indexable por buscadores.
- **Seguridad mejorada**: Menor superficie de ataque al no requerir un servidor Node.js en producción.
- **Despliegue simplificado**: Compatibilidad perfecta con nuestra configuración Traefik/Docker.
- **Costos reducidos**: Menor consumo de recursos en servidores.

### Astro Islands: Interactividad Selectiva

Implementamos el patrón "Islands Architecture" de Astro, permitiendo interactividad solo donde es necesaria:

```astro
<!-- Componente estático por defecto -->
<CardDisplay />

<!-- Componente interactivo que se hidrata en la carga -->
<GameControls client:load />

<!-- Componente que se hidrata cuando el usuario está inactivo -->
<PlayerStats client:idle />

<!-- Componente que solo se ejecuta en el cliente (SPA) -->
<GameRoom client:only="react" />
```

**Directivas de hidratación utilizadas:**

- `client:load`: Componentes críticos que necesitan interactividad inmediata.
- `client:idle`: Componentes que pueden esperar a que el navegador esté inactivo.
- `client:visible`: Componentes que solo necesitan interactividad cuando son visibles.
- `client:only`: Componentes que dependen completamente de APIs del navegador.

### Flujo de desarrollo en DeckCards

Para desarrollar y extender DeckCards, sigue estos pasos:

1. **Configuración del entorno**:
   ```bash
   # Clonar el repositorio
   git clone <repository-url>
   cd DeckCard
   
   # Iniciar contenedores
   docker compose up -d
   ```

2. **Desarrollo del backend**:
   - Implementa nuevos endpoints en Django REST Framework
   - Prueba los endpoints con herramientas como Postman o curl
   - Documenta los nuevos endpoints con comentarios claros

3. **Desarrollo del frontend**:
   - Crea/modifica componentes Astro en `frontend/deckcard-ui/src/`
   - Implementa servicios TypeScript para comunicación con la API
   - Usa Islands Architecture para componentes interactivos con las directivas `client:*`

4. **Integración y pruebas**:
   - Verifica la comunicación correcta entre frontend y backend
   - Comprueba que las rutas de API estén configuradas correctamente
   - Prueba los flujos completos de usuarios en la aplicación

### Escenarios de Islands en DeckCards

Las Islands se utilizan estratégicamente en estos escenarios:

1. **Gestión de Salas (`client:load`):**
   - Creación y unión a salas
   - Gestión de participantes
   - Configuración de reglas de juego

2. **Control del Juego (`client:load`):**
   - Interfaz del administrador para mezclar y repartir cartas
   - Controles de turnos
   - Acciones de juego principales

3. **Mano del Jugador (`client:visible`):**
   - Visualización y uso de cartas propias
   - Interacción con cartas para jugarlas o descartarlas

4. **Estado del Juego (`client:idle`):**
   - Tablero general y estadísticas
   - Indicadores de estado de otros jugadores
   - Resumen de acciones recientes

5. **Chat y Comunicación (`client:only`):**
   - Sistema de mensajería entre jugadores
   - Notificaciones en tiempo real

### Gestión de Estado del Cliente

Utilizamos un enfoque por capas para el estado:

```typescript
// stores/gameStore.ts
import { atom, map } from 'nanostores';

// Estado global del juego
export const gameState = map({
  roomCode: null,
  players: [],
  currentTurn: null,
  gamePhase: 'waiting'
});

// Estado de la mano del jugador actual
export const playerHand = atom([]);

// Acciones del juego
export function drawCard() {
  // Lógica para tomar una carta que actualiza el estado
}
```

**Principios de gestión de estado:**

1. **Inmutabilidad**: Nunca modificamos el estado directamente.
2. **Fuente única de verdad**: El backend es la autoridad final sobre el estado del juego.
3. **Actualizaciones atómicas**: Cada acción resulta en una actualización completa del estado relevante.
4. **Optimistic UI**: Actualizamos la UI inmediatamente mientras esperamos confirmación del servidor.

### Sincronización en Tiempo Real

#### Opciones de Implementación

1. **WebSockets (implementación principal)**
   ```typescript
   // services/socketService.ts
   import { gameState } from '../stores/gameStore';
   
   export class SocketService {
     socket: WebSocket;
     
     constructor(roomCode: string) {
       this.socket = new WebSocket(`wss://api.deckcards.com/ws/room/${roomCode}`);
       
       this.socket.onmessage = (event) => {
         const data = JSON.parse(event.data);
         this.handleUpdate(data);
       };
     }
     
     handleUpdate(data) {
       // Actualizar el estado basado en el mensaje recibido
       gameState.set(data.gameState);
     }
     
     sendAction(action, payload) {
       this.socket.send(JSON.stringify({ action, payload }));
     }
   }
   ```

2. **Polling con SWR (alternativa simple)**
   ```typescript
   // En componentes React
   import useSWR from 'swr';
   
   function GameStatus() {
     const { data, error } = useSWR(
       `/api/rooms/${roomCode}`, 
       fetcher, 
       { refreshInterval: 1000 }
     );
     
     return <div>{data ? data.status : 'Loading...'}</div>;
   }
   ```

3. **Server-Sent Events (alternativa ligera)**
   ```typescript
   // services/sseService.ts
   export function initializeSSE(roomCode) {
     const eventSource = new EventSource(`/api/rooms/${roomCode}/events`);
     
     eventSource.onmessage = (event) => {
       const data = JSON.parse(event.data);
       // Actualizar estado
     };
     
     return () => eventSource.close();
   }
   ```

**Estrategia de sincronización:**

- **WebSockets**: Utilizado para acciones críticas en tiempo real (jugar cartas, turnos).
- **Reconciliación de estado**: Sincronización periódica completa para prevenir desviaciones.
- **Resolución de conflictos**: El servidor es la autoridad final para resolver conflictos.
- **Notificaciones de cambios**: Alertas visuales cuando otros jugadores realizan acciones.

### Ventajas de esta Arquitectura para DeckCards

1. **Experiencia óptima**: Carga inicial rápida con interactividad progresiva.
2. **Mejor UX**: Interfaz receptiva que actualiza inmediatamente las acciones del usuario.
3. **Resiliencia**: Funcionamiento parcial incluso con conexiones intermitentes.
4. **Mantenibilidad**: Estructura organizada que facilita la evolución del código.
5. **Eficiencia en desarrollo**: Permite trabajar en paralelo en frontend y backend.

Esta arquitectura aprovecha lo mejor de ambos mundos: la simplicidad y rendimiento de un sitio estático con la rica interactividad de una aplicación de página única (SPA) donde es necesario.