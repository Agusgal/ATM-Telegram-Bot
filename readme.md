# Evaluación técnica Jampp: Bot de Telegram

En el siguiente proyecto se implementó un bot de telegram que lista los cajeros automáticos más cercanos de la
red seleccionada y muestra un mapa con su ubicación precisa. 

En el siguiente repositorio puede encontrarse el proyecto completo: https://github.com/Agusgal/TelegramBot

Para encontrar el bot debe buscarse como: @BsAsATMbot

## Bibliotecas requeridas:

- Python-Telegram-Bot: interfaz intermedia para manejar API de Telegram
                       documentación disponible en https://python-telegram-bot.readthedocs.io/en/stable/
- Tilemapbase: biblioteca para descargar mapas opensource, se 
               se utiliza OpenStreetMaps en especifico. Documentacion 
               disponible en: https://github.com/MatthewDaws/TileMapBase
- Matplotlib: dibujado de mapas.
- Geopy: calculo de coordenadas geográficas y distancias, documentación disponible en: 
- Datetime: manejo de horarios y fechas, documentación disponible en:
- Numpy: matemática general y arreglos eficientes
- Csv: manjeo de archivo Csv 
- Json: almacenamiento de datos de cajeros utilizados.

## Instrucciones de uso:

Para poder ejecutar el programa solamente hace falta colocarse en el directorio donde resida el proyecto y
correr el siguiente comando en una terminal: 

> Python3 main.py

Se utilizó la versión 3.8 de Python para desarrollar el proyecto.

## Elecciones de Diseño relevantes:

- El bot posee los siguientes comandos: 'help', el cual muestra todos los comandos disponibles, 'start' se inicia la 
conversación con el bot, 'link' y 'banelco', muestran información acerca de cajeros 
cercanos de la red correspondiente
- Se decició cargar solamente los cajeros de la red seleccionada en un objeto de creación propia y luego filtrarlos para 
encontrar los cajeros más cercanos
- Cada vez que se consulta la API se guarda en un archivo JSON la información del cajero consultado: el horario, las recargas estimadas 
restantes y su id. 
- Para el algoritmo de busqueda se utilizó una busqueda binaria en una coordenada espacial (latitud), lo que logra una performance hasta 24 veces mejor que 
el caso lineal promedio
- Se utilizaron mapas del proyecto open-source OpenStreetMaps
- Para estimar el número de extracciones restantes se tiene en cuenta el número de extracciones almacenado en el archivo JSON,
el horario de la última extracción, y cuántos cajeros son los que el usuario tiene como más cercanos