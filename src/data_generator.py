"""Generador de datos de prueba para el proyecto Neo4j.

Genera archivos CSV con datos de ejemplo para cargar en la base de datos.
"""
import csv
import random
from datetime import datetime, timedelta
import os
from pathlib import Path


class DataGenerator:
    """Genera datos de ejemplo para el sistema de recomendación de películas."""
    
    GENRES = [
        "Acción", "Comedia", "Drama", "Terror", "Ciencia Ficción",
        "Fantasía", "Romance", "Thriller", "Animación", "Documental",
        "Aventura", "Misterio", "Musical", "Superhéroes", "Western",
        "Histórico", "Deportes", "Crimen", "Familia", "Independiente"
    ]
    
    COUNTRIES = [
        "Estados Unidos", "Reino Unido", "Francia", "Alemania", "Italia",
        "España", "Japón", "México", "India", "Canadá", "Australia",
        "Corea del Sur", "Brasil", "Argentina", "China"
    ]
    
    NAMES_FIRST = [
        "James", "Mary", "Robert", "Patricia", "Michael", "Jennifer", "William", "Linda",
        "David", "Barbara", "Richard", "Elizabeth", "Joseph", "Susan", "Thomas", "Jessica",
        "Charles", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Lisa",
        "Anthony", "Betty", "Donald", "Margaret", "Steven", "Sandra", "Paul", "Ashley",
        "Andrew", "Kimberly", "Joshua", "Emily", "Kenneth", "Donna", "Kevin", "Michelle"
    ]
    
    NAMES_LAST = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"
    ]
    
    MOVIE_TITLES = [
        "El Viaje del Héroe", "Sueños de Medianoche", "Cruzar las Fronteras",
        "El Último Guardián", "Voces del Futuro", "La Ciudad Perdida",
        "Más Allá del Horizonte", "La Sombra del Tiempo", "Encuentro Inesperado",
        "El Código Secreto", "Revolución Digital", "Bajo el Cielo Infinito",
        "El Espejo de Cristal", "Caminos Convergentes", "La Última Frontera",
        "Ecos del Pasado", "Luz en la Oscuridad", "El Puente de Esperanza",
        "Navegando lo Desconocido", "La Fuerza Interior", "Conexión Rota",
        "El Destino Llama", "Verdades Ocultas", "Renacimiento",
        "El Precio de la Verdad", "Más Allá de la Realidad"
    ]
    
    @staticmethod
    def generate_users(count: int = 500) -> list:
        """Generar datos de usuarios."""
        users = []
        for i in range(count):
            user_id = f"user_{i+1:04d}"
            email = f"user{i+1}@example.com"
            first = random.choice(DataGenerator.NAMES_FIRST)
            last = random.choice(DataGenerator.NAMES_LAST)
            nombre = f"{first} {last}"
            edad = random.randint(13, 80)
            país = random.choice(DataGenerator.COUNTRIES)
            fecha_registro = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
            
            users.append({
                "user_id": user_id,
                "email": email,
                "nombre": nombre,
                "edad": edad,
                "país": país,
                "fechaRegistro": fecha_registro
            })
        return users
    
    @staticmethod
    def generate_movies(count: int = 1000) -> list:
        """Generar datos de películas."""
        movies = []
        title_count = 0
        for i in range(count):
            movie_id = f"movie_{i+1:05d}"
            # Usar títulos generados
            title_num = title_count % len(DataGenerator.MOVIE_TITLES)
            if title_count >= len(DataGenerator.MOVIE_TITLES):
                título = f"{DataGenerator.MOVIE_TITLES[title_num]} {title_count // len(DataGenerator.MOVIE_TITLES)}"
            else:
                título = DataGenerator.MOVIE_TITLES[title_num]
            title_count += 1
            
            año = random.randint(1990, 2024)
            duración = random.randint(80, 180)
            presupuesto = round(random.uniform(10, 300), 2)
            descripción = f"Una película de {año} con duración de {duración} minutos."
            
            movies.append({
                "movie_id": movie_id,
                "título": título,
                "año": año,
                "duración": duración,
                "presupuesto": presupuesto,
                "descripción": descripción
            })
        return movies
    
    @staticmethod
    def generate_genres() -> list:
        """Generar datos de géneros."""
        genres = []
        for i, genre_name in enumerate(DataGenerator.GENRES):
            genre_id = f"genre_{i+1:02d}"
            descripción = f"Películas del género {genre_name}"
            películas_totales = random.randint(20, 200)
            popularidad = round(random.uniform(3.0, 9.5), 1)
            
            genres.append({
                "genre_id": genre_id,
                "nombre": genre_name,
                "descripción": descripción,
                "películas_totales": películas_totales,
                "popularidad": popularidad
            })
        return genres
    
    @staticmethod
    def generate_actors(count: int = 2500) -> list:
        """Generar datos de actores."""
        actors = []
        for i in range(count):
            actor_id = f"actor_{i+1:05d}"
            first = random.choice(DataGenerator.NAMES_FIRST)
            last = random.choice(DataGenerator.NAMES_LAST)
            nombre = f"{first} {last}"
            fecha_nac = (datetime.now() - timedelta(days=random.randint(365*20, 365*80))).strftime("%Y-%m-%d")
            nacionalidad = random.choice(DataGenerator.COUNTRIES)
            biografía = f"Actor/Actriz nacido en {nacionalidad}."
            premios = random.sample(["Oscar", "BAFTA", "Golden Globe", "Emmy", "Palma de Oro"], 
                                   k=random.randint(0, 3)) if random.random() > 0.7 else []
            
            actors.append({
                "actor_id": actor_id,
                "nombre": nombre,
                "fechaNacimiento": fecha_nac,
                "nacionalidad": nacionalidad,
                "biografía": biografía,
                "premios": "|".join(premios) if premios else ""
            })
        return actors
    
    @staticmethod
    def generate_directors(count: int = 500) -> list:
        """Generar datos de directores."""
        directors = []
        for i in range(count):
            director_id = f"director_{i+1:04d}"
            first = random.choice(DataGenerator.NAMES_FIRST)
            last = random.choice(DataGenerator.NAMES_LAST)
            nombre = f"{first} {last}"
            fecha_nac = (datetime.now() - timedelta(days=random.randint(365*20, 365*80))).strftime("%Y-%m-%d")
            nacionalidad = random.choice(DataGenerator.COUNTRIES)
            películas_dirigidas = random.randint(1, 50)
            bio = f"Director/Directora de {nacionalidad} con {películas_dirigidas} películas."
            
            directors.append({
                "director_id": director_id,
                "nombre": nombre,
                "fechaNacimiento": fecha_nac,
                "nacionalidad": nacionalidad,
                "películas_dirigidas": películas_dirigidas,
                "bio": bio
            })
        return directors
    
    @staticmethod
    def generate_relationships(users: list, movies: list, genres: list, actors: list, directors: list) -> dict:
        """Generar relaciones entre nodos."""
        relationships = {
            "watched": [],
            "rated": [],
            "liked": [],
            "bookmarked": [],
            "has_genre": [],
            "stars_in": [],
            "directed_by": [],
            "wrote_review": [],
            "follows": [],
            "similar_to": []
        }
        
        # WATCHED: Usuarios ven películas (30% de usuarios x películas)
        for user in random.sample(users, k=int(len(users) * 0.8)):
            for movie in random.sample(movies, k=random.randint(5, 50)):
                fecha = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
                duracion_visto = random.randint(int(movie["duración"]*0.7), movie["duración"])
                completado = duracion_visto >= int(movie["duración"] * 0.9)
                relationships["watched"].append({
                    "user_id": user["user_id"],
                    "movie_id": movie["movie_id"],
                    "fecha": fecha,
                    "duracion_visto": duracion_visto,
                    "completado": "true" if completado else "false"
                })
        
        # RATED: Usuarios califican películas (30% de usuarios x películas vistas)
        for rel in random.sample(relationships["watched"], k=int(len(relationships["watched"]) * 0.4)):
            fecha = rel["fecha"]
            puntuacion = random.randint(1, 10)
            relationships["rated"].append({
                "user_id": rel["user_id"],
                "movie_id": rel["movie_id"],
                "puntuacion": puntuacion,
                "fecha": fecha,
                "útil": "true" if random.random() > 0.7 else "false"
            })
        
        # LIKED: Usuarios marcan como favoritas
        for rel in random.sample(relationships["rated"], k=int(len(relationships["rated"]) * 0.3)):
            relationships["liked"].append({
                "user_id": rel["user_id"],
                "movie_id": rel["movie_id"],
                "fecha": rel["fecha"],
                "motivación": random.choice(["Excelente actuación", "Trama emocionante", "Música increíble"]),
                "intensidad": random.randint(1, 5)
            })
        
        # BOOKMARKED: Usuarios agregan a watchlist
        for user in random.sample(users, k=int(len(users) * 0.6)):
            for movie in random.sample(movies, k=random.randint(3, 20)):
                relationships["bookmarked"].append({
                    "user_id": user["user_id"],
                    "movie_id": movie["movie_id"],
                    "fecha": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
                    "prioridad": random.randint(1, 5),
                    "recordatorio": "true" if random.random() > 0.5 else "false"
                })
        
        # HAS_GENRE: Películas tienen géneros (cada película 1-3 géneros)
        for movie in movies:
            for genre in random.sample(genres, k=random.randint(1, 4)):
                relationships["has_genre"].append({
                    "movie_id": movie["movie_id"],
                    "genre_id": genre["genre_id"],
                    "es_principal": "true" if random.random() > 0.6 else "false",
                    "peso": round(random.uniform(0.5, 1.0), 2),
                    "origen": random.choice(["curado", "usuario", "automatico"])
                })
        
        # STARS_IN: Actores en películas (cada película 5-20 actores)
        for movie in movies:
            for actor in random.sample(actors, k=random.randint(5, 20)):
                relationships["stars_in"].append({
                    "actor_id": actor["actor_id"],
                    "movie_id": movie["movie_id"],
                    "rol": random.choice(["Protagonista", "Coprotagonista", "Secundario"]),
                    "orden": random.randint(1, 20),
                    "pantalla_time": round(random.uniform(5, 180), 1)
                })
        
        # DIRECTED_BY: Directores dirigen películas
        for movie in movies:
            director = random.choice(directors)
            relationships["directed_by"].append({
                "director_id": director["director_id"],
                "movie_id": movie["movie_id"],
                "año_filmacion": movie["año"],
                "versión": "Original",
                "credito_principal": "true" if random.random() > 0.1 else "false"
            })
        
        # WROTE_REVIEW: Usuarios escriben reseñas (20% de rated)
        for rel in random.sample(relationships["rated"], k=int(len(relationships["rated"]) * 0.2)):
            relationships["wrote_review"].append({
                "user_id": rel["user_id"],
                "movie_id": rel["movie_id"],
                "fecha": rel["fecha"],
                "editado": "false",
                "spoiler": "true" if random.random() > 0.85 else "false"
            })
        
        # FOLLOWS: Usuarios siguen a otros usuarios
        for user in random.sample(users, k=int(len(users) * 0.5)):
            for other_user in random.sample(users, k=random.randint(2, 15)):
                if user["user_id"] != other_user["user_id"]:
                    relationships["follows"].append({
                        "user_id": user["user_id"],
                        "other_user_id": other_user["user_id"],
                        "fecha": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                        "notificaciones": "true" if random.random() > 0.5 else "false",
                        "nivel_interaccion": random.randint(1, 5)
                    })
        
        # SIMILAR_TO: Películas similares
        for i, movie1 in enumerate(random.sample(movies, k=int(len(movies) * 0.3))):
            for movie2 in random.sample([m for m in movies if m != movie1], k=random.randint(2, 5)):
                relationships["similar_to"].append({
                    "movie_id": movie1["movie_id"],
                    "similar_movie_id": movie2["movie_id"],
                    "similitud": round(random.uniform(0.6, 1.0), 2),
                    "mismo_genero": "true" if random.random() > 0.4 else "false",
                    "origen": random.choice(["metadata", "co-views", "manual"])
                })
        
        return relationships
    
    @staticmethod
    def save_to_csv(data: list, filename: str, data_dir: str = "data"):
        """Guardar datos en archivo CSV."""
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)
        
        if not data:
            return filepath
        
        keys = data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Generado: {filepath} ({len(data)} registros)")
        return filepath
    
    @staticmethod
    def generate_all(data_dir: str = "data"):
        """Generar todos los datos."""
        print("Generando datos de prueba...")
        
        # Generar datos
        users = DataGenerator.generate_users(1000)
        movies = DataGenerator.generate_movies(1500)
        genres = DataGenerator.generate_genres()
        actors = DataGenerator.generate_actors(3000)
        directors = DataGenerator.generate_directors(800)
        
        # Guardar
        DataGenerator.save_to_csv(users, "users.csv", data_dir)
        DataGenerator.save_to_csv(movies, "movies.csv", data_dir)
        DataGenerator.save_to_csv(genres, "genres.csv", data_dir)
        DataGenerator.save_to_csv(actors, "actors.csv", data_dir)
        DataGenerator.save_to_csv(directors, "directors.csv", data_dir)
        
        # Relaciones
        rels = DataGenerator.generate_relationships(users, movies, genres, actors, directors)
        for rel_type, rel_data in rels.items():
            DataGenerator.save_to_csv(rel_data, f"{rel_type}.csv", data_dir)
        
        total_nodes = len(users) + len(movies) + len(genres) + len(actors) + len(directors)
        total_rels = sum(len(v) for v in rels.values())
        
        print(f"\n Generación completada!")
        print(f"   Total de nodos: {total_nodes:,}")
        print(f"   Total de relaciones: {total_rels:,}")
        
        return data_dir


if __name__ == "__main__":
    DataGenerator.generate_all()
