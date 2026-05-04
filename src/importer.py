"""Importador Python-driven para Neo4j (compatible con AuraDB).

Este importador evita `LOAD CSV` y en su lugar lee CSVs en Python,
envía lotes vía `UNWIND $rows` para ser compatible con bases Neo4j en la nube.
"""
import csv
import os
from typing import List, Dict, Any

from .neo4j_conn import get_connection
from . import schema


class DataImporter:
    """Importa datos de CSV a Neo4j para el dominio de supply-chain."""

    def __init__(self, conn=None):
        self.conn = conn or get_connection()

    def _read_csv(self, path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    def import_suppliers(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            CREATE (s:Supplier {
                id_proveedor: toInteger(row.id_proveedor),
                nombre: row.nombre,
                pais: row.pais,
                rating: CASE WHEN row.rating IS NULL OR row.rating = '' THEN NULL ELSE toFloat(row.rating) END,
                activo: row.activo,
                categorias: row.categorias
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_products(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            CREATE (p:Product {
                id_producto: toInteger(row.id_producto),
                nombre: row.nombre,
                categoria: row.categoria,
                precio: CASE WHEN row.precio IS NULL OR row.precio = '' THEN NULL ELSE toFloat(row.precio) END,
                perecedero: row.perecedero,
                fecha_expiracion: CASE WHEN row.fecha_expiracion IS NULL OR row.fecha_expiracion = '' THEN NULL ELSE row.fecha_expiracion END
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_centers(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            CREATE (c:CentroDistribucion {
                id_centro: toInteger(row.id_centro),
                nombre: row.nombre,
                ciudad: row.ciudad,
                capacidad: CASE WHEN row.capacidad IS NULL OR row.capacidad = '' THEN NULL ELSE toInteger(row.capacidad) END,
                activo: row.activo,
                tipo: row.tipo
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_inventories(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            CREATE (inv:Inventory {
                id_inventario: toInteger(row.id_inventario),
                cantidad: CASE WHEN row.cantidad IS NULL OR row.cantidad = '' THEN NULL ELSE toInteger(row.cantidad) END,
                ubicacion: row.ubicacion,
                capacidad_max: CASE WHEN row.capacidad_max IS NULL OR row.capacidad_max = '' THEN NULL ELSE toInteger(row.capacidad_max) END,
                temperatura_controlada: row.temperatura_controlada,
                fecha_actualizacion: row.fecha_actualizacion
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_transports(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            CREATE (t:Transporte {
                id_transporte: toInteger(row.id_transporte),
                tipo: row.tipo,
                costo: CASE WHEN row.costo IS NULL OR row.costo = '' THEN NULL ELSE toFloat(row.costo) END,
                duracion_dias: CASE WHEN row.duracion_dias IS NULL OR row.duracion_dias = '' THEN NULL ELSE toInteger(row.duracion_dias) END,
                estado: row.estado,
                fecha_salida: row.fecha_salida
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_orders(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            CREATE (o:OrderCompra {
                id_orden: toInteger(row.id_orden),
                fecha_orden: row.fecha_orden,
                estado: row.estado,
                total: CASE WHEN row.total IS NULL OR row.total = '' THEN NULL ELSE toFloat(row.total) END,
                urgente: row.urgente,
                metodo_pago: row.metodo_pago
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_supplies(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (s:Supplier {id_proveedor: toInteger(row.id_proveedor)})
            MATCH (p:Product {id_producto: toInteger(row.id_producto)})
            CREATE (s)-[:SUMINISTRA {fecha: CASE WHEN row.fecha = '' THEN NULL ELSE row.fecha END, costo: CASE WHEN row.costo = '' OR row.costo IS NULL THEN NULL ELSE toFloat(row.costo) END}]->(p)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_includes(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (o:OrderCompra {id_orden: toInteger(row.id_orden)})
            MATCH (p:Product {id_producto: toInteger(row.id_producto)})
            CREATE (o)-[:INCLUYE {cantidad: CASE WHEN row.cantidad = '' OR row.cantidad IS NULL THEN NULL ELSE toInteger(row.cantidad) END, precio_unitario: CASE WHEN row.precio_unitario = '' OR row.precio_unitario IS NULL THEN NULL ELSE toFloat(row.precio_unitario) END, subtotal: CASE WHEN row.subtotal = '' OR row.subtotal IS NULL THEN NULL ELSE toFloat(row.subtotal) END}]->(p)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_stored_in(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (p:Product {id_producto: toInteger(row.id_producto)})
            MATCH (inv:Inventory {id_inventario: toInteger(row.id_inventario)})
            CREATE (p)-[:ALMACENADO_EN {fecha_ingreso: CASE WHEN row.fecha_ingreso = '' THEN NULL ELSE row.fecha_ingreso END, cantidad: CASE WHEN row.cantidad = '' OR row.cantidad IS NULL THEN NULL ELSE toInteger(row.cantidad) END, estado: row.estado}]->(inv)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_sent_by(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (o:OrderCompra {id_orden: toInteger(row.id_orden)})
            MATCH (t:Transporte {id_transporte: toInteger(row.id_transporte)})
            CREATE (o)-[:SE_ENVIA_POR {fecha_envio: CASE WHEN row.fecha_envio = '' THEN NULL ELSE row.fecha_envio END, costo_envio: CASE WHEN row.costo_envio = '' OR row.costo_envio IS NULL THEN NULL ELSE toFloat(row.costo_envio) END, estado: row.estado}]->(t)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_arrives_departs(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (o:OrderCompra {id_orden: toInteger(row.id_orden)})
            MATCH (c:CentroDistribucion {id_centro: toInteger(row.id_centro)})
            CREATE (o)-[:LLEGA_A {fecha_llegada: CASE WHEN row.fecha_llegada = '' THEN NULL ELSE row.fecha_llegada END}]->(c)
            CREATE (o)-[:SALE_DE {fecha_salida: CASE WHEN row.fecha_salida = '' THEN NULL ELSE row.fecha_salida END}]->(c)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_manages(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (c:CentroDistribucion {id_centro: toInteger(row.id_centro)})
            MATCH (inv:Inventory {id_inventario: toInteger(row.id_inventario)})
            CREATE (c)-[:GESTIONA {fecha: CASE WHEN row.fecha = '' THEN NULL ELSE row.fecha END, responsable: row.responsable, estado: row.estado}]->(inv)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_destination(self, csv_path: str) -> int:
        rows = self._read_csv(csv_path)
        if not rows:
            return 0

        def _import(tx):
            query = """
            UNWIND $rows AS row
            MATCH (o:OrderCompra {id_orden: toInteger(row.id_orden)})
            MATCH (c:CentroDistribucion {id_centro: toInteger(row.id_centro)})
            CREATE (o)-[:DESTINO {fecha_entrega: CASE WHEN row.fecha_entrega = '' THEN NULL ELSE row.fecha_entrega END, prioridad: CASE WHEN row.prioridad = '' OR row.prioridad IS NULL THEN NULL ELSE toInteger(row.prioridad) END, estado: row.estado}]->(c)
            RETURN count(*) AS count
            """
            result = tx.run(query, rows=rows)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def create_indexes(self) -> None:
        def _create(tx):
            idxs = [
                "CREATE INDEX IF NOT EXISTS FOR (s:Supplier) ON (s.id_proveedor)",
                "CREATE INDEX IF NOT EXISTS FOR (p:Product) ON (p.id_producto)",
                "CREATE INDEX IF NOT EXISTS FOR (o:OrderCompra) ON (o.id_orden)",
                "CREATE INDEX IF NOT EXISTS FOR (inv:Inventory) ON (inv.id_inventario)",
                "CREATE INDEX IF NOT EXISTS FOR (c:CentroDistribucion) ON (c.id_centro)",
                "CREATE INDEX IF NOT EXISTS FOR (t:Transporte) ON (t.id_transporte)",
            ]
            for q in idxs:
                try:
                    tx.run(q)
                except Exception:
                    pass

        self.conn.execute_write(_create)

    def clear_database(self) -> bool:
        def _clear(tx):
            tx.run("MATCH (n) DETACH DELETE n")
            return True

        return self.conn.execute_write(_clear)


if __name__ == "__main__":
    from .data_generator import DataGenerator

    DataGenerator.generate_all("data")

    importer = DataImporter()
    importer.clear_database()
    importer.create_indexes()

    print("Importando datos...")
    print(f"Proveedores: {importer.import_suppliers('data/suppliers.csv')}")
    print(f"Productos: {importer.import_products('data/products.csv')}")
    print(f"Centros: {importer.import_centers('data/centers.csv')}")
    print(f"Inventarios: {importer.import_inventories('data/inventories.csv')}")
    print(f"Transportes: {importer.import_transports('data/transports.csv')}")
    print(f"Órdenes: {importer.import_orders('data/orders.csv')}")
    print(f"SUMINISTRA: {importer.import_supplies('data/supplies.csv')}")
    print(f"INCLUYE: {importer.import_includes('data/includes.csv')}")
    print(f"ALMACENADO_EN: {importer.import_stored_in('data/stored_in.csv')}")
    print(f"SE_ENVIA_POR: {importer.import_sent_by('data/sent_by.csv')}")
    print(f"LLEGA/SALE: {importer.import_arrives_departs('data/arrives_departs.csv')}")
    print(f"GESTIONA: {importer.import_manages('data/manages.csv')}")
    print(f"DESTINO: {importer.import_destination('data/destination.csv')}")
    print("\nImportación completada!")
