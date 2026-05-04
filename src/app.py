"""Aplicación principal para la Cadena de Suministros.

Proporciona funciones de inicialización, importación y operaciones CRUD
mínimas para interactuar con el modelo supply-chain definido en `schema.py`.
"""

from typing import Dict, List, Any, Optional
from .neo4j_conn import get_connection
from .crud_operations import CrudOperations
from .data_generator import DataGenerator
from .importer import DataImporter
from . import schema


class SupplyChainApp:
    """Aplicación principal para operaciones básicas de cadena de suministros."""

    def __init__(self):
        self.conn = get_connection()
        self.crud = CrudOperations(self.conn)
        self.importer = DataImporter(self.conn)

    def initialize_database(self, clear: bool = True, data_dir: str = "data") -> Dict[str, int]:
        """Generar datos de ejemplo e importarlos en Neo4j.

        Devuelve un diccionario con el conteo de nodos/relaciones importados.
        """
        self.conn.verify_connectivity()

        if clear:
            self.importer.clear_database()

        DataGenerator.generate_all(data_dir)
        self.importer.create_indexes()

        stats = {
            "suppliers": self.importer.import_suppliers(f"{data_dir}/suppliers.csv"),
            "products": self.importer.import_products(f"{data_dir}/products.csv"),
            "orders": self.importer.import_orders(f"{data_dir}/orders.csv"),
            "inventories": self.importer.import_inventories(f"{data_dir}/inventories.csv"),
            "centers": self.importer.import_centers(f"{data_dir}/centers.csv"),
            "transports": self.importer.import_transports(f"{data_dir}/transports.csv"),
            "supplies": self.importer.import_supplies(f"{data_dir}/supplies.csv"),
            "includes": self.importer.import_includes(f"{data_dir}/includes.csv"),
            "stored_in": self.importer.import_stored_in(f"{data_dir}/stored_in.csv"),
            "sent_by": self.importer.import_sent_by(f"{data_dir}/sent_by.csv"),
            "arrives": self.importer.import_arrives_departs(f"{data_dir}/arrives_departs.csv"),
        }

        return stats

    # ==== CRUD Helpers (nodos) ====

    def create_supplier(self, supplier: Dict) -> Dict:
        return self.crud.create_node_single_label(schema.LABEL_SUPPLIER, supplier)

    def get_supplier(self, supplier_id: int) -> Optional[Dict]:
        return self.crud.get_node_by_id(schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, supplier_id)

    def list_suppliers(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_SUPPLIER)[:limit]

    def create_product(self, product: Dict) -> Dict:
        return self.crud.create_node_single_label(schema.LABEL_PRODUCT, product)

    def get_product(self, product_id: int) -> Optional[Dict]:
        return self.crud.get_node_by_id(schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, product_id)

    def list_products(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_PRODUCT)[:limit]

    def list_orders(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_ORDER)[:limit]

    def list_centers(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_DISTRIBUTION_CENTER)[:limit]

    def list_inventories(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_INVENTORY)[:limit]

    def list_transports(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_TRANSPORT)[:limit]

    def get_graph_stats(self) -> Dict[str, Any]:
        return {
            "total_suppliers": self.crud.count_nodes(schema.LABEL_SUPPLIER),
            "total_products": self.crud.count_nodes(schema.LABEL_PRODUCT),
            "total_orders": self.crud.count_nodes(schema.LABEL_ORDER),
            "total_inventories": self.crud.count_nodes(schema.LABEL_INVENTORY),
            "total_centers": self.crud.count_nodes(schema.LABEL_DISTRIBUTION_CENTER),
            "total_transports": self.crud.count_nodes(schema.LABEL_TRANSPORT),
            "total_nodes": self.crud.count_all_nodes(),
            "total_relationships": self.crud.count_relationships(),
        }

    def close(self):
        self.conn.close()


def main():
    print("Aplicación Cadena de Suministros - Neo4j\n")
    app = SupplyChainApp()
    try:
        print("Inicializando base de datos de ejemplo (esto puede tardar)...")
        stats = app.initialize_database(clear=True)
        print("Importación completada. Estadísticas:")
        for k, v in stats.items():
            print(f"  {k}: {v}")

        print("\nEstadísticas del grafo:")
        gstats = app.get_graph_stats()
        for k, v in gstats.items():
            print(f"  {k}: {v}")

    except RuntimeError as exc:
        print(str(exc))
    finally:
        app.close()


if __name__ == "__main__":
    main()
