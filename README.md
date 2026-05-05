# Proyecto: Neo4j — Cadena de Suministro (Supply Chain)

**Estado**: Completado — cubre todos los criterios de la rubrica base

Sistema de cadena de suministros implementado en Neo4j con generacion
de datos, importacion CSV, CRUD completo de nodos y relaciones, 6 consultas
Cypher, 4 analytics de data science y API REST.

## Estructura del Proyecto

```
PRY2-BD2/
├── src/
│   ├── app.py                    # Fachada SupplyChainApp
│   ├── api.py                    # API REST (Flask)
│   ├── console.py                # Consola interactiva con menus
│   ├── demo.py                   # Demo CLI automatizada
│   ├── schema.py                 # Esquema: 6 labels, 11 relaciones
│   ├── crud_operations.py        # CRUD generico reutilizable
│   ├── queries.py                # 5 consultas Cypher
│   ├── recommendation.py         # Analytics engine (Data Science)
│   ├── data_generator.py         # Generador CSV (5,410+ nodos)
│   ├── importer.py               # Importador Python-driven (UNWIND)
│   ├── neo4j_conn.py             # Conexion Neo4j
│   └── config.py                 # Configuracion desde .env
├── tests/
│   ├── conftest.py               # Fixtures compartidos
│   ├── unit/                     # Pruebas sin Neo4j
│   └── integration/              # Pruebas con Neo4j real
├── main.py                       # Entry point unificado
├── requirements.txt
└── README.md
```

## Inicio Rapido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar `.env`

```bash
# Neo4j local
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

Para AuraDB, usa las credenciales de tu instancia (`neo4j+s://...`).

### 3. Verificar conexion

```bash
python main.py --mode check
```

### 4. Inicializar la base de datos

```bash
python main.py --mode init
```

Esto genera +5,400 nodos y +70,000 relaciones, los importa y crea indices.

## Comandos

```bash
# Verificar conexion, stats y grafo conexo
python main.py --mode check

# Verificar si el grafo es conexo
python main.py --mode connected

# Inicializar base de datos (generar + importar)
python main.py --mode init
python main.py --mode init --keep-data   # sin limpiar datos previos

# Consola interactiva con menus (recomendada)
python main.py --mode console

# Demo automatizada (recorre toda la rubrica)
python main.py --mode demo

# API REST + dashboard web
python main.py --mode api
# Abrir: http://localhost:5000/

# Ejecutar tests
python main.py --mode test
```

## Consola Interactiva

```bash
python main.py --mode console
```

Menus navegables con numeros:

- **Menu Principal**: init, stats, CRUD nodos, CRUD relaciones, consultas, analytics, demo automatica, grafo conexo
- **CRUD Nodos**: crear 1/2+ labels, consultar, listar, filtrar, agregar/actualizar/eliminar propiedades, eliminar, agregaciones
- **CRUD Relaciones**: crear con 3+ props, agregar/actualizar/eliminar propiedades, eliminar
- **Consultas**: productos por categoria, inventario, top suppliers, ordenes pendientes, transportes
- **Analytics**: stockouts, reorder, top suppliers por volumen, resumen transportes

## API Endpoints

```
POST   /api/init                              Inicializar BD
GET    /api/stats                             Estadisticas del grafo
GET    /api/suppliers                         Listar proveedores
POST   /api/suppliers                         Crear proveedor
GET    /api/suppliers/<id>                    Detalle proveedor
GET    /api/products                          Listar productos
GET    /api/products/<id>                     Detalle producto
GET    /api/orders                            Listar ordenes
GET    /api/inventories                       Listar inventarios
GET    /api/centers                           Listar centros
GET    /api/transports                        Listar transportes
GET    /api/queries/products-by-category/<c>  Productos por categoria
GET    /api/queries/top-suppliers             Top proveedores rating
GET    /api/queries/pending-orders            Ordenes pendientes
GET    /api/queries/transport-status          Estado transportes
GET    /api/analytics/stockouts               Bajo inventario
GET    /api/analytics/reorder                 Sugerencia reorden
GET    /api/analytics/top-suppliers           Top suppliers volumen
GET    /api/health                            Health check
```

## Tests

```bash
python main.py --mode test
# o directo:
python -m pytest tests/ -v
```

## Rubrica

- 6 labels con 6 propiedades cada una
- 11 tipos de relaciones con 3+ propiedades cada una
- Tipos: String, Integer, Float, Boolean, List, Date
- Carga CSV, 5,410+ nodos, grafo conexo
- CRUD completo de nodos y relaciones
- 6 consultas Cypher funcionales
- 4 analytics de Data Science
- API REST funcional con dashboard HTML
- Consola interactiva con menus
