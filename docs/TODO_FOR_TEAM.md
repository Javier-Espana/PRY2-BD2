# Tareas pendientes y guía rápida para el equipo

Objetivo: empezar la implementación del Proyecto 2 (Neo4j) siguiendo las instrucciones del PDF `docs/Proyecto 2 - Neo4j.pdf`.

Prioridad alta
- Revisar el PDF principal y el PDF anotado en `docs/` y extraer requisitos funcionales y esquemas de datos.
- Definir el modelo de grafo (etiquetas, propiedades y relaciones) en un documento `docs/model.md`.
- Completar `src/neo4j_project/config.py` para usar variables de entorno seguras y documentar cómo obtener credenciales.

Desarrollo (dividir entre compañeros)
- Implementar funciones de importación específicas por fuente de datos (CSV, JSON). Asignar 1 archivo por persona.
- Añadir mapeos de esquema y pruebas unitarias para cada importador.
- Crear scripts de ejemplo en `scripts/` para transformar datos de entrada al formato esperado.

Infra / DevOps
- Probar ejecución local con una instancia de Neo4j (docker-compose sugerido). Crear `docker-compose.yml` con servicio `neo4j` y credenciales de ejemplo.
- Añadir CI básico que instale dependencias y ejecute tests (GitHub Actions o similar).

Documentación y entrega
- Redactar `docs/usage.md` con pasos para ejecutar localmente y cargar datos de ejemplo.
- Preparar una sección `docs/evaluation.md` con criterios y comandos para que el profesor valide (ej.: consultas de verificación).

Notas
- No subir credenciales reales. Usar `.env` local y documentar las variables necesarias (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`).
