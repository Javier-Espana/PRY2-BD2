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
│   ├── demo.py                   # Demo CLI orientada a rubrica
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
├── main.py                       # Entry point: api, demo, init
├── requirements.txt
└── README.md
```

## Inicio Rapido

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Crear `.env`:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

3. Inicializar BD:

```bash
python main.py --mode init
```

4. Iniciar API:

```bash
python main.py --mode api
# Dashboard: http://localhost:5000/
```

5. Demo:

```bash
python main.py --mode demo
```

## Endpoints principales

```
POST   /api/init                          Inicializar BD
GET    /api/stats                         Estadisticas del grafo
GET    /api/suppliers                     Listar proveedores
POST   /api/suppliers                     Crear proveedor
GET    /api/suppliers/<id>                Detalle proveedor
GET    /api/products                      Listar productos
GET    /api/products/<id>                 Detalle producto
GET    /api/orders                        Listar ordenes
GET    /api/inventories                   Listar inventarios
GET    /api/centers                       Listar centros
GET    /api/transports                    Listar transportes
GET    /api/queries/products-by-category/<c>  Productos por categoria
GET    /api/queries/top-suppliers         Top proveedores
GET    /api/queries/pending-orders        Ordenes pendientes
GET    /api/queries/transport-status      Estado transportes
GET    /api/analytics/stockouts           Bajo inventario
GET    /api/analytics/reorder             Sugerencia reorden
GET    /api/analytics/top-suppliers       Top suppliers volumen
GET    /api/health                        Health check
```

## Tests

```bash
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
