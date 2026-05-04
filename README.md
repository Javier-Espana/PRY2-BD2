# Proyecto: Neo4j — Cadena de Suministro (Supply Chain)

**Estado**: En progreso — reestructurado a dominio de cadena de suministros

Este repositorio implementa un modelo de dominio para la cadena de suministros
usando Neo4j. Provee utilidades para generar datos de ejemplo, importar desde CSV,
realizar operaciones CRUD básicas, y exponer una API REST mínima para explorar
entidades clave (proveedores, productos, órdenes, inventarios, centros y transporte).

## Estructura del Proyecto

```
PRY2-BD2/
├── src/
│   ├── app.py                    # Aplicación principal (SupplyChainApp)
│   ├── api.py                    # API REST (Flask)
│   ├── demo.py                   # Demo CLI
│   ├── schema.py                 # Definiciones de esquema
│   ├── crud_operations.py        # Operaciones CRUD reutilizables
│   ├── queries.py                # Consultas Cypher específicas
│   ├── recommendation.py         # Motor de análisis / analytics
│   ├── data_generator.py         # Generador de datos CSV (supply-chain)
│   ├── importer.py               # Importador CSV -> Neo4j (supply-chain)
│   ├── neo4j_conn.py             # Wrapper de conexión a Neo4j
│   └── config.py                 # Carga de `.env`
├── docs/
│   ├── modelo_datos.tex          # Documento LaTeX con modelo
├── tests/
├── main.py                       # Punto de entrada único (lazy imports)
├── requirements.txt
└── README.md
```

## Inicio Rápido

1. Crear y activar un entorno virtual e instalar dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Crear un archivo `.env` en la raíz con las credenciales (no subir este archivo):

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

3. Inicializar la base de datos con datos de ejemplo (genera CSV y los importa):

```bash
python main.py --mode init
```

4. Iniciar la API REST:

```bash
python main.py --mode api
# Acceder a: http://localhost:5000/api/
```

5. Ejecutar la demo local (sin Flask):

```bash
python main.py --mode demo
```

## Endpoints principales (ejemplos)

POST   /api/init                Inicializar BD (genera e importa CSV)
GET    /api/stats               Estadísticas del grafo
GET    /api/suppliers           Listar proveedores
GET    /api/suppliers/<id>      Detalle proveedor
GET    /api/products            Listar productos
GET    /api/products/<id>       Detalle producto
GET    /api/orders              Listar órdenes
GET    /api/inventories         Listar inventarios
GET    /api/centers             Listar centros de distribución
GET    /api/transports          Listar transportes
GET    /api/health              Estado de la aplicación

Consulta `src/api.py` para más rutas.

## Notas de seguridad

- Las credenciales se deben mantener en `.env` y **no** subir al repositorio.
- `.gitignore` ya incluye `.env`.

## Verificación rápida

1. Asegúrate de que Neo4j esté accesible y que `.env` tenga valores correctos.
2. Ejecuta `python main.py --mode init` y revisa la salida para confirmar que
   la importación terminó sin errores.
3. Inicia la API y prueba `GET /api/stats`.

Ejemplo:

```bash
python main.py --mode init
python main.py --mode api
curl http://localhost:5000/api/stats
```

## Tests

`tests/test_connection.py` contiene una prueba básica de humo que verifica
que las variables de entorno están configuradas.

## Documentación adicional

Ver [docs/modelo_datos.tex](docs/modelo_datos.tex) para el modelo de datos en LaTeX.

---

Si quieres, puedo ahora ejecutar una verificación de conectividad contra Neo4j
usando las credenciales en `.env` (esperando 60 segundos antes de conectar),
o bien puedo proceder a actualizar/ejecutar pruebas adicionales. Indica qué
prefieres que haga a continuación.
