"""Consultas Cypher para análisis del grafo.

Implementa 6 consultas diferentes como se requiere en la rúbrica.
"""
from typing import List, Dict, Any
from .neo4j_conn import Neo4jConnection
from . import schema


class CypherQueries:
    """Maneja consultas Cypher complejas."""
    
    def __init__(self, conn: Neo4jConnection):
        self.conn = conn
    
    def query_1_movies_by_genre(self, genre_name: str) -> List[Dict]:
        """Consulta 1: Obtener todas las películas de un género específico."""
        def _query(tx):
            cypher = """
            MATCH (g:Genre {nombre: $genre_name})-[:HAS_GENRE]-(m:Movie)
            RETURN m.título as título, m.año as año, m.duración as duración
            ORDER BY m.año DESC
            """
            result = tx.run(cypher, genre_name=genre_name)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_2_user_watchlist_with_actors(self, user_id: str) -> List[Dict]:
        """Consulta 2: Obtener películas guardadas por un usuario con sus actores principales."""
        def _query(tx):
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:BOOKMARKED]->(m:Movie)
            OPTIONAL MATCH (m)<-[:STARS_IN]-(a:Actor)
            RETURN DISTINCT m.título as película, 
                   COLLECT(a.nombre) as actores,
                   m.año as año,
                   m.duración as duración
            ORDER BY película
            """
            result = tx.run(cypher, user_id=user_id)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_3_directors_and_movie_count(self) -> List[Dict]:
        """Consulta 3: Directores con cantidad de películas y presupuesto total."""
        def _query(tx):
            cypher = """
            MATCH (d:Director)-[:DIRECTED_BY]-(m:Movie)
            RETURN d.nombre as director,
                   COUNT(m) as películas_dirigidas,
                   SUM(m.presupuesto) as presupuesto_total,
                   AVG(m.presupuesto) as presupuesto_promedio
            ORDER BY películas_dirigidas DESC
            LIMIT 20
            """
            result = tx.run(cypher)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_4_top_rated_movies(self, limit: int = 10) -> List[Dict]:
        """Consulta 4: Películas mejor calificadas basadas en ratings de usuarios."""
        def _query(tx):
            cypher = """
            MATCH (u:User)-[r:RATED]->(m:Movie)
            RETURN m.título as película,
                   m.año as año,
                   COUNT(r) as total_calificaciones,
                   AVG(r.puntuacion) as calificacion_promedio,
                   MIN(r.puntuacion) as calificacion_minima,
                   MAX(r.puntuacion) as calificacion_maxima
            ORDER BY calificacion_promedio DESC, total_calificaciones DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_5_user_similarity_network(self, user_id: str, depth: int = 2) -> List[Dict]:
        """Consulta 5: Red de usuarios similares basada en películas vistas."""
        def _query(tx):
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:WATCHED]->(m:Movie)<-[:WATCHED]-(other:User)
            WHERE u <> other
            WITH other, COUNT(DISTINCT m) as películas_comunes, 
                 COLLECT(m.título) as películas
            RETURN other.nombre as usuario,
                   other.user_id as user_id,
                   películas_comunes as películas_comunes,
                   películas
            ORDER BY películas_comunes DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=depth * 5)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_6_recommendation_based_on_watched_and_genres(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Consulta 6: Películas recomendadas basadas en géneros de películas vistas.
        
        Algoritmo: 
        - Encontrar géneros de películas que el usuario ha visto
        - Encontrar otras películas en esos géneros que NO ha visto
        - Ordenar por calificación promedio
        """
        def _query(tx):
            cypher = """
            MATCH (u:User {user_id: $user_id})-[:WATCHED]->(watched:Movie)-[:HAS_GENRE]->(g:Genre)
            MATCH (g)-[:HAS_GENRE]-(recommended:Movie)
            WHERE NOT (u)-[:WATCHED]->(recommended) 
              AND NOT (u)-[:RATED]->(recommended)
            OPTIONAL MATCH (u2:User)-[r:RATED]->(recommended)
            WITH recommended, g.nombre as genre, 
                 COUNT(DISTINCT u2) as usuarios_que_califican,
                 AVG(r.puntuacion) as calificacion_promedio
            RETURN DISTINCT recommended.título as película,
                   recommended.año as año,
                   recommended.duración as duración,
                   COLLECT(genre) as géneros,
                   usuarios_que_califican,
                   COALESCE(calificacion_promedio, 0) as calificacion_promedio
            ORDER BY calificacion_promedio DESC, usuarios_que_califican DESC
            LIMIT $limit
            """
            result = tx.run(cypher, user_id=user_id, limit=limit)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_aggregation_actors_by_genre(self) -> List[Dict]:
        """Consulta de agregación: Actores por género de películas."""
        def _query(tx):
            cypher = """
            MATCH (a:Actor)-[:STARS_IN]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            RETURN g.nombre as género,
                   COUNT(DISTINCT a) as cantidad_actores,
                   COUNT(DISTINCT m) as películas,
                   COLLECT(DISTINCT a.nombre) as actores
            ORDER BY cantidad_actores DESC
            """
            result = tx.run(cypher)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
    
    def query_user_engagement_stats(self) -> Dict[str, Any]:
        """Consulta de estadísticas: Engagement de usuarios."""
        def _query(tx):
            cypher = """
            MATCH (u:User)
            OPTIONAL MATCH (u)-[:WATCHED]->(m)
            OPTIONAL MATCH (u)-[:RATED]->(rated)
            OPTIONAL MATCH (u)-[:WROTE_REVIEW]->(rev)
            WITH u, 
                 COUNT(DISTINCT m) as películas_vistas,
                 COUNT(DISTINCT rated) as películas_calificadas,
                 COUNT(DISTINCT rev) as reviews_escritas
            RETURN COUNT(u) as total_usuarios,
                   AVG(películas_vistas) as promedio_vistas,
                   AVG(películas_calificadas) as promedio_calificaciones,
                   AVG(reviews_escritas) as promedio_reviews,
                   MAX(películas_vistas) as max_vistas,
                   MAX(películas_calificadas) as max_calificaciones,
                   MAX(reviews_escritas) as max_reviews
            """
            result = tx.run(cypher)
            return result.single()
        
        record = self.conn.execute_read(_query)
        return dict(record) if record else {}
    
    def query_movies_without_reviews(self) -> List[Dict]:
        """Consulta: Películas sin reseñas."""
        def _query(tx):
            cypher = """
            MATCH (m:Movie)
            WHERE NOT (m)<-[:WROTE_REVIEW]-()
            RETURN m.título as película,
                   m.año as año,
                   m.duración as duración,
                   m.presupuesto as presupuesto
            ORDER BY m.año DESC
            LIMIT 50
            """
            result = tx.run(cypher)
            return result
        
        records = self.conn.execute_read(_query)
        return [dict(record) for record in records] if records else []
