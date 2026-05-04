"""API Flask para el sistema de recomendacion de peliculas.

Proporciona endpoints REST para acceder a todas las funcionalidades.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from .app import MovieRecommendationApp

app = Flask(__name__)
CORS(app)

# Instancia global de la aplicacion
movie_app = MovieRecommendationApp()


# ============ INICIALIZACION ============

@app.route('/api/init', methods=['POST'])
def initialize():
    """Inicializar base de datos."""
    try:
        payload = request.get_json(silent=True) or {}
        stats = movie_app.initialize_database(clear=payload.get('clear', True))
        return jsonify({
            "success": True,
            "message": "Base de datos inicializada",
            "stats": stats
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadisticas del grafo."""
    try:
        stats = movie_app.get_graph_stats()
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ USUARIOS ============

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Obtener datos de un usuario."""
    try:
        user = movie_app.get_user(user_id)
        if user:
            return jsonify({"success": True, "data": user}), 200
        return jsonify({"success": False, "error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users', methods=['GET'])
def list_users():
    """Listar todos los usuarios."""
    try:
        limit = request.args.get('limit', 50, type=int)
        users = movie_app.list_all_users()[:limit]
        return jsonify({"success": True, "data": users}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    """Crear un nuevo usuario."""
    try:
        user_data = request.get_json(silent=True) or {}
        user = movie_app.create_user(user_data)
        return jsonify({"success": True, "data": user}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ PELICULAS ============

@app.route('/api/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Obtener datos de una pelicula."""
    try:
        movie = movie_app.get_movie(movie_id)
        if movie:
            return jsonify({"success": True, "data": movie}), 200
        return jsonify({"success": False, "error": "Pelicula no encontrada"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/movies', methods=['GET'])
def list_movies():
    """Listar todas las peliculas."""
    try:
        limit = request.args.get('limit', 50, type=int)
        movies = movie_app.list_all_movies()[:limit]
        return jsonify({"success": True, "data": movies}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/movies/genre/<genre_name>', methods=['GET'])
def get_movies_by_genre(genre_name):
    """Obtener peliculas de un genero."""
    try:
        movies = movie_app.get_movies_by_genre(genre_name)
        return jsonify({"success": True, "data": movies}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/top-rated-movies', methods=['GET'])
def top_rated():
    """Obtener peliculas mejor calificadas."""
    try:
        limit = request.args.get('limit', 10, type=int)
        movies = movie_app.get_top_rated_movies(limit)
        return jsonify({"success": True, "data": movies}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/trending-movies', methods=['GET'])
def trending():
    """Obtener peliculas tendencia."""
    try:
        limit = request.args.get('limit', 10, type=int)
        movies = movie_app.get_trending_movies(limit)
        return jsonify({"success": True, "data": movies}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ RECOMENDACIONES ============

@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Obtener recomendaciones personalizadas."""
    try:
        strategy = request.args.get('strategy', 'personalized')
        limit = request.args.get('limit', 10, type=int)

        if strategy == 'collaborative':
            recs = movie_app.recommend_collaborative_filtering(user_id, limit)
        elif strategy == 'content':
            recs = movie_app.recommend_by_content(user_id, limit)
        elif strategy == 'genre':
            recs = movie_app.recommend_by_genre(user_id, limit)
        elif strategy == 'actors':
            recs = movie_app.recommend_by_favorite_actors(user_id, limit)
        elif strategy == 'community':
            recs = movie_app.recommend_from_community(user_id, limit)
        else:  # personalized (default)
            recs = movie_app.get_personalized_recommendations(user_id, limit)

        return jsonify({"success": True, "strategy": strategy, "data": recs}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/similar-users/<user_id>', methods=['GET'])
def similar_users(user_id):
    """Obtener usuarios con gustos similares."""
    try:
        users = movie_app.get_user_similar_users(user_id)
        return jsonify({"success": True, "data": users}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/similarity/<user1_id>/<user2_id>', methods=['GET'])
def user_similarity(user1_id, user2_id):
    """Calcular similitud entre dos usuarios."""
    try:
        similarity = movie_app.calculate_user_similarity(user1_id, user2_id)
        return jsonify({"success": True, "data": {"similarity": similarity}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ INTERACCIONES ============

@app.route('/api/users/<user_id>/watch/<movie_id>', methods=['POST'])
def watch_movie(user_id, movie_id):
    """Marcar pelicula como vista."""
    try:
        movie_app.user_watch_movie(user_id, movie_id)
        return jsonify({"success": True, "message": "Pelicula marcada como vista"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users/<user_id>/rate/<movie_id>', methods=['POST'])
def rate_movie(user_id, movie_id):
    """Calificar una pelicula."""
    try:
        payload = request.get_json(silent=True) or {}
        rating = payload.get('rating')
        if not rating or not (1 <= rating <= 10):
            return jsonify({"success": False, "error": "Rating debe estar entre 1 y 10"}), 400

        movie_app.user_rate_movie(user_id, movie_id, rating)
        return jsonify({"success": True, "message": "Pelicula calificada"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users/<user_id>/like/<movie_id>', methods=['POST'])
def like_movie(user_id, movie_id):
    """Marcar pelicula como favorita."""
    try:
        movie_app.user_like_movie(user_id, movie_id)
        return jsonify({"success": True, "message": "Pelicula agregada a favoritos"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users/<user_id>/bookmark/<movie_id>', methods=['POST'])
def bookmark_movie(user_id, movie_id):
    """Agregar pelicula a la lista de ver despues."""
    try:
        payload = request.get_json(silent=True) or {}
        priority = payload.get('priority', 3)
        movie_app.user_bookmark_movie(user_id, movie_id, priority)
        return jsonify({"success": True, "message": "Pelicula agregada a lista de ver"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users/<user_id>/follow/<other_user_id>', methods=['POST'])
def follow_user(user_id, other_user_id):
    """Un usuario sigue a otro."""
    try:
        movie_app.user_follow_user(user_id, other_user_id)
        return jsonify({"success": True, "message": "Usuario seguido"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ CONSULTAS ============

@app.route('/api/directors-stats', methods=['GET'])
def directors_stats():
    """Obtener estadisticas de directores."""
    try:
        stats = movie_app.get_directors_stats()
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/engagement-stats', methods=['GET'])
def engagement_stats():
    """Obtener estadisticas de engagement."""
    try:
        stats = movie_app.get_user_engagement_stats()
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/movies-without-reviews', methods=['GET'])
def movies_without_reviews():
    """Obtener peliculas sin resenas."""
    try:
        limit = request.args.get('limit', 20, type=int)
        movies = movie_app.get_movies_without_reviews()[:limit]
        return jsonify({"success": True, "data": movies}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ HEALTH CHECK ============

@app.route('/api/health', methods=['GET'])
def health():
    """Verificar estado de la API."""
    return jsonify({"success": True, "message": "API is running"}), 200


def run_api(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    """Run the Flask server."""
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run_api(debug=True)
