"""Aplicación principal - Backend funcional para el sistema de recomendación de películas.

Proporciona una interfaz para interactuar con la base de datos Neo4j,
incluyendo CRUD de nodos, relaciones, consultas y recomendaciones.
"""
from typing import Dict, List, Any
from datetime import datetime, date
from .neo4j_conn import get_connection
from .crud_operations import CrudOperations
from .queries import CypherQueries
from .recommendation import RecommendationEngine
from .data_generator import DataGenerator
from .importer import DataImporter
from . import schema


class MovieRecommendationApp:
    """Aplicación principal de recomendación de películas."""
    
    def __init__(self):
        self.conn = get_connection()
        self.crud = CrudOperations(self.conn)
        self.queries = CypherQueries(self.conn)
        self.recommendations = RecommendationEngine(self.conn)
        self.importer = DataImporter(self.conn)
    
    # ============ INICIALIZACIÓN ============
    
    def initialize_database(self, clear=True):
        """Inicializar la base de datos con datos de prueba."""
        print("Inicializando base de datos...")
        
        if clear:
            print("  - Limpiando datos existentes...")
            self.importer.clear_database()
        
        print("  - Generando datos de prueba...")
        data_dir = DataGenerator.generate_all()
        
        print("  - Creando índices...")
        self.importer.create_indexes()
        
        print("  - Importando datos...")
        stats = {
            "users": self.importer.import_users(f"{data_dir}/users.csv"),
            "movies": self.importer.import_movies(f"{data_dir}/movies.csv"),
            "genres": self.importer.import_genres(f"{data_dir}/genres.csv"),
            "actors": self.importer.import_actors(f"{data_dir}/actors.csv"),
            "directors": self.importer.import_directors(f"{data_dir}/directors.csv"),
            "watched": self.importer.import_watched_relationships(f"{data_dir}/watched.csv"),
            "rated": self.importer.import_rated_relationships(f"{data_dir}/rated.csv"),
            "liked": self.importer.import_liked_relationships(f"{data_dir}/liked.csv"),
            "bookmarked": self.importer.import_bookmarked_relationships(f"{data_dir}/bookmarked.csv"),
            "has_genre": self.importer.import_has_genre_relationships(f"{data_dir}/has_genre.csv"),
            "stars_in": self.importer.import_stars_in_relationships(f"{data_dir}/stars_in.csv"),
            "directed_by": self.importer.import_directed_by_relationships(f"{data_dir}/directed_by.csv"),
            "follows": self.importer.import_follows_relationships(f"{data_dir}/follows.csv"),
            "similar_to": self.importer.import_similar_to_relationships(f"{data_dir}/similar_to.csv"),
        }
        
        print("\n✅ Base de datos inicializada:")
        total_nodes = sum([stats["users"], stats["movies"], stats["genres"], stats["actors"], stats["directors"]])
        total_relationships = sum([v for k, v in stats.items() if k != "users" and k != "movies" and k != "genres" and k != "actors" and k != "directors"])
        
        for key, value in stats.items():
            print(f"   {key}: {value}")
        print(f"\n   📊 Total: {total_nodes:,} nodos, {total_relationships:,} relaciones")
        
        return stats
    
    # ============ OPERACIONES CRUD - NODOS ============
    
    def create_user(self, user_data: Dict) -> Dict:
        """Crear un nuevo usuario."""
        return self.crud.create_user(user_data)
    
    def create_movie(self, movie_data: Dict) -> Dict:
        """Crear una nueva película."""
        return self.crud.create_movie(movie_data)
    
    def create_genre(self, genre_data: Dict) -> Dict:
        """Crear un nuevo género."""
        return self.crud.create_genre(genre_data)
    
    def create_actor(self, actor_data: Dict) -> Dict:
        """Crear un nuevo actor."""
        return self.crud.create_actor(actor_data)
    
    def create_director(self, director_data: Dict) -> Dict:
        """Crear un nuevo director."""
        return self.crud.create_director(director_data)
    
    def get_user(self, user_id: str) -> Dict:
        """Obtener datos de un usuario."""
        return self.crud.get_node_by_id(schema.LABEL_USER, schema.PROP_USER_ID, user_id)
    
    def get_movie(self, movie_id: str) -> Dict:
        """Obtener datos de una película."""
        return self.crud.get_node_by_id(schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id)
    
    def get_movies_by_genre(self, genre_name: str) -> List[Dict]:
        """Obtener películas de un género."""
        return self.queries.query_1_movies_by_genre(genre_name)
    
    def get_user_watchlist(self, user_id: str) -> List[Dict]:
        """Obtener películas guardadas por un usuario."""
        return self.queries.query_2_user_watchlist_with_actors(user_id)
    
    def list_all_users(self) -> List[Dict]:
        """Listar todos los usuarios."""
        return self.crud.get_all_nodes(schema.LABEL_USER)
    
    def list_all_movies(self) -> List[Dict]:
        """Listar todas las películas."""
        return self.crud.get_all_nodes(schema.LABEL_MOVIE)
    
    def update_user(self, user_id: str, properties: Dict) -> Dict:
        """Actualizar propiedades de un usuario."""
        return self.crud.add_properties_to_node(schema.LABEL_USER, schema.PROP_USER_ID, user_id, properties)
    
    def update_movie(self, movie_id: str, properties: Dict) -> Dict:
        """Actualizar propiedades de una película."""
        return self.crud.add_properties_to_node(schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id, properties)
    
    def delete_user(self, user_id: str) -> bool:
        """Eliminar un usuario."""
        return self.crud.delete_node(schema.LABEL_USER, schema.PROP_USER_ID, user_id)
    
    def delete_movie(self, movie_id: str) -> bool:
        """Eliminar una película."""
        return self.crud.delete_node(schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id)
    
    # ============ OPERACIONES CRUD - RELACIONES ============
    
    def user_watch_movie(self, user_id: str, movie_id: str, properties: Dict = None) -> Dict:
        """Marcar película como vista."""
        properties = properties or {
            "fecha": date.today().isoformat(),
            "duracion_visto": 90,
            "completado": True
        }
        return self.crud.create_relationship(
            schema.LABEL_USER, schema.PROP_USER_ID, user_id,
            schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id,
            schema.REL_WATCHED, properties
        )
    
    def user_rate_movie(self, user_id: str, movie_id: str, rating: int) -> Dict:
        """Calificar una película."""
        return self.crud.create_relationship(
            schema.LABEL_USER, schema.PROP_USER_ID, user_id,
            schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id,
            schema.REL_RATED, {
                "puntuacion": rating,
                "fecha": date.today().isoformat(),
                "útil": True
            }
        )
    
    def user_like_movie(self, user_id: str, movie_id: str) -> Dict:
        """Marcar película como favorita."""
        return self.crud.create_relationship(
            schema.LABEL_USER, schema.PROP_USER_ID, user_id,
            schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id,
            schema.REL_LIKED, {
                "fecha": date.today().isoformat(),
                "motivación": "Excelente película"
            }
        )
    
    def user_bookmark_movie(self, user_id: str, movie_id: str, priority: int = 3) -> Dict:
        """Agregar película a la lista de ver después."""
        return self.crud.create_relationship(
            schema.LABEL_USER, schema.PROP_USER_ID, user_id,
            schema.LABEL_MOVIE, schema.PROP_MOVIE_ID, movie_id,
            schema.REL_BOOKMARKED, {
                "fecha": date.today().isoformat(),
                "prioridad": priority
            }
        )
    
    def user_follow_user(self, user_id: str, other_user_id: str) -> Dict:
        """Un usuario sigue a otro usuario."""
        return self.crud.create_relationship(
            schema.LABEL_USER, schema.PROP_USER_ID, user_id,
            schema.LABEL_USER, schema.PROP_USER_ID, other_user_id,
            schema.REL_FOLLOWS, {
                "fecha": date.today().isoformat(),
                "notificaciones": True
            }
        )
    
    # ============ CONSULTAS CYPHER ============
    
    def get_top_rated_movies(self, limit: int = 10) -> List[Dict]:
        """Obtener películas mejor calificadas."""
        return self.queries.query_4_top_rated_movies(limit)
    
    def get_directors_stats(self) -> List[Dict]:
        """Obtener estadísticas de directores."""
        return self.queries.query_3_directors_and_movie_count()
    
    def get_user_similar_users(self, user_id: str) -> List[Dict]:
        """Obtener usuarios con gustos similares."""
        return self.queries.query_5_user_similarity_network(user_id)
    
    def search_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Obtener películas recomendadas basadas en géneros."""
        return self.queries.query_6_recommendation_based_on_watched_and_genres(user_id, limit)
    
    def get_aggregation_actors_by_genre(self) -> List[Dict]:
        """Obtener agregación de actores por género."""
        return self.queries.query_aggregation_actors_by_genre()
    
    def get_user_engagement_stats(self) -> Dict:
        """Obtener estadísticas de engagement de usuarios."""
        return self.queries.query_user_engagement_stats()
    
    def get_movies_without_reviews(self) -> List[Dict]:
        """Obtener películas sin reseñas."""
        return self.queries.query_movies_without_reviews()
    
    # ============ RECOMENDACIONES ============
    
    def recommend_collaborative_filtering(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Recomendación por filtrado colaborativo."""
        return self.recommendations.recommend_by_collaborative_filtering(user_id, limit)
    
    def recommend_by_content(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Recomendación por similitud de contenido."""
        return self.recommendations.recommend_by_content_similarity(user_id, limit)
    
    def recommend_by_genre(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Recomendación por afinidad de género."""
        return self.recommendations.recommend_by_genre_affinity(user_id, limit)
    
    def get_trending_movies(self, limit: int = 10) -> List[Dict]:
        """Obtener películas tendencia."""
        return self.recommendations.recommend_trending(limit)
    
    def recommend_by_favorite_actors(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Recomendación por actores favoritos."""
        return self.recommendations.get_actor_recommendations(user_id, limit)
    
    def recommend_from_community(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Recomendación basada en comunidad de usuarios seguidos."""
        return self.recommendations.get_community_recommendations(user_id, limit)
    
    def get_personalized_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Obtener recomendaciones personalizadas (estrategia híbrida)."""
        return self.recommendations.get_personalized_recommendations(user_id, limit)
    
    def calculate_user_similarity(self, user_id_1: str, user_id_2: str) -> float:
        """Calcular similitud entre dos usuarios."""
        return self.recommendations.calculate_user_similarity(user_id_1, user_id_2)
    
    # ============ ESTADÍSTICAS ============
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del grafo."""
        return {
            "total_users": self.crud.count_nodes(schema.LABEL_USER),
            "total_movies": self.crud.count_nodes(schema.LABEL_MOVIE),
            "total_genres": self.crud.count_nodes(schema.LABEL_GENRE),
            "total_actors": self.crud.count_nodes(schema.LABEL_ACTOR),
            "total_directors": self.crud.count_nodes(schema.LABEL_DIRECTOR),
            "total_nodes": self.crud.count_all_nodes(),
            "total_relationships": self.crud.count_relationships(),
            "watched_count": self.crud.count_relationships(schema.REL_WATCHED),
            "rated_count": self.crud.count_relationships(schema.REL_RATED),
        }
    
    def close(self):
        """Cerrar conexión con la base de datos."""
        self.conn.close()


# ============ EJEMPLO DE USO ============

def main():
    """Función principal de ejemplo."""
    print("🎬 Sistema de Recomendación de Películas - Neo4j\n")
    
    app = MovieRecommendationApp()
    
    try:
        # Inicializar base de datos
        print("=" * 60)
        app.initialize_database()
        
        # Obtener estadísticas
        print("\n" + "=" * 60)
        print("ESTADÍSTICAS DEL GRAFO")
        print("=" * 60)
        stats = app.get_graph_stats()
        for key, value in stats.items():
            print(f"  {key}: {value:,}")
        
        # Ejemplos de consultas
        print("\n" + "=" * 60)
        print("PELÍCULAS MEJOR CALIFICADAS")
        print("=" * 60)
        top_movies = app.get_top_rated_movies(5)
        for movie in top_movies:
            print(f"  {movie['película']} ({movie['año']}): {movie['calificacion_promedio']}/10")
        
        # Recomendaciones
        print("\n" + "=" * 60)
        print("RECOMENDACIONES PERSONALIZADAS (Usuario: user_0001)")
        print("=" * 60)
        recommendations = app.get_personalized_recommendations("user_0001", 5)
        for rec in recommendations:
            print(f"  {rec['película']} ({rec['año']}): {rec['calificacion_promedio']}/10")
        
        # Tendencias
        print("\n" + "=" * 60)
        print("PELÍCULAS TENDENCIA")
        print("=" * 60)
        trending = app.get_trending_movies(5)
        for movie in trending:
            print(f"  {movie['película']}: {movie['vistas_ultimos_30_dias']} vistas")
        
        print("\n" + "=" * 60)
        print("✅ Aplicación funcionando correctamente!")
        print("=" * 60)
        
    finally:
        app.close()


if __name__ == "__main__":
    main()
