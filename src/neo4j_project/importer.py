"""Importador de datos CSV a Neo4j para el dominio de cadena de suministros.

Carga datos de archivos CSV y crea nodos/relaciones relevantes para Supply Chain.
"""
from .neo4j_conn import get_connection


class DataImporter:
    """Importa datos de CSV a Neo4j (supply-chain)."""

    def __init__(self, conn=None):
        self.conn = conn or get_connection()

    def import_suppliers(self, csv_path: str) -> int:
        """Importar proveedores desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (s:Supplier {
                supplier_id: row.supplier_id,
                nombre: row.nombre,
                rating: toFloat(row.rating),
                pais: row.pais,
                contacto: row.contacto
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_products(self, csv_path: str) -> int:
        """Importar productos desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (p:Product {
                product_id: row.product_id,
                nombre: row.nombre,
                categoria: row.categoria,
                cantidad_disponible: toInteger(row.cantidad_disponible),
                stock_minimo: toInteger(row.stock_minimo),
                dias_entrega: toInteger(row.dias_entrega)
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_centers(self, csv_path: str) -> int:
        """Importar centros de distribución desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (c:DistributionCenter {
                center_id: row.center_id,
                nombre: row.nombre,
                direccion: row.direccion,
                ciudad: row.ciudad
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_inventories(self, csv_path: str) -> int:
        """Importar inventarios desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (p:Product {product_id: row.product_id})
            MATCH (c:DistributionCenter {center_id: row.center_id})
            CREATE (inv:Inventory {
                inventory_id: row.inventory_id,
                cantidad: toInteger(row.cantidad),
                fecha_actualizacion: date(row.fecha_actualizacion)
            })
            CREATE (p)-[:STORED_IN]->(inv)
            CREATE (inv)-[:LOCATED_AT]->(c)
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_transports(self, csv_path: str) -> int:
        """Importar vehículos/transporte desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (t:Transport {
                transport_id: row.transport_id,
                tipo: row.tipo,
                capacidad: toInteger(row.capacidad),
                estado: row.estado
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_orders(self, csv_path: str) -> int:
        """Importar órdenes desde CSV."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (o:Order {
                order_id: row.order_id,
                fecha: date(row.fecha),
                cantidad: toInteger(row.cantidad),
                estado: row.estado
            })
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    # Relaciones
    def import_supplies(self, csv_path: str) -> int:
        """Importar relaciones SUMINISTRA (Supplier -> Product)."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (s:Supplier {supplier_id: row.supplier_id})
            MATCH (p:Product {product_id: row.product_id})
            CREATE (s)-[:SUPPLIES {precio: toFloat(row.precio)}]->(p)
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_includes(self, csv_path: str) -> int:
        """Importar relaciones INCLUYE (Order -> Product)."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (o:Order {order_id: row.order_id})
            MATCH (p:Product {product_id: row.product_id})
            CREATE (o)-[:INCLUDES {cantidad: toInteger(row.cantidad)}]->(p)
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_stored_in(self, csv_path: str) -> int:
        """Importar relaciones ALMACENADO_EN (Inventory -> Center)."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (inv:Inventory {inventory_id: row.inventory_id})
            MATCH (c:DistributionCenter {center_id: row.center_id})
            CREATE (inv)-[:STORED_IN]->(c)
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_sent_by(self, csv_path: str) -> int:
        """Importar relaciones SE_ENVIA_POR (Order -> Transport)."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (o:Order {order_id: row.order_id})
            MATCH (t:Transport {transport_id: row.transport_id})
            CREATE (o)-[:SENT_BY {fecha_envio: date(row.fecha_envio)}]->(t)
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_arrives_departs(self, csv_path: str) -> int:
        """Importar relaciones LLEGA_A/SALE_DE entre Orden y Centro."""
        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (o:Order {order_id: row.order_id})
            MATCH (c:DistributionCenter {center_id: row.center_id})
            CREATE (o)-[:ARRIVES_AT {fecha_llegada: date(row.fecha_llegada)}]->(c)
            CREATE (o)-[:DEPARTS_FROM {fecha_salida: date(row.fecha_salida)}]->(c)
            RETURN count(*) AS count
            """
            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def create_indexes(self) -> None:
        """Crear índices en las propiedades principales."""
        def _create(tx):
            indexes = [
                "CREATE INDEX supplier_id FOR (s:Supplier) ON (s.supplier_id)",
                "CREATE INDEX product_id FOR (p:Product) ON (p.product_id)",
                "CREATE INDEX order_id FOR (o:Order) ON (o.order_id)",
                "CREATE INDEX inventory_id FOR (inv:Inventory) ON (inv.inventory_id)",
                "CREATE INDEX center_id FOR (c:DistributionCenter) ON (c.center_id)",
                "CREATE INDEX transport_id FOR (t:Transport) ON (t.transport_id)",
            ]
            for idx in indexes:
                try:
                    tx.run(idx)
                except Exception:
                    pass  # índice podría ya existir

        self.conn.execute_write(_create)

    def clear_database(self) -> bool:
        """Limpiar la base de datos."""
        def _clear(tx):
            tx.run("MATCH (n) DETACH DELETE n")
            return True

        return self.conn.execute_write(_clear)


if __name__ == "__main__":
    # Ejemplo de uso: generar/importar datos supply-chain
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
    print(f"SUMPLISTAS: {importer.import_supplies('data/supplies.csv')}")
    print(f"INCLUYE: {importer.import_includes('data/includes.csv')}")
    print(f"ALMACENADO_EN: {importer.import_stored_in('data/stored_in.csv')}")
    print(f"SE_ENVIA_POR: {importer.import_sent_by('data/sent_by.csv')}")
    print(f"LLEGA/SALE: {importer.import_arrives_departs('data/arrives_departs.csv')}")
    print("\nImportación completada!")
