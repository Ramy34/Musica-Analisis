# 🎵 Musica-Analisis (Tablero Musical)

**Musica-Analisis** es un proyecto de Ingeniería de Datos (Pipeline ETL) que combina **Python**, **PostgreSQL** y herramientas de BI para extraer, transformar, analizar y dar una nueva vida a tu biblioteca musical local (iTunes/Apple Music).

A diferencia de los resúmenes anuales como Spotify Wrapped, este proyecto te da control total sobre tu información, permitiéndote analizar tus hábitos de escucha históricos y generar **playlists inteligentes (M3U)** de forma completamente automatizada.

---

## 🚀 El Flujo de Trabajo (Pipeline ETL)

1. **Extracción de Metadatos (`extraccion_metdatos.py`)**: Escanea tus archivos de audio `.mp3` y `.m4a` para extraer etiquetas profundas (BPM, Letras, Tonos, Danzabilidad, Colores de beaTunes) y las exporta a CSV mediante procesamiento en paralelo.
2. **Parseo de XML (`xml_to_csv.py`)**: Convierte las exportaciones de la biblioteca de iTunes (`.xml` / `plist`) a formato tabular, rescatando datos invaluables como contador de reproducciones, fechas de salto y calificaciones.
3. **Carga en Base de Datos (`carga_postgresql.py`)**: Sube los datos procesados a **PostgreSQL**, creando automáticamente esquemas, tablas dinámicas y vistas precalculadas listas para el análisis.
4. **Generación de Playlists (`generar_playlist.py`)**: Consulta la base de datos para crear archivos `.m3u8` automatizados basados en algoritmos personalizados (ej. una lista "nocturna" basada en BPM y género).

---

## 📊 Tecnologías Utilizadas
- **Python**: Orquestación del flujo (`multiprocessing`), manejo de datos (`pandas`), extracción de tags de audio (`mutagen`), y conexión a base de datos (`psycopg2`).
- **PostgreSQL**: Motor de base de datos relacional para el almacenamiento centralizado, normalización de artistas y limpieza de datos (gestión de catálogos y excepciones).
- **Power BI**: Herramienta de BI para conectarse a las vistas de la base de datos y crear dashboards interactivos (Opcional).

---

## ✨ Características Principales
- **Orquestador Centralizado (`main.py`)**: Ejecuta todo el flujo con un solo comando, mostrando barras de progreso a color en la terminal y manteniendo un registro de auditoría (`musica_analisis.log`).
- **Desnormalización Inteligente de Artistas**: Maneja agrupaciones complejas y colaboraciones (ej. "Jesse & Joy", o artistas con comas) para calcular estadísticas reales por artista individual.
- **Filtros Dinámicos**: Discrimina automáticamente versiones en vivo, acústicas, instrumentales o repetidas basándose en los comentarios de la canción para mantener tus listas limpias.

---

## ⚙️ Uso e Instalación

1. Clona el repositorio e instala las dependencias de Python necesarias usando el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Configura tus credenciales de PostgreSQL y rutas de carpetas a través de tu clase de configuración (`config_loader.py`).
3. Inicializa las tablas base y catálogos en PostgreSQL ejecutando el script `code/sql/01 - Inicializacion.sql`.
4. Ejecuta el orquestador principal desde la terminal:
   ```bash
   python main.py
   ```
5. Revisa la carpeta de salida para encontrar tus nuevas playlists M3U generadas o conecta tu software de visualización a la base de datos PostgreSQL.

*Nota: Las carpetas con archivos de audio XML y CSV deben organizarse según lo especificado en la configuración del proyecto.*