"""Analytics Engine para Supply Chain: consultas de negocio.

Se ajustan las consultas a las etiquetas/propiedades definidas en schema.py.
"""

from typing import List, Dict, Any
from .neo4j_conn import Neo4jConnection


class AnalyticsEngine:
    def __init__(self, conn: Neo4jConnection):
        self.conn = conn

    def detect_stockouts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Detectar productos con bajo inventario."""
        def _query(tx):
            cypher = """
            MATCH (p:Product)
            OPTIONAL MATCH (p)-[:ALMACENADO_EN]->(inv:Inventory)
            WITH p, COALESCE(SUM(inv.cantidad), 0) AS total_stock
            RETURN p.id_producto AS id_producto, p.nombre AS nombre,
                   total_stock AS inventario_total
            ORDER BY total_stock ASC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return [dict(r) for r in result]

        return self.conn.execute_read(_query)

    def suggest_reorder(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Sugerir reorden basandose en demanda historica (ultimos 90 dias)."""
        def _query(tx):
            cypher = """
            MATCH (p:Product)<-[inc:INCLUYE]-(o:OrderCompra)
            WHERE o.fecha_orden IS NOT NULL
              AND o.fecha_orden >= date() - duration('P90D')
            WITH p, AVG(inc.cantidad) AS avg_demand
            WHERE avg_demand IS NOT NULL
            RETURN p.id_producto AS id_producto, p.nombre AS nombre,
                   avg_demand AS demanda_promedio
            ORDER BY demanda_promedio DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return [dict(r) for r in result]

        return self.conn.execute_read(_query)

    def top_suppliers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Ranquear proveedores por volumen suministrado."""
        def _query(tx):
            cypher = """
            MATCH (s:Supplier)-[r:SUMINISTRA]->(p:Product)
            WITH s, COUNT(r) AS productos_suministrados
            RETURN s.id_proveedor AS id_proveedor, s.nombre AS nombre,
                   productos_suministrados
            ORDER BY productos_suministrados DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return [dict(r) for r in result]

        return self.conn.execute_read(_query)

    def transport_overview(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Resumen de transportes (conteo y estados)."""
        def _query(tx):
            cypher = """
            MATCH (t:Transporte)
            RETURN t.id_transporte AS id_transporte, t.tipo AS tipo,
                   t.estado AS estado
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return [dict(r) for r in result]

        return self.conn.execute_read(_query)
