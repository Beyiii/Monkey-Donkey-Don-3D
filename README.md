# Monkey-Donkey-Don-3D

El juego recibe un archivo csv donde estará el patrón de la estructura constituida por las plataformas. El 
archivo debe poseer 5 datos (1, 0, o x) separados por comas en cada línea (5 líneas). El 1 indica la presencia 
de una plataforma escalable, el 0 indica que no existe plataforma y el x indica que es una plataforma falsa, 
es decir, que desaparecerá si el personaje salta sobre ella. El archivo puede ser modificado siguiendo las 
reglas indicadas con anterioridad. La parte del código “Escenografia” es el encargado de leer el archivo csv.
Las plataformas se van dibujando en 2 planos distintos (uno más adelante que otro) intercaladamente, de 
tal manera que quede 3 columnas en un plano más adelante que las otras 2. Además, la forma en que se van
dibujando es a partir de la posición X positiva a negativa.
Para mover al personaje se ocupan 4 teclas, “A” para rotarlo hacia la izquierda (contrario a las manecillas
del reloj), “W” para avanzar, “D” para rotarlo hacia la derecha (como las manecillas del reloj) y “SPACE”
para que salte (parabólicamente).
Para cambiar la posición de la cámara se ocupan 3 teclas, “B” para que quede frente al personaje, “N” para
que capte un ¾ de la escena (la cámara se ubica en x positivo) y “M” para que capte un ¾ de la escena (la
cámara se ubica en x negativo). 
Para poder jugar se debe acceder a la consola en donde está la carpeta del juego y hacer la siguiente 
llamada para poder ejecutarlo: python monkey_jump.py structure.csv
