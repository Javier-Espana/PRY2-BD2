"""Pruebas de tipos de datos reales en Neo4j tras importacion."""

import pytest
from src.data_generator import DataGenerator
from src.importer import DataImporter


@pytest.mark.integration
class TestDataTypes:
    """Verifica que los tipos de datos se persistan correctamente."""

    def _mini_import(self, conn):
        importer = DataImporter(conn)
        conn.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
        importer.create_indexes()
        data_dir = DataGenerator.generate_all("data")
        importer.import_suppliers(f"{data_dir}/suppliers.csv")
        importer.import_products(f"{data_dir}/products.csv")
        importer.import_orders(f"{data_dir}/orders.csv")
        importer.import_inventories(f"{data_dir}/inventories.csv")
        importer.import_centers(f"{data_dir}/centers.csv")
        importer.import_transports(f"{data_dir}/transports.csv")
        importer.import_supplies(f"{data_dir}/supplies.csv")
        importer.import_includes(f"{data_dir}/includes.csv")
        importer.import_stored_in(f"{data_dir}/stored_in.csv")
        importer.import_sent_by(f"{data_dir}/sent_by.csv")
        importer.import_arrives_departs(f"{data_dir}/arrives.csv")
        importer.import_manages(f"{data_dir}/manages.csv")
        importer.import_destination(f"{data_dir}/destination.csv")

    def test_integer_type_present(self, conn):
        """Verificar que existen propiedades Integer."""
        self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run(
                "MATCH (s:Supplier) WHERE s.id_proveedor IS NOT NULL "
                "RETURN toInteger(s.id_proveedor) as val LIMIT 1"
            ).single()
        )
        assert result is not None

    def test_float_type_present(self, conn):
        """Verificar que existen propiedades Float."""
        self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run(
                "MATCH (s:Supplier) WHERE s.rating IS NOT NULL "
                "RETURN toFloat(s.rating) as val LIMIT 1"
            ).single()
        )
        assert result is not None

    def test_string_type_present(self, conn):
        """Verificar que existen propiedades String."""
        self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run(
                "MATCH (s:Supplier) WHERE s.nombre IS NOT NULL "
                "RETURN s.nombre as val LIMIT 1"
            ).single()
        )
        assert result is not None

    def test_date_type_present(self, conn):
        """Verificar que existen propiedades Date."""
        self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run(
                "MATCH (o:OrderCompra) WHERE o.fecha_orden IS NOT NULL "
                "RETURN o.fecha_orden as val LIMIT 1"
            ).single()
        )
        assert result is not None
