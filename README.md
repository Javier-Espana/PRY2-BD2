# Neo4j Supply Chain — PRY2-BD2


### Vídeo: https://youtu.be/JCF7pjkjz5Y

### Documento Etapa 1: docs\Proyecto 2 - Planteamiento.pdf




Sistema de cadena de suministros (bebidas/distribución) sobre Neo4j con API REST, dashboard web y consola interactiva. Cubre todos los criterios de la rúbrica CC3089.

## Setup

```bash
pip install -r requirements.txt
```

Crea `.env` (copia `.env.example`):

```
NEO4J_URI=neo4j+s://<host>
NEO4J_USER=neo4j
NEO4J_PASSWORD=<password>
NEO4J_DATABASE=neo4j
```

## Comandos

| Comando                           | Descripción                                              |
| --------------------------------- | --------------------------------------------------------- |
| `python main.py --mode check`   | Verificar conexión y estadísticas                       |
| `python main.py --mode init`    | Generar e importar 5,400+ nodos                           |
| `python main.py --mode api`     | Iniciar API REST + dashboard en `http://localhost:5000` |
| `python main.py --mode console` | Consola interactiva con menús                            |
| `python main.py --mode demo`    | Demo automatizada de toda la rúbrica                     |
| `python main.py --mode test`    | Ejecutar suite de tests                                   |

## API Endpoints

**Base:** `http://localhost:5000`

### Nodos genéricos

| Método    | Ruta                                          | Descripción                                 |
| ---------- | --------------------------------------------- | -------------------------------------------- |
| `POST`   | `/api/nodes`                                | Crear nodo (1 ó 2+ labels, con propiedades) |
| `GET`    | `/api/nodes/<label>`                        | Listar nodos por label                       |
| `GET`    | `/api/nodes/<label>/<id>`                   | Obtener nodo por ID                          |
| `PATCH`  | `/api/nodes/<label>/<id>`                   | Agregar/actualizar propiedades               |
| `DELETE` | `/api/nodes/<label>/<id>`                   | Eliminar nodo                                |
| `POST`   | `/api/nodes/<label>/<id>/remove-properties` | Eliminar propiedades específicas            |
| `POST`   | `/api/nodes/<label>/bulk/update`            | Actualizar props en múltiples nodos         |
| `POST`   | `/api/nodes/<label>/bulk/delete`            | Eliminar múltiples nodos                    |
| `POST`   | `/api/nodes/<label>/bulk/remove-properties` | Eliminar props de múltiples nodos           |
| `GET`    | `/api/nodes/<label>/aggregations`           | COUNT / AVG / MAX / MIN / SUM                |

### Entidades específicas

`GET/POST /api/suppliers` · `GET/DELETE /api/suppliers/<id>`
`GET/POST /api/products` · `GET/DELETE /api/products/<id>`
`GET/POST /api/orders` · `GET/POST /api/inventories`
`GET/POST /api/centers` · `GET/POST /api/transports`

### Relaciones

| Método    | Ruta                                          | Descripción                              |
| ---------- | --------------------------------------------- | ----------------------------------------- |
| `POST`   | `/api/relationships`                        | Crear relación con ≥3 propiedades       |
| `PATCH`  | `/api/relationships`                        | Agregar/actualizar propiedades            |
| `DELETE` | `/api/relationships`                        | Eliminar relación                        |
| `POST`   | `/api/relationships/remove-properties`      | Eliminar props de relación               |
| `POST`   | `/api/relationships/bulk/update`            | Actualizar props en múltiples relaciones |
| `POST`   | `/api/relationships/bulk/remove-properties` | Eliminar props de múltiples relaciones   |
| `POST`   | `/api/relationships/bulk/delete`            | Eliminar múltiples relaciones            |

### Consultas y analytics

| Ruta                                            | Descripción                    |
| ----------------------------------------------- | ------------------------------- |
| `GET /api/queries/products-by-category/<cat>` | Productos por categoría        |
| `GET /api/queries/top-suppliers`              | Top proveedores por rating      |
| `GET /api/queries/pending-orders`             | Órdenes pendientes             |
| `GET /api/queries/transport-status`           | Estado de transportes           |
| `GET /api/queries/inventory-for-product/<id>` | Inventario por producto         |
| `GET /api/analytics/stockouts`                | Detección de quiebres de stock |
| `GET /api/analytics/reorder`                  | Sugerencias de reorden          |
| `GET /api/analytics/top-suppliers`            | Top proveedores por volumen     |
| `GET /api/analytics/transport-overview`       | Resumen de transportes          |
| `GET /api/stats`                              | Estadísticas del grafo         |
| `POST /api/init`                              | Inicializar base de datos       |

## Rúbrica cubierta

| Categoría   | Criterio                                                               | ✓ |
| ------------ | ---------------------------------------------------------------------- | -- |
| Modelado     | Caso de uso: cadena de suministros                                     | ✓ |
| Modelado     | 6 labels distintas con 6+ propiedades cada una                         | ✓ |
| Modelado     | 11 tipos de relaciones con 3+ propiedades                              | ✓ |
| Modelado     | Todos los tipos de datos (String, Float, Integer, Boolean, List, Date) | ✓ |
| Set de datos | Carga CSV (5,410+ nodos, grafo conexo)                                 | ✓ |
| App          | Crear nodo con 1 label                                                 | ✓ |
| App          | Crear nodo con 2+ labels                                               | ✓ |
| App          | Crear nodo con 5+ propiedades                                          | ✓ |
| App          | Visualización de nodos (1, muchos, agregados)                         | ✓ |
| App          | Gestión de propiedades en nodos (add/update/remove single y bulk)     | ✓ |
| App          | Creación de relación con 3+ propiedades                              | ✓ |
| App          | Gestión de relaciones (add/update/remove single y bulk)               | ✓ |
| App          | Eliminación de nodos (1 y múltiples)                                 | ✓ |
| App          | Eliminación de relaciones (1 y múltiples)                            | ✓ |
| App          | 6 consultas Cypher parametrizables                                     | ✓ |
| Extras       | 4 algoritmos de Data Science                                           | ✓ |
| Extras       | Interfaz gráfica (dashboard web funcional)                            | ✓ |
