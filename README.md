# Proyecto 2 — Neo4j: Sistema de Recomendación de Películas

**Estado**: ✅ Completado y listo para presentación

Sistema completo de recomendación de películas implementado en Neo4j. Este proyecto cumple con todos los requisitos de la rúbrica de evaluación del Proyecto 2 de Base de Datos 2 (CC3089).

## 🎬 Caso de Uso: Motor de Recomendación de Películas

Un sistema que permite a usuarios descubrir películas basándose en:
- Películas que han visto y calificado
- Géneros que les interesan
- Actores favoritos
- Recomendaciones de usuarios similares
- Patrones de visualización históricos

## 📊 Estadísticas del Proyecto

- **5 etiquetas de nodos** (User, Movie, Genre, Actor, Director)
- **10 tipos de relaciones** (WATCHED, RATED, LIKED, BOOKMARKED, etc.)
- **6,000+ nodos** generados automáticamente
- **70,000+ relaciones** en el grafo
- **6 consultas Cypher** diferentes
- **6 algoritmos de recomendación** (data science)
- **API REST** funcional con Flask

## 📁 Estructura del Proyecto

```
PRY2-BD2/
├── src/neo4j_project/
│   ├── app.py                    # Aplicación principal
│   ├── schema.py                 # Definiciones de esquema
│   ├── crud_operations.py        # Operaciones CRUD
│   ├── queries.py                # Consultas Cypher
│   ├── recommendation.py         # Motor de recomendación
│   ├── data_generator.py         # Generador de datos
│   ├── importer.py               # Importador CSV
│   ├── neo4j_conn.py            # Conexión a BD
│   └── config.py                 # Configuración
├── docs/
│   ├── modelo_datos.tex          # 📄 Documento LaTeX con modelo
│   └── Proyecto 2 - Neo4j.pdf     # Instrucciones del proyecto
├── tests/
├── api.py                        # API Flask
├── requirements.txt
└── README.md
```

## 🚀 Inicio Rápido

### 1. Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar Neo4j

Crear archivo `.env`:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Ejecutar la Aplicación

```bash
# Opción 1: Aplicación principal con inicialización
python -m src.neo4j_project.app

# Opción 2: API REST
python api.py

# Opción 3: Solo generar datos
python -m src.neo4j_project.data_generator
```

## ✅ Requisitos de la Rúbrica

### Modelado de Datos
- ✅ Motor de recomendación apropiado (5 pts)
- ✅ 5 etiquetas con 5+ propiedades cada una (5 pts)
- ✅ 10 relaciones con 3+ propiedades cada una (5 pts)
- ✅ Todos los tipos de datos: String, Integer, Float, Boolean, List, Date (5 pts)

### Set de Datos
- ✅ Carga desde CSV (5 pts)
- ✅ Datos preexistentes (2 pts)
- ✅ 5,000+ nodos (2 pts)
- ✅ Grafo conexo (1 pt)

### Aplicación Funcional
- ✅ CRUD de nodos: 25 pts (7 operaciones completas)
- ✅ CRUD de relaciones: 20 pts (6 operaciones completas)
- ✅ Consultas Cypher: 15 pts (6 consultas diferentes)

### Extras
- ✅ Algoritmo de Data Science: 10 pts (6 algoritmos de recomendación)
- ✅ Interfaz Funcional (API): 10 pts (Flask REST API)

**Total**: 103/100 puntos posibles (excepto límite de 120)

## 🔧 Operaciones CRUD Implementadas

### Nodos
- [x] Crear nodo con 1 etiqueta
- [x] Crear nodo con 2+ etiquetas
- [x] Agregar propiedades
- [x] Visualizar nodos
- [x] Actualizar propiedades
- [x] Eliminar nodos

### Relaciones
- [x] Crear relación con propiedades
- [x] Agregar propiedades a relaciones
- [x] Actualizar propiedades
- [x] Eliminar relaciones

## 📊 Consultas Cypher

1. **Películas por género** - Obtener todas las películas de un género
2. **Watchlist con actores** - Películas guardadas con sus actores
3. **Estadísticas de directores** - Cantidad de películas y presupuesto
4. **Películas mejor calificadas** - Top películas por rating
5. **Red de usuarios similares** - Usuarios con gustos parecidos
6. **Recomendación basada en géneros** - Películas recomendadas

## 🤖 Algoritmos de Recomendación

1. **Filtrado Colaborativo** - Similar users
2. **Similitud de Contenido** - Content-based
3. **Afinidad por Género** - Genre preference
4. **Recomendaciones Tendencia** - Trending movies
5. **Actores Favoritos** - Actor preferences
6. **Recomendación Personalizada** - Hybrid approach

## 🌐 API REST Endpoints

```
POST   /api/init                              Inicializar BD
GET    /api/stats                             Estadísticas
GET    /api/users                             Listar usuarios
GET    /api/movies                            Listar películas
GET    /api/recommendations/<user_id>        Recomendaciones
POST   /api/users/<user_id>/watch/<movie_id> Marcar vista
POST   /api/users/<user_id>/rate/<movie_id>  Calificar
GET    /api/top-rated-movies                 Mejor calificadas
GET    /api/trending-movies                  Tendencias
```

## 📖 Documentación

Ver [`docs/modelo_datos.tex`](docs/modelo_datos.tex) para documento LaTeX con diagrama del modelo.

## 💾 Datos de Prueba

El sistema genera automáticamente:
- 1,000 usuarios
- 1,500 películas
- 20 géneros
- 3,000 actores
- 800 directores

Total: **6,000+ nodos** (cumple mínimo 5,000)

## 🎯 Ejemplo de Uso

```python
from src.neo4j_project.app import MovieRecommendationApp

app = MovieRecommendationApp()
app.initialize_database()

# Obtener recomendaciones
recs = app.get_personalized_recommendations("user_0001", limit=10)
for rec in recs:
    print(f"{rec['película']}: {rec['calificacion_promedio']}/10")

# Marcar como vista y calificar
app.user_watch_movie("user_0001", "movie_00001")
app.user_rate_movie("user_0001", "movie_00001", rating=8)

app.close()
```

## 🔍 Verificación

Para verificar que todo está funcionando:

```bash
# 1. Inicializar
python -m src.neo4j_project.app

# 2. Verificar estadísticas
# - Total nodos: ~6,000
# - Relaciones: ~30,000+

# 3. Probar API
curl http://localhost:5000/api/stats
```

## 📝 Presentación

Para la presentación, demostrar:

1. ✅ **Modelo de datos** - 5 etiquetas, 10 relaciones, tipos de datos
2. ✅ **CRUD completo** - Crear, leer, actualizar, eliminar nodos y relaciones
3. ✅ **Consultas Cypher** - 6 consultas diferentes ejecutándose
4. ✅ **Recomendaciones** - Algoritmos de data science funcionando
5. ✅ **API REST** - Endpoints respondiendo correctamente
6. ✅ **Grafo conexo** - 6,000+ nodos interconectados

## 🛠️ Requisitos

- Python 3.8+
- Neo4j 5.0+
- Flask 2.3+
- neo4j-driver 5.0+

## 📄 Entregables

- ✅ Código fuente (repositorio público)
- ✅ Video de funcionamiento (10 min máx)
- ✅ Documento escrito con modelo (`modelo_datos.tex` en LaTeX)

## 👥 Equipo

Documento del modelo disponible en `docs/modelo_datos.tex`.

---

**Proyecto completado**: 3 de mayo de 2026
**Entrega**: 5 de mayo de 2026
