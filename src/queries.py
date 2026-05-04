"""Consultas Cypher para el dominio de Cadena de Suministros.

Contiene consultas útiles para análisis: productos por categoría,
estado de inventarios, proveedores top, órdenes pendientes y estado de transportes.
"""

from typing import List, Dict, Any
from .neo4j_conn import Neo4jConnection
from . import schema


class CypherQueries:
    """Consultas Cypher orientadas a supply-chain."""

    def __init__(self, conn: Neo4jConnection):
        self.conn = conn

    def products_by_category(self, category: str) -> List[Dict]:
        def _query(tx):
            cypher = """
            MATCH (p:Product {categoria: $category})
            RETURN p.id_producto as id_producto, p.nombre as nombre, p.precio as precio, p.perecedero as perecedero
            ORDER BY p.nombre
            """
            return tx.run(cypher, category=category)

        records = self.conn.execute_read(_query)
        return [dict(r) for r in records] if records else []

    def inventory_status_for_product(self, product_id: int) -> List[Dict]:
        def _query(tx):
            cypher = """
            MATCH (p:Product {id_producto: $product_id})-[:ALMACENADO_EN]->(i:Inventory)
            RETURN i.id_inventario as id_inventario, i.ubicacion as ubicacion, i.cantidad as cantidad, i.capacidad_max as capacidad_max
            """
            return tx.run(cypher, product_id=product_id)

        records = self.conn.execute_read(_query)
        return [dict(r) for r in records] if records else []

    def top_suppliers_by_rating(self, limit: int = 10) -> List[Dict]:
        def _query(tx):
            cypher = """
            MATCH (s:Supplier)
            RETURN s.id_proveedor as id_proveedor, s.nombre as nombre, s.pais as pais, s.rating as rating
            ORDER BY s.rating DESC
            LIMIT $limit
            """
            return tx.run(cypher, limit=limit)

        records = self.conn.execute_read(_query)
        return [dict(r) for r in records] if records else []

    def pending_orders(self, limit: int = 50) -> List[Dict]:
        def _query(tx):
            cypher = """
            MATCH (o:OrderCompra {estado: 'PENDIENTE'})
            RETURN o.id_orden as id_orden, o.fecha_orden as fecha_orden, o.total as total, o.urgente as urgente
            ORDER BY o.fecha_orden DESC
            LIMIT $limit
            """
            return tx.run(cypher, limit=limit)

        records = self.conn.execute_read(_query)
        return [dict(r) for r in records] if records else []

    def transport_status(self, limit: int = 50) -> List[Dict]:
        def _query(tx):
            cypher = """
            MATCH (t:Transporte)
            RETURN t.id_transporte as id_transporte, t.tipo as tipo, t.estado as estado, t.fecha_salida as fecha_salida
            ORDER BY t.fecha_salida DESC
            LIMIT $limit
            """
            return tx.run(cypher, limit=limit)

        records = self.conn.execute_read(_query)
        return [dict(r) for r in records] if records else []
