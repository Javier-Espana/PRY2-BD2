"""Definición del esquema del grafo.

Este archivo contiene definiciones de constantes para etiquetas, 
relaciones y propiedades del grafo.
"""

# Etiquetas de Nodos
LABEL_USER = "User"
LABEL_MOVIE = "Movie"
LABEL_GENRE = "Genre"
LABEL_ACTOR = "Actor"
LABEL_DIRECTOR = "Director"
LABEL_REVIEW = "Review"

# Tipos de Relaciones
REL_WATCHED = "WATCHED"
REL_RATED = "RATED"
REL_LIKED = "LIKED"
REL_BOOKMARKED = "BOOKMARKED"
REL_HAS_GENRE = "HAS_GENRE"
REL_STARS_IN = "STARS_IN"
REL_DIRECTED_BY = "DIRECTED_BY"
REL_WROTE_REVIEW = "WROTE_REVIEW"
REL_FOLLOWS = "FOLLOWS"
REL_RECOMMENDS = "RECOMMENDS"
REL_SIMILAR_TO = "SIMILAR_TO"
REL_SIMILAR_USER = "SIMILAR_USER"

# Propiedades de Usuarios
PROP_USER_ID = "user_id"
PROP_USER_EMAIL = "email"
PROP_USER_NOMBRE = "nombre"
PROP_USER_EDAD = "edad"
PROP_USER_PAIS = "país"
PROP_USER_FECHA_REGISTRO = "fechaRegistro"

# Propiedades de Películas
PROP_MOVIE_ID = "movie_id"
PROP_MOVIE_TITULO = "título"
PROP_MOVIE_AÑO = "año"
PROP_MOVIE_DURACION = "duración"
PROP_MOVIE_PRESUPUESTO = "presupuesto"
PROP_MOVIE_DESCRIPCION = "descripción"

# Propiedades de Géneros
PROP_GENRE_ID = "genre_id"
PROP_GENRE_NOMBRE = "nombre"
PROP_GENRE_DESCRIPCION = "descripción"
PROP_GENRE_TOTALES = "películas_totales"
PROP_GENRE_POPULARIDAD = "popularidad"

# Propiedades de Actores
PROP_ACTOR_ID = "actor_id"
PROP_ACTOR_NOMBRE = "nombre"
PROP_ACTOR_FECHA_NAC = "fechaNacimiento"
PROP_ACTOR_NACIONALIDAD = "nacionalidad"
PROP_ACTOR_BIO = "biografía"
PROP_ACTOR_PREMIOS = "premios"

# Propiedades de Directores
PROP_DIRECTOR_ID = "director_id"
PROP_DIRECTOR_NOMBRE = "nombre"
PROP_DIRECTOR_FECHA_NAC = "fechaNacimiento"
PROP_DIRECTOR_NACIONALIDAD = "nacionalidad"
PROP_DIRECTOR_PELICULAS = "películas_dirigidas"
PROP_DIRECTOR_BIO = "bio"

# Propiedades de Reviews
PROP_REVIEW_ID = "review_id"
PROP_REVIEW_CALIFICACION = "calificación"
PROP_REVIEW_TEXTO = "texto"
PROP_REVIEW_FECHA = "fecha"
PROP_REVIEW_UTIL_COUNT = "útil_count"
PROP_REVIEW_SPOILER = "spoiler"

# Propiedades de Relaciones
PROP_REL_FECHA = "fecha"
PROP_REL_DURACION = "duracion_visto"
PROP_REL_COMPLETADO = "completado"
PROP_REL_PUNTUACION = "puntuacion"
PROP_REL_MOTIVACION = "motivación"
PROP_REL_PRIORIDAD = "prioridad"
PROP_REL_ES_PRINCIPAL = "es_principal"
PROP_REL_PESO = "peso"
PROP_REL_ROL = "rol"
PROP_REL_ORDEN = "orden"
PROP_REL_PANTALLA_TIME = "pantalla_time"
PROP_REL_CONFIANZA = "confianza"
PROP_REL_SIMILITUD = "similitud"
PROP_REL_PELICULAS_COMUNES = "películas_comunes"
PROP_REL_RAZON = "razón"

# Índices recomendados
INDEXES = [
    (LABEL_USER, PROP_USER_ID),
    (LABEL_USER, PROP_USER_EMAIL),
    (LABEL_MOVIE, PROP_MOVIE_ID),
    (LABEL_GENRE, PROP_GENRE_ID),
    (LABEL_ACTOR, PROP_ACTOR_ID),
    (LABEL_DIRECTOR, PROP_DIRECTOR_ID),
    (LABEL_REVIEW, PROP_REVIEW_ID),
]
