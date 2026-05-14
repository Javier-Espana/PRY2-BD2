"""Pruebas de set de datos: conectividad y volumen."""

import pytest
from src.data_generator import DataGenerator
from src.importer import DataImporter
from src.crud_operations import CrudOperations


@pytest.mark.integration
class TestDataSet:
    """Set de datos: 5000+ nodos y grafo conexo."""

    def _full_import(self, conn):
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

    def test_total_nodes_above_5000(self, conn):
        """El dataset completo debe tener 5000+ nodos."""
        self._full_import(conn)
        crud = CrudOperations(conn)
        total = crud.count_all_nodes()
        assert total >= 5000, f"Solo hay {total} nodos, se requieren 5000+"

    def test_graph_is_connected(self, conn):
        """El grafo completo debe ser conexo."""
        self._full_import(conn)
        crud = CrudOperations(conn)
        assert crud.is_graph_connected(), (
            "El grafo NO es conexo. La rubrica exige grafo conexo."
        )
