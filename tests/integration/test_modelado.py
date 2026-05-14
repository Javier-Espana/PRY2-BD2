"""Pruebas de integracion: validan modelado en Neo4j real."""

import pytest
from src.data_generator import DataGenerator
from src.importer import DataImporter


@pytest.mark.integration
class TestImportedLabels:
    """Verifica que los labels existen en la BD tras importar."""

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
        return importer

    def test_supplier_label_exists(self, conn):
        imp = self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run("MATCH (n:Supplier) RETURN count(n) as c").single()
        )
        assert result["c"] >= 200

    def test_product_label_exists(self, conn):
        imp = self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run("MATCH (n:Product) RETURN count(n) as c").single()
        )
        assert result["c"] >= 1500

    def test_order_label_exists(self, conn):
        imp = self._mini_import(conn)
        result = conn.execute_read(
            lambda tx: tx.run("MATCH (n:OrderCompra) RETURN count(n) as c").single()
        )
        assert result["c"] >= 1500

    def test_relationships_imported(self, conn):
        imp = self._mini_import(conn)
        rels = ["SUMINISTRA", "INCLUYE", "ALMACENADO_EN",
                "SE_ENVIA_POR", "LLEGA_A", "SALE_DE",
                "GESTIONA", "DESTINO"]
        for rel in rels:
            result = conn.execute_read(
                lambda tx, r=rel: tx.run(
                    f"MATCH ()-[r:{r}]->() RETURN count(r) as c"
                ).single()
            )
            assert result["c"] > 0, f"Relacion {rel} no tiene registros importados"
