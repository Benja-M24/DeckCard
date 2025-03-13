# DeckCards
## Objetivo
Experimentar funcionalidades del stack (Postgres, django, docker, astro) en una aplicación web practica sin mucha logica detras.

### Aplicación
Gestor de Mazos de cartas para juegos de mesa.
Permite completar los campos de una tabla para generar un registro por cada carta 

### Funcionalidades

#### backend (python y django admin interface)
- Crear mazos
- Eliminar mazo
- Renombrar mazo
- Ver lista de mazos

- Añadir cartas al mazo
- Eliminar cartas del mazo
- Ver lista de cartas del mazo
- Editar cartas del mazo

- Mezclar mazo
- Repartir 'x' cartas del mazo a 'y' jugadores
- Tomar una nueva carta del mazo

#### Frontend
- Elegir mazo
- Mezclar
- Tomar la siguiente carta
- Ver la carta en modo presentacion
- Salir del modo presentacion

### Tablas de la BD
- Mazos (ID, nombre, version, fecha automatica)
- Cartas_negocios (ID, titulo, subtitulo, tipo, Costo, lista_De_niveles_Soportados, benefico_base = x - leng(nivles_Soportados), beneficio x turno en cada nivel= [a,b,c,d]) 
- Niveles_de_negocio (ID, n_Nivel, n_Wachines_necesarios, plus_De_Beneficio, )
- Cartas_Personajes (ID, Nombre, Historia, edad, sexo, imagen, Atributos_de_personaje)
- Atributos_de_personaje (ID, karma, dinero, fama, x)
- Cartas_Especiales (ID, Titulo, frase, consinga, imagen)

### Proximas funcionalidades
Salas de jugarores
- con codigo y contraseñá
- numero variable de jugadores que solo pueden ver sus cartas
- numero variable de cartas repartidas
- turnos
- descartar cartasa de la mano y tomar nuevas

## Instalación

1. Clonar el repositorio
2. Crear un archivo `.env` en la raíz del proyecto y copiar el contenido de `.env.example` y rellenar los datos necesarios
3. Ejecutar `docker compose up --build`



