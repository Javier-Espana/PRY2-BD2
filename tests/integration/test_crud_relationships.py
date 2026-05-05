"""Pruebas de CRUD completo de relaciones via SupplyChainApp."""

import pytest
from src import schema


@pytest.mark.integration
class TestRelationshipCrudComplete:
    """Todas las operaciones CRUD de relaciones exigidas por la rubrica."""

    def _setup_rel_nodes(self, app):
        app.create_supplier({
            "id_proveedor": 99901, "nombre": "R S1", "pais": "GT",
            "rating": 4.0, "activo": "true", "categorias": "Bebidas"
        })
        app.create_product({
            "id_producto": 88801, "nombre": "R P1", "categoria": "Bebidas",
            "precio": 5.0, "perecedero": "false", "fecha_expiracion": ""
        })
        app.create_product({
            "id_producto": 88802, "nombre": "R P2", "categoria": "Bebidas",
            "precio": 8.0, "perecedero": "false", "fecha_expiracion": ""
        })

    def test_create_relationship_with_props(self, app, clean_db):
        """Crear relacion entre 2 nodos con 3+ propiedades."""
        self._setup_rel_nodes(app)
        rel = app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        assert rel is not None

    def test_add_props_to_relationship(self, app, clean_db):
        """Agregar propiedades a una relacion."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        result = app.add_props_to_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES, {"nota": "urgente"}
        )
        assert result is not None

    def test_add_props_to_multiple_relationships(self, app, clean_db):
        """Agregar propiedades a multiples relaciones."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88802,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-02", "costo": 8.0, "estado": "Activo"}
        )
        updated = app.add_props_to_multiple_relationships(
            schema.REL_SUPPLIES, schema.LABEL_SUPPLIER,
            schema.PROP_SUPPLIER_ID, [99901],
            {"lote": "A1"}
        )
        assert updated >= 1

    def test_update_props_in_relationship(self, app, clean_db):
        """Actualizar propiedades de una relacion."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        result = app.update_props_in_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES, {"costo": 12.0}
        )
        assert result is not None

    def test_remove_props_from_relationship(self, app, clean_db):
        """Eliminar propiedades de una relacion."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        app.add_props_to_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES, {"temporal": "borrar"}
        )
        result = app.remove_props_from_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES, ["temporal"]
        )
        assert result is not None

    def test_remove_props_from_multiple_relationships(self, app, clean_db):
        """Eliminar propiedades de multiples relaciones."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        app.add_props_to_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES, {"temp": 1}
        )
        updated = app.remove_props_from_multiple_relationships(
            schema.REL_SUPPLIES, schema.LABEL_SUPPLIER,
            schema.PROP_SUPPLIER_ID, [99901], ["temp"]
        )
        assert updated >= 1

    def test_delete_relationship(self, app, clean_db):
        """Eliminar una relacion."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        deleted = app.delete_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES
        )
        assert deleted is True

    def test_delete_multiple_relationships(self, app, clean_db):
        """Eliminar multiples relaciones."""
        self._setup_rel_nodes(app)
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88801,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 10.5, "estado": "Activo"}
        )
        app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 88802,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-02", "costo": 8.0, "estado": "Activo"}
        )
        deleted = app.delete_multiple_relationships(
            schema.REL_SUPPLIES, schema.LABEL_SUPPLIER,
            schema.PROP_SUPPLIER_ID, [99901]
        )
        assert deleted >= 1
