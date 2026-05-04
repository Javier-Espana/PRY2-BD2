"""Sistema de recomendación basado en grafos y algoritmos de data science.

Implementa recomendaciones usando:
- Filtrado colaborativo
- Similitud de contenido
- Análisis de patrón de usuario
"""
from typing import List, Dict, Any
from .neo4j_conn import Neo4jConnection
from . import schema


class RecommendationEngine:
    """Motor de recomendación para películas."""
    
    def __init__(self, conn: Neo4jConnection):
        self.conn = conn
    
    def recommend_by_collaborative_filtering(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Recomendación por filtrado colaborativo.
        
        Encuentra usuarios con gustos similares y recomienda películas que ellos han calificado bien.
        """
        def _recommend(tx):
            cypher = """
            MATCH (target_user:User {user_id: $user_id})-[:RATED]->(movie:Movie)<-[:RATED]-(similar_user:User)
            WHERE target_user <> similar_user
            
            // Encontrar películas que los usuarios similares calificaron bien pero target no ha visto
            MATCH (similar_user)-[r:RATED]->(recommendation:Movie)
            WHERE NOT (target_user)-[:WATCHED]->(recommendation)
              AND NOT (target_user)-[:RATED]->(recommendation)
              AND r.puntuacion >= 7
            
            // Calcular score basado en:
            // 1. Cuántos usuarios similares la calificaron bien
            // 2. La calificación promedio
            WITH recommendation,
                 COUNT(similar_user) as usuarios_similares_count,
                 AVG(r.puntuacion) as avg_rating
            
            // Datos de la película
            OPTIONAL MATCH (recommendation)-[:HAS_GENRE]->(g:Genre)
            WITH recommendation, usuarios_similares_count, avg_rating,
                 COLLECT(DISTINCT g.nombre) as generos
            
            RETURN recommendation.título as película,
                   recommendation.año as año,
                   recommendation.duración as duración,
                   generos as géneros,
                   usuarios_similares_count as votos_similares,
                   ROUND(avg_rating * 10) / 10.0 as calificación_promedio,
                   usuarios_similares_count * avg_rating as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
    
    def recommend_by_content_similarity(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Recomendación por similitud de contenido.
        
        Basada en películas similares a las que el usuario ha visto.
        """
        def _recommend(tx):
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:RATED]->(watched:Movie)
            WHERE watched.año >= $year_threshold
            
            // Encontrar películas similares
            MATCH (watched)-[:SIMILAR_TO]->(similar:Movie)
            WHERE NOT (u)-[:WATCHED]->(similar)
              AND NOT (u)-[:RATED]->(similar)
            
            // Score basado en similitud
            WITH similar, watched.título as movie_watched
            OPTIONAL MATCH (similar)-[:HAS_GENRE]->(g:Genre)
            OPTIONAL MATCH (u2:User)-[r:RATED]->(similar)
            
            WITH similar, COLLECT(DISTINCT g.nombre) as generos,
                 COUNT(DISTINCT u2) as rating_count,
                 AVG(r.puntuacion) as avg_rating
            
            RETURN similar.título as película,
                   similar.año as año,
                   similar.duración as duración,
                   generos as géneros,
                   rating_count as veces_calificada,
                   COALESCE(ROUND(avg_rating * 10) / 10.0, 0) as calificación_promedio,
                   rating_count * COALESCE(avg_rating, 5) as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, year_threshold=2020, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
    
    def recommend_by_genre_affinity(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Recomendación basada en afinidad por géneros.
        
        Analiza qué géneros ha calificado bien y recomienda películas similares.
        """
        def _recommend(tx):
            cypher = """
            // Encontrar géneros favoritos del usuario
            MATCH (u:User {user_id: $user_id})-[:RATED {puntuacion: 8}|:RATED {puntuacion: 9}|:RATED {puntuacion: 10}]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            WITH g, COUNT(DISTINCT m) as movies_count
            WHERE movies_count >= 2
            
            // Encontrar películas en esos géneros que el usuario no ha visto
            MATCH (g)-[:HAS_GENRE]-(new_movie:Movie)
            WHERE NOT (u)-[:WATCHED]->(new_movie)
              AND NOT (u)-[:RATED]->(new_movie)
            
            // Calcular rating de la película
            OPTIONAL MATCH (other_users:User)-[r:RATED]->(new_movie)
            
            WITH new_movie, g.nombre as genre,
                 COUNT(DISTINCT other_users) as users_rated,
                 AVG(r.puntuacion) as avg_rating,
                 COUNT(DISTINCT g) as genre_matches
            
            RETURN DISTINCT new_movie.título as película,
                   new_movie.año as año,
                   new_movie.duración as duración,
                   genre_matches as géneros_coincidentes,
                   users_rated as calificaciones_recibidas,
                   COALESCE(ROUND(avg_rating * 10) / 10.0, 0) as calificación_promedio,
                   genre_matches * COALESCE(avg_rating, 7) as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
    
    def recommend_trending(self, limit: int = 10) -> List[Dict]:
        """
        Obtener películas tendencia.
        
        Basadas en número de visualizaciones recientes y calificación.
        """
        def _recommend(tx):
            cypher = """
            MATCH (u:User)-[watched:WATCHED]->(m:Movie)
            WHERE watched.fecha >= date() - duration('P30D')
            
            OPTIONAL MATCH (u2:User)-[r:RATED]->(m)
            WHERE r.fecha >= date() - duration('P30D')
            
            WITH m,
                 COUNT(DISTINCT u) as views_30days,
                 AVG(r.puntuacion) as avg_rating_recent,
                 COUNT(DISTINCT u2) as recent_ratings
            
            OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
            
            WITH m, views_30days, avg_rating_recent, recent_ratings,
                 COLLECT(DISTINCT g.nombre) as generos
            
            RETURN m.título as película,
                   m.año as año,
                   m.duración as duración,
                   generos as géneros,
                   views_30days as vistas_ultimos_30_dias,
                   COALESCE(ROUND(avg_rating_recent * 10) / 10.0, 0) as calificación_reciente,
                   views_30days * COALESCE(avg_rating_recent, 7) as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
    
    def get_actor_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Películas con actores favoritos del usuario.
        """
        def _recommend(tx):
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:RATED {puntuacion: 9}|:RATED {puntuacion: 10}]->(m:Movie)<-[:STARS_IN]-(a:Actor)
            
            // Encontrar otras películas con estos actores
            MATCH (a)-[:STARS_IN]->(new_movie:Movie)
            WHERE NOT (u)-[:WATCHED]->(new_movie)
              AND NOT (u)-[:RATED]->(new_movie)
            
            OPTIONAL MATCH (u2:User)-[r:RATED]->(new_movie)
            OPTIONAL MATCH (new_movie)-[:HAS_GENRE]->(g:Genre)
            
            WITH new_movie, a.nombre as actor,
                 COLLECT(DISTINCT g.nombre) as generos,
                 COUNT(DISTINCT u2) as rating_count,
                 AVG(r.puntuacion) as avg_rating
            
            RETURN DISTINCT new_movie.título as película,
                   new_movie.año as año,
                   actor as actor_favorito,
                   generos as géneros,
                   COALESCE(ROUND(avg_rating * 10) / 10.0, 0) as calificación_promedio
            
            ORDER BY calificación_promedio DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
    
    def calculate_user_similarity(self, user_id: str, other_user_id: str) -> float:
        """
        Calcular similitud entre dos usuarios basada en películas vistas.
        
        Devuelve valor entre 0 (sin similitud) y 1 (idénticos gustos).
        """
        def _calculate(tx):
            cypher = """
            MATCH (u1:User {user_id: $user_id})-[:WATCHED]->(m1:Movie)<-[:WATCHED]-(u2:User {user_id: $other_user_id})
            MATCH (u1)-[:WATCHED]->(all_m1)
            MATCH (u2)-[:WATCHED]->(all_m2)
            
            WITH COUNT(DISTINCT m1) as common_movies,
                 COUNT(DISTINCT all_m1) as u1_total,
                 COUNT(DISTINCT all_m2) as u2_total
            
            // Jaccard similarity
            RETURN CASE 
                   WHEN (u1_total + u2_total - common_movies) = 0 THEN 1.0
                   ELSE ROUND(toFloat(common_movies) / (u1_total + u2_total - common_movies) * 100) / 100.0
                   END as similarity
            """
            result = tx.run(cypher, user_id=user_id, other_user_id=other_user_id)
            record = result.single()
            return record["similarity"] if record else 0.0
        
        return self.conn.execute_read(_calculate)
    
    def get_community_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Recomendaciones basadas en la comunidad de usuarios seguidos.
        """
        def _recommend(tx):
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:FOLLOWS]->(followed:User)
            MATCH (followed)-[:LIKED]->(m:Movie)
            WHERE NOT (u)-[:WATCHED]->(m)
            
            OPTIONAL MATCH (rated_user:User)-[r:RATED]->(m)
            OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
            
            WITH m, COLLECT(followed.nombre) as seguidos_que_la_like,
                 COLLECT(DISTINCT g.nombre) as generos,
                 COUNT(DISTINCT rated_user) as total_ratings,
                 AVG(r.puntuacion) as avg_rating
            
            RETURN m.título as película,
                   m.año as año,
                   LENGTH(seguidos_que_la_like) as recomendaciones_de_seguidos,
                   seguidos_que_la_like as seguidos,
                   generos as géneros,
                   COALESCE(ROUND(avg_rating * 10) / 10.0, 0) as calificación_promedio
            
            ORDER BY recomendaciones_de_seguidos DESC, calificación_promedio DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
    
    def get_personalized_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Obtener recomendaciones personalizadas combinando múltiples estrategias.
        
        Combina filtrado colaborativo, similitud de contenido y affinidad por géneros.
        """
        def _recommend(tx):
            cypher = """
            // Estrategia híbrida: combinar múltiples fuentes
            MATCH (u:User {user_id: $user_id})
            
            // 1. Usuarios similares que han calificado películas bien
            MATCH (u)-[:RATED]->(m1)<-[:RATED]-(sim_user:User)
            WHERE u <> sim_user
            MATCH (sim_user)-[r:RATED {puntuacion: 8}|:RATED {puntuacion: 9}|:RATED {puntuacion: 10}]->(rec1:Movie)
            WHERE NOT (u)-[:WATCHED]->(rec1)
            
            WITH u, COUNT(DISTINCT rec1) as collab_count, COLLECT(DISTINCT rec1) as collab_movies
            
            // 2. Películas similares a las vistas
            MATCH (u)-[:WATCHED]->(watched:Movie)-[:SIMILAR_TO]->(rec2:Movie)
            WHERE NOT (u)-[:WATCHED]->(rec2)
            
            WITH u, collab_count, collab_movies,
                 COUNT(DISTINCT rec2) as similarity_count, COLLECT(DISTINCT rec2) as similar_movies
            
            // Combinar y rankear
            WITH u, 
                 collab_movies + similar_movies as all_recommendations,
                 collab_count, similarity_count
            
            UNWIND all_recommendations as recommendation
            
            OPTIONAL MATCH (u2:User)-[r:RATED]->(recommendation)
            OPTIONAL MATCH (recommendation)-[:HAS_GENRE]->(g:Genre)
            
            WITH recommendation,
                 COLLECT(DISTINCT g.nombre) as generos,
                 AVG(r.puntuacion) as avg_rating,
                 COUNT(DISTINCT u2) as rating_count
            
            RETURN DISTINCT recommendation.título as película,
                   recommendation.año as año,
                   recommendation.duración as duración,
                   generos as géneros,
                   COALESCE(ROUND(avg_rating * 10) / 10.0, 0) as calificación_promedio,
                   rating_count as calificaciones_totales,
                   rating_count * COALESCE(avg_rating, 7) as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=limit)
            return result
        
        records = self.conn.execute_read(_recommend)
        return [dict(record) for record in records] if records else []
