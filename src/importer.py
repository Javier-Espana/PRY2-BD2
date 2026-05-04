"""Importador de datos CSV a Neo4j para la Cadena de Suministros.

Implementa importadores básicos para proveedores, productos, órdenes,
inventarios, centros de distribución y transportes, así como las
relaciones principales definidas en el planteamiento.
"""

from .neo4j_conn import get_connection


class DataImporter:
    """Importa datos de CSV a Neo4j para el dominio de supply-chain."""

    def __init__(self, conn=None):
        self.conn = conn or get_connection()

    def import_suppliers(self, csv_path: str) -> int:
        """Importar proveedores desde CSV."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (:Supplier {
                id_proveedor: toInteger(row.id_proveedor),
                nombre: row.nombre,
                pais: row.pais,
                rating: toFloat(row.rating),
                activo: row.activo = 'true',
                categorias: CASE WHEN row.categorias = '' THEN [] ELSE split(row.categorias, '|') END
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
            CREATE (:Product {
                id_producto: toInteger(row.id_producto),
                nombre: row.nombre,
                categoria: row.categoria,
                precio: toFloat(row.precio),
                perecedero: row.perecedero = 'true',
                fecha_expiracion: CASE WHEN row.fecha_expiracion = '' THEN null ELSE date(row.fecha_expiracion) END
            })
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_orders(self, csv_path: str) -> int:
        """Importar órdenes de compra desde CSV."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (:OrderCompra {
                id_orden: toInteger(row.id_orden),
                fecha_orden: date(row.fecha_orden),
                estado: row.estado,
                total: toFloat(row.total),
                urgente: row.urgente = 'true',
                metodo_pago: row.metodo_pago
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
            CREATE (:Inventory {
                id_inventario: toInteger(row.id_inventario),
                cantidad: toInteger(row.cantidad),
                ubicacion: row.ubicacion,
                capacidad_max: toInteger(row.capacidad_max),
                temperatura_controlada: row.temperatura_controlada = 'true',
                fecha_actualizacion: CASE WHEN row.fecha_actualizacion = '' THEN null ELSE date(row.fecha_actualizacion) END
            })
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_transports(self, csv_path: str) -> int:
        """Importar medios de transporte desde CSV."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            CREATE (:Transporte {
                id_transporte: toInteger(row.id_transporte),
                tipo: row.tipo,
                costo: toFloat(row.costo),
                duracion_dias: toInteger(row.duracion_dias),
                estado: row.estado,
                fecha_salida: CASE WHEN row.fecha_salida = '' THEN null ELSE date(row.fecha_salida) END
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
            CREATE (:CentroDistribucion {
                id_centro: toInteger(row.id_centro),
                nombre: row.nombre,
                ciudad: row.ciudad,
                capacidad: toInteger(row.capacidad),
                activo: row.activo = 'true',
                tipo: row.tipo
            })
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    # Relaciones principales
    def import_supplies(self, csv_path: str) -> int:
        """Importar relaciones SUMINISTRA (Supplier -> Product)."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (s:Supplier {id_proveedor: toInteger(row.id_proveedor)})
            MATCH (p:Product {id_producto: toInteger(row.id_producto)})
            CREATE (s)-[:SUMINISTRA { fecha: CASE WHEN row.fecha = '' THEN null ELSE date(row.fecha) END, costo: toFloat(row.costo) }]->(p)
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_includes(self, csv_path: str) -> int:
        """Importar relaciones INCLUYE (OrderCompra -> Product)."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (o:OrderCompra {id_orden: toInteger(row.id_orden)})
            MATCH (p:Product {id_producto: toInteger(row.id_producto)})
            CREATE (o)-[:INCLUYE { cantidad: toInteger(row.cantidad), precio_unitario: toFloat(row.precio_unitario), subtotal: toFloat(row.subtotal) }]->(p)
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_stored_in(self, csv_path: str) -> int:
        """Importar relaciones ALMACENADO_EN (Product -> Inventory)."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (p:Product {id_producto: toInteger(row.id_producto)})
            MATCH (i:Inventory {id_inventario: toInteger(row.id_inventario)})
            CREATE (p)-[:ALMACENADO_EN { fecha_ingreso: CASE WHEN row.fecha_ingreso = '' THEN null ELSE date(row.fecha_ingreso) END, cantidad: toInteger(row.cantidad), estado: row.estado }]->(i)
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_sent_by(self, csv_path: str) -> int:
        """Importar relaciones SE_ENVIA_POR (OrderCompra -> Transporte)."""

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (o:OrderCompra {id_orden: toInteger(row.id_orden)})
            MATCH (t:Transporte {id_transporte: toInteger(row.id_transporte)})
            CREATE (o)-[:SE_ENVIA_POR { fecha_envio: CASE WHEN row.fecha_envio = '' THEN null ELSE date(row.fecha_envio) END, costo_envio: toFloat(row.costo_envio), estado: row.estado }]->(t)
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def import_arrives_departs(self, csv_path: str) -> int:
        """Importar relaciones LLEGA_A / SALE_DE (Transporte <-> CentroDistribucion).

        CSV debe contener campos: id_transporte, id_centro, fecha_llegada, tiempo_real, fecha_salida, tiempo_estimado, estado
        Esta función crea relaciones LLEGA_A y SALE_DE según estén presentes las columnas.
        """

        def _import(tx):
            query = """
            LOAD CSV WITH HEADERS FROM "file:///" + $file AS row
            MATCH (t:Transporte {id_transporte: toInteger(row.id_transporte)})
            MATCH (c:CentroDistribucion {id_centro: toInteger(row.id_centro)})
            FOREACH(_ IN CASE WHEN row.fecha_llegada <> '' THEN [1] ELSE [] END |
                CREATE (t)-[:LLEGA_A { fecha_llegada: date(row.fecha_llegada), tiempo_real: toInteger(row.tiempo_real) }]->(c)
            )
            FOREACH(_ IN CASE WHEN row.fecha_salida <> '' THEN [1] ELSE [] END |
                CREATE (t)-[:SALE_DE { fecha_salida: date(row.fecha_salida), tiempo_estimado: toInteger(row.tiempo_estimado), estado: row.estado }]->(c)
            )
            RETURN count(*) AS count
            """

            result = tx.run(query, file=csv_path)
            return result.single()["count"]

        return self.conn.execute_write(_import)

    def create_indexes(self) -> None:
        """Crear índices en las propiedades principales del modelo supply-chain."""

        def _create(tx):
            indexes = [
                "CREATE INDEX supplier_id FOR (s:Supplier) ON (s.id_proveedor)",
                "CREATE INDEX product_id FOR (p:Product) ON (p.id_producto)",
                "CREATE INDEX order_id FOR (o:OrderCompra) ON (o.id_orden)",
                "CREATE INDEX inventory_id FOR (i:Inventory) ON (i.id_inventario)",
                "CREATE INDEX center_id FOR (c:CentroDistribucion) ON (c.id_centro)",
                "CREATE INDEX transport_id FOR (t:Transporte) ON (t.id_transporte)",
            ]
            for idx in indexes:
                try:
                    tx.run(idx)
                except Exception:
                    pass

        self.conn.execute_write(_create)

    def clear_database(self) -> bool:
        """Limpiar la base de datos."""

        def _clear(tx):
            tx.run("MATCH (n) DETACH DELETE n")
            return True

        return self.conn.execute_write(_clear)


if __name__ == "__main__":
    # Ejemplo de uso mínimo para generar/insertar datos de ejemplo.
    from .data_generator import DataGenerator

    DataGenerator.generate_all("data")

    importer = DataImporter()
    importer.clear_database()
    importer.create_indexes()

    print("Importando datos de cadena de suministros...")
    print(f"Proveedores: {importer.import_suppliers('data/suppliers.csv')}")
    print(f"Productos: {importer.import_products('data/products.csv')}")
    print(f"Órdenes: {importer.import_orders('data/orders.csv')}")
    print(f"Inventarios: {importer.import_inventories('data/inventories.csv')}")
    print(f"Centros: {importer.import_centers('data/centers.csv')}")
    print(f"Transportes: {importer.import_transports('data/transports.csv')}")
    print("Relaciones: ")
    print(f"SUMINISTRA: {importer.import_supplies('data/supplies.csv')}")
    print(f"INCLUYE: {importer.import_includes('data/includes.csv')}")
    print(f"ALMACENADO_EN: {importer.import_stored_in('data/stored_in.csv')}")
    print(f"SE_ENVIA_POR: {importer.import_sent_by('data/sent_by.csv')}")
    print(f"LLEGA/SALE: {importer.import_arrives_departs('data/arrives_departs.csv')}")
    print("\n Importación completada!")
