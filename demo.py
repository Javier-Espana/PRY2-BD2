#!/usr/bin/env python3
"""Script de demostración del Sistema de Recomendación de Películas.

Ejecuta ejemplos de todas las funcionalidades principales del proyecto.
"""

from src.neo4j_project.app import MovieRecommendationApp
import sys


def print_section(title):
    """Imprimir encabezado de sección."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_initialization():
    """Demostración 1: Inicialización de la base de datos."""
    print_section("1. INICIALIZACIÓN DE BASE DE DATOS")
    
    app = MovieRecommendationApp()
    
    print("\n Inicializando base de datos con datos de prueba...")
    stats = app.initialize_database(clear=True)
    
    print("\n Base de datos inicializada exitosamente!")
    total_nodes = sum([stats["users"], stats["movies"], stats["genres"], 
                      stats["actors"], stats["directors"]])
    print(f"\n   Nodos: {total_nodes:,}")
    print(f"   - Usuarios: {stats['users']}")
    print(f"   - Películas: {stats['movies']}")
    print(f"   - Géneros: {stats['genres']}")
    print(f"   - Actores: {stats['actors']}")
    print(f"   - Directores: {stats['directors']}")
    
    return app


def demo_graph_stats(app):
    """Demostración 2: Estadísticas del grafo."""
    print_section("2. ESTADÍSTICAS DEL GRAFO")
    
    stats = app.get_graph_stats()
    
    print("\n Estadísticas Generales:")
    for key, value in stats.items():
        print(f"   {key}: {value:,}")

    connected = app.crud.is_graph_connected()
    print(f"\n Grafo conexo: {connected}")


def demo_crud_operations(app):
    """Demostración 3: Operaciones CRUD."""
    print_section("3. OPERACIONES CRUD")
    
    # CREATE
    print("\n▶ CREATE - Creando nuevos nodos...")
    
    new_user = app.create_user({
        "user_id": "user_demo_001",
        "email": "demo@example.com",
        "nombre": "Usuario Demo",
        "edad": 25,
        "país": "Guatemala",
        "fechaRegistro": "2024-03-15"
    })
    print("    Usuario creado exitosamente")
    
    # READ
    print("\n▶ READ - Leyendo datos...")
    user = app.get_user("user_demo_001")
    if user:
        print(f"    Usuario encontrado: {user['nombre']} ({user['email']})")
    
    # UPDATE
    print("\n▶ UPDATE - Actualizando propiedades...")
    updated = app.update_user("user_demo_001", {"edad": 26, "país": "Estados Unidos"})
    print(f"    Usuario actualizado: {updated['nombre']} ahora tiene {updated['edad']} años")
    
    # DELETE
    print("\n▶ DELETE - Eliminando nodo...")
    deleted = app.delete_user("user_demo_001")
    print(f"    Usuario eliminado: {deleted}")


def demo_queries(app):
    """Demostración 4: Consultas Cypher."""
    print_section("4. CONSULTAS CYPHER")
    
    print("\n Consulta 1: Películas Mejor Calificadas")
    top_movies = app.get_top_rated_movies(3)
    for i, movie in enumerate(top_movies, 1):
        print(f"   {i}. {movie['película']} ({movie['año']})")
        print(f"      Calificación: {movie['calificacion_promedio']}/10")
        print(f"      Votos: {movie['total_calificaciones']}")
    
    print("\n Consulta 2: Directores y Estadísticas")
    directors = app.get_directors_stats()[:3]
    for i, director in enumerate(directors, 1):
        print(f"   {i}. {director['director']} - {director['películas_dirigidas']} películas")
    
    print("\n Consulta 3: Estadísticas de Engagement")
    engagement = app.get_user_engagement_stats()
    print(f"   Total usuarios: {engagement['total_usuarios']}")
    print(f"   Promedio de películas vistas: {engagement['promedio_vistas']:.1f}")
    print(f"   Promedio de calificaciones: {engagement['promedio_calificaciones']:.1f}")
    
    print("\n Consulta 4: Películas por Género")
    action_movies = app.get_movies_by_genre("Acción")
    print(f"   Películas de acción: {len(action_movies)}")
    for movie in action_movies[:3]:
        print(f"   - {movie['título']} ({movie['año']})")


def demo_recommendations(app):
    """Demostración 5: Sistema de Recomendaciones."""
    print_section("5. SISTEMA DE RECOMENDACIONES")
    
    # Usar un usuario que exista
    user_id = "user_0001"
    
    print(f"\n Generando recomendaciones para {user_id}...\n")
    
    print("▶ Estrategia 1: Filtrado Colaborativo")
    try:
        recs = app.recommend_collaborative_filtering(user_id, limit=3)
        if recs:
            for i, rec in enumerate(recs, 1):
                print(f"   {i}. {rec['película']} ({rec['año']})")
        else:
            print("   (Sin datos disponibles)")
    except:
        print("   (Sin suficientes datos)")
    
    print("\n▶ Estrategia 2: Recomendaciones Tendencia")
    trends = app.get_trending_movies(3)
    for i, movie in enumerate(trends, 1):
        print(f"   {i}. {movie['película']} - {movie['vistas_ultimos_30_dias']} vistas")
    
    print("\n▶ Estrategia 3: Por Afinidad de Género")
    try:
        genre_recs = app.recommend_by_genre(user_id, limit=3)
        if genre_recs:
            for i, rec in enumerate(genre_recs, 1):
                print(f"   {i}. {rec['película']} ({rec['año']})")
        else:
            print("   (Sin datos disponibles)")
    except:
        print("   (Sin suficientes datos)")
    
    print("\n▶ Estrategia 4: Recomendación Personalizada (Híbrida)")
    try:
        personalized = app.get_personalized_recommendations(user_id, limit=3)
        if personalized:
            for i, rec in enumerate(personalized, 1):
                print(f"   {i}. {rec['película']} ({rec['año']})")
        else:
            print("   (Sin datos disponibles)")
    except:
        print("   (Sin suficientes datos)")


def demo_interactions(app):
    """Demostración 6: Interacciones de Usuario."""
    print_section("6. INTERACCIONES DE USUARIO")
    
    user_id = "user_0001"
    movie_id = "movie_00001"
    
    print(f"\n Usuario {user_id} interactuando con películas...")
    
    # Watch
    print(f"\n▶ Marcar película como vista...")
    try:
        app.user_watch_movie(user_id, movie_id)
        print(f"    Película {movie_id} marcada como vista")
    except:
        print(f"    No se pudo marcar (relación puede ya existir)")
    
    # Rate
    print(f"\n▶ Calificar película (8/10)...")
    try:
        app.user_rate_movie(user_id, movie_id, rating=8)
        print(f"    Película calificada con 8/10")
    except:
        print(f"    No se pudo calificar (relación puede ya existir)")
    
    # Like
    print(f"\n▶ Marcar como favorita...")
    try:
        app.user_like_movie(user_id, movie_id)
        print(f"    Película agregada a favoritos")
    except:
        print(f"    No se pudo agregar (relación puede ya existir)")


def main():
    """Función principal."""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  SISTEMA DE RECOMENDACIÓN DE PELÍCULAS - DEMO                     ║
║  Proyecto 2 - Base de Datos 2 (CC3089)                            ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # 1. Inicialización
        app = demo_initialization()
        
        # 2. Estadísticas
        demo_graph_stats(app)
        
        # 3. CRUD
        demo_crud_operations(app)
        
        # 4. Consultas
        demo_queries(app)
        
        # 5. Recomendaciones
        demo_recommendations(app)
        
        # 6. Interacciones
        demo_interactions(app)
        
        # Cierre
        print_section(" DEMOSTRACIÓN COMPLETADA")
        print("\n Todas las funcionalidades se ejecutaron exitosamente!")
        print("\nPara más información, ver: README.md")
        
        app.close()
        
    except Exception as e:
        print(f"\n Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
