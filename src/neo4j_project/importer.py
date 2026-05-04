"""Importador de datos CSV a Neo4j.

Carga datos de archivos CSV y establece relaciones en la base de datos.
"""
from .neo4j_conn import get_connection


class DataImporter:
    """Importa datos de CSV a Neo4j."""
    
    def __init__(self, conn=None):
        self.conn = conn or get_connection()
    
    def import_users(self, csv_path: str) -> int:
        """Importar usuarios desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            CREATE (u:User {
                user_id: row.user_id,
                email: row.email,
                nombre: row.nombre,
                edad: toInteger(row.edad),
                país: row.país,
                fechaRegistro: date(row.fechaRegistro)
            })
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_movies(self, csv_path: str) -> int:
        """Importar películas desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            CREATE (m:Movie {
                movie_id: row.movie_id,
                título: row.título,
                año: toInteger(row.año),
                duración: toInteger(row.duración),
                presupuesto: toFloat(row.presupuesto),
                descripción: row.descripción
            })
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_genres(self, csv_path: str) -> int:
        """Importar géneros desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            CREATE (g:Genre {
                genre_id: row.genre_id,
                nombre: row.nombre,
                descripción: row.descripción,
                películas_totales: toInteger(row.películas_totales),
                popularidad: toFloat(row.popularidad)
            })
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_actors(self, csv_path: str) -> int:
        """Importar actores desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            CREATE (a:Actor {
                actor_id: row.actor_id,
                nombre: row.nombre,
                fechaNacimiento: date(row.fechaNacimiento),
                nacionalidad: row.nacionalidad,
                biografía: row.biografía,
                premios: CASE WHEN row.premios = '' THEN [] ELSE split(row.premios, '|') END
            })
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_directors(self, csv_path: str) -> int:
        """Importar directores desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            CREATE (d:Director {
                director_id: row.director_id,
                nombre: row.nombre,
                fechaNacimiento: date(row.fechaNacimiento),
                nacionalidad: row.nacionalidad,
                películas_dirigidas: toInteger(row.películas_dirigidas),
                bio: row.bio
            })
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_watched_relationships(self, csv_path: str) -> int:
        """Importar relaciones WATCHED."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (u:User {user_id: row.user_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (u)-[:WATCHED {
                fecha: date(row.fecha),
                duracion_visto: toInteger(row.duracion_visto),
                completado: row.completado = 'true'
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_rated_relationships(self, csv_path: str) -> int:
        """Importar relaciones RATED."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (u:User {user_id: row.user_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (u)-[:RATED {
                puntuacion: toInteger(row.puntuacion),
                fecha: date(row.fecha),
                útil: row.útil = 'true'
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_liked_relationships(self, csv_path: str) -> int:
        """Importar relaciones LIKED."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (u:User {user_id: row.user_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (u)-[:LIKED {
                fecha: date(row.fecha),
                motivación: row.motivación,
                intensidad: toInteger(row.intensidad)
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_bookmarked_relationships(self, csv_path: str) -> int:
        """Importar relaciones BOOKMARKED."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (u:User {user_id: row.user_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (u)-[:BOOKMARKED {
                fecha: date(row.fecha),
                prioridad: toInteger(row.prioridad),
                recordatorio: row.recordatorio = 'true'
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_has_genre_relationships(self, csv_path: str) -> int:
        """Importar relaciones HAS_GENRE."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (m:Movie {movie_id: row.movie_id})
            MATCH (g:Genre {genre_id: row.genre_id})
            CREATE (m)-[:HAS_GENRE {
                es_principal: row.es_principal = 'true',
                peso: toFloat(row.peso),
                origen: row.origen
            }]->(g)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_stars_in_relationships(self, csv_path: str) -> int:
        """Importar relaciones STARS_IN."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (a:Actor {actor_id: row.actor_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (a)-[:STARS_IN {
                rol: row.rol,
                orden: toInteger(row.orden),
                pantalla_time: toFloat(row.pantalla_time)
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_directed_by_relationships(self, csv_path: str) -> int:
        """Importar relaciones DIRECTED_BY."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (d:Director {director_id: row.director_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (d)-[:DIRECTED_BY {
                año_filmacion: toInteger(row.año_filmacion),
                versión: row.versión,
                credito_principal: row.credito_principal = 'true'
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_wrote_review_relationships(self, csv_path: str) -> int:
        """Importar relaciones WROTE_REVIEW."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (u:User {user_id: row.user_id})
            MATCH (m:Movie {movie_id: row.movie_id})
            CREATE (u)-[:WROTE_REVIEW {
                fecha: date(row.fecha),
                editado: row.editado = 'true',
                spoiler: row.spoiler = 'true'
            }]->(m)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_follows_relationships(self, csv_path: str) -> int:
        """Importar relaciones FOLLOWS."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (u1:User {user_id: row.user_id})
            MATCH (u2:User {user_id: row.other_user_id})
            CREATE (u1)-[:FOLLOWS {
                fecha: date(row.fecha),
                notificaciones: row.notificaciones = 'true',
                nivel_interaccion: toInteger(row.nivel_interaccion)
            }]->(u2)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def import_similar_to_relationships(self, csv_path: str) -> int:
        """Importar relaciones SIMILAR_TO."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file as row
            MATCH (m1:Movie {movie_id: row.movie_id})
            MATCH (m2:Movie {movie_id: row.similar_movie_id})
            CREATE (m1)-[:SIMILAR_TO {
                similitud: toFloat(row.similitud),
                mismo_genero: row.mismo_genero = 'true',
                origen: row.origen
            }]->(m2)
            RETURN count(*) as count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]
        
        return self.conn.execute_write(_import)
    
    def create_indexes(self) -> None:
        """Crear índices en las propiedades principales."""
        def _create(tx):
            indexes = [
                "CREATE INDEX user_id FOR (u:User) ON (u.user_id)",
                "CREATE INDEX user_email FOR (u:User) ON (u.email)",
                "CREATE INDEX movie_id FOR (m:Movie) ON (m.movie_id)",
                "CREATE INDEX genre_id FOR (g:Genre) ON (g.genre_id)",
                "CREATE INDEX actor_id FOR (a:Actor) ON (a.actor_id)",
                "CREATE INDEX director_id FOR (d:Director) ON (d.director_id)",
            ]
            for idx in indexes:
                try:
                    tx.run(idx)
                except:
                    pass  # El índice podría ya existir
        
        self.conn.execute_write(_create)
    
    def clear_database(self) -> bool:
        """Limpiar la base de datos."""
        def _clear(tx):
            tx.run("MATCH (n) DETACH DELETE n")
            return True
        
        return self.conn.execute_write(_clear)


if __name__ == "__main__":
    # Ejemplo de uso
    from .data_generator import DataGenerator
    
    # Generar datos
    DataGenerator.generate_all("data")
    
    # Importar
    importer = DataImporter()
    importer.clear_database()
    importer.create_indexes()
    
    print("Importando datos...")
    print(f"Usuarios: {importer.import_users('data/users.csv')}")
    print(f"Películas: {importer.import_movies('data/movies.csv')}")
    print(f"Géneros: {importer.import_genres('data/genres.csv')}")
    print(f"Actores: {importer.import_actors('data/actors.csv')}")
    print(f"Directores: {importer.import_directors('data/directors.csv')}")
    print(f"WATCHED: {importer.import_watched_relationships('data/watched.csv')}")
    print(f"RATED: {importer.import_rated_relationships('data/rated.csv')}")
    print(f"LIKED: {importer.import_liked_relationships('data/liked.csv')}")
    print(f"BOOKMARKED: {importer.import_bookmarked_relationships('data/bookmarked.csv')}")
    print(f"HAS_GENRE: {importer.import_has_genre_relationships('data/has_genre.csv')}")
    print(f"STARS_IN: {importer.import_stars_in_relationships('data/stars_in.csv')}")
    print(f"DIRECTED_BY: {importer.import_directed_by_relationships('data/directed_by.csv')}")
    print(f"WROTE_REVIEW: {importer.import_wrote_review_relationships('data/wrote_review.csv')}")
    print(f"FOLLOWS: {importer.import_follows_relationships('data/follows.csv')}")
    print(f"SIMILAR_TO: {importer.import_similar_to_relationships('data/similar_to.csv')}")
    print("\n Importación completada!")
