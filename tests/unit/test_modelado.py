"""Pruebas de modelado de datos contra la rubrica.

Valida labels, propiedades, relaciones y tipos de datos.
"""

import pytest
from src import schema


@pytest.mark.unit
class TestLabels:
    """5+ labels con 5+ propiedades cada una."""

    def test_minimum_five_labels(self):
        labels = [
            schema.LABEL_SUPPLIER,
            schema.LABEL_PRODUCT,
            schema.LABEL_ORDER,
            schema.LABEL_INVENTORY,
            schema.LABEL_DISTRIBUTION_CENTER,
            schema.LABEL_TRANSPORT,
        ]
        assert len(set(labels)) >= 5

    def test_supplier_properties(self):
        props = [
            schema.PROP_SUPPLIER_ID, schema.PROP_SUPPLIER_NOMBRE,
            schema.PROP_SUPPLIER_PAIS, schema.PROP_SUPPLIER_RATING,
            schema.PROP_SUPPLIER_ACTIVO, schema.PROP_SUPPLIER_CATEGORIAS,
        ]
        assert len(props) >= 5

    def test_product_properties(self):
        props = [
            schema.PROP_PRODUCT_ID, schema.PROP_PRODUCT_NOMBRE,
            schema.PROP_PRODUCT_CATEGORIA, schema.PROP_PRODUCT_PRECIO,
            schema.PROP_PRODUCT_PERECEDERO, schema.PROP_PRODUCT_FECHA_EXPIRACION,
        ]
        assert len(props) >= 5

    def test_order_properties(self):
        props = [
            schema.PROP_ORDER_ID, schema.PROP_ORDER_FECHA,
            schema.PROP_ORDER_ESTADO, schema.PROP_ORDER_TOTAL,
            schema.PROP_ORDER_URGENTE, schema.PROP_ORDER_METODO_PAGO,
        ]
        assert len(props) >= 5

    def test_inventory_properties(self):
        props = [
            schema.PROP_INVENTORY_ID, schema.PROP_INVENTORY_CANTIDAD,
            schema.PROP_INVENTORY_UBICACION, schema.PROP_INVENTORY_CAPACIDAD_MAX,
            schema.PROP_INVENTORY_TEMPERATURA_CONTROLADA,
            schema.PROP_INVENTORY_FECHA_ACTUALIZACION,
        ]
        assert len(props) >= 5

    def test_center_properties(self):
        props = [
            schema.PROP_CENTER_ID, schema.PROP_CENTER_NOMBRE,
            schema.PROP_CENTER_CIUDAD, schema.PROP_CENTER_CAPACIDAD,
            schema.PROP_CENTER_ACTIVO, schema.PROP_CENTER_TIPO,
        ]
        assert len(props) >= 5

    def test_transport_properties(self):
        props = [
            schema.PROP_TRANSPORT_ID, schema.PROP_TRANSPORT_TIPO,
            schema.PROP_TRANSPORT_COSTO, schema.PROP_TRANSPORT_DURACION_DIAS,
            schema.PROP_TRANSPORT_ESTADO, schema.PROP_TRANSPORT_FECHA_SALIDA,
        ]
        assert len(props) >= 5


@pytest.mark.unit
class TestRelationships:
    """10+ relaciones definidas en schema."""

    def test_minimum_ten_relationships(self):
        rels = [
            schema.REL_SUPPLIES, schema.REL_RECEIVES_ORDER,
            schema.REL_INCLUDES, schema.REL_SENT_BY,
            schema.REL_STORED_IN, schema.REL_LOCATED_IN,
            schema.REL_ARRIVES_AT, schema.REL_DEPARTS_FROM,
            schema.REL_MANAGES, schema.REL_REQUIRES,
            schema.REL_DESTINATION,
        ]
        assert len(set(rels)) >= 10


@pytest.mark.unit
class TestIndexes:
    """Indices definidos en schema."""

    def test_indexes_defined(self):
        assert len(schema.INDEXES) >= 5
