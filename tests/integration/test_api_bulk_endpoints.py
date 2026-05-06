import src.api as api
from src import schema


def test_bulk_update_nodes_http_roundtrip(monkeypatch, app, clean_db):
    monkeypatch.setattr(api, 'sc_app', app)
    client = api.app.test_client()

    app.create_supplier({
        'id_proveedor': 91001, 'nombre': 'S1', 'pais': 'GT',
        'rating': 3.5, 'activo': 'true', 'categorias': 'Bebidas'
    })
    app.create_supplier({
        'id_proveedor': 91002, 'nombre': 'S2', 'pais': 'GT',
        'rating': 4.0, 'activo': 'true', 'categorias': 'Alimentos'
    })

    resp = client.post('/api/nodes/Supplier/bulk/update', json={
        'filter_prop': 'pais',
        'filter_values': ['GT'],
        'properties': {'verificado': True},
    })

    assert resp.status_code == 200
    assert resp.json['updated'] == 2


def test_bulk_delete_relationships_http_roundtrip(monkeypatch, app, clean_db):
    monkeypatch.setattr(api, 'sc_app', app)
    client = api.app.test_client()

    app.create_supplier({
        'id_proveedor': 92001, 'nombre': 'RS1', 'pais': 'GT',
        'rating': 4.0, 'activo': 'true', 'categorias': 'Bebidas'
    })
    app.create_product({
        'id_producto': 93001, 'nombre': 'RP1', 'categoria': 'Bebidas',
        'precio': 10.0, 'perecedero': 'false', 'fecha_expiracion': ''
    })
    app.create_product({
        'id_producto': 93002, 'nombre': 'RP2', 'categoria': 'Bebidas',
        'precio': 12.0, 'perecedero': 'false', 'fecha_expiracion': ''
    })

    app.crud.create_relationship(
        schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 92001,
        schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 93001,
        schema.REL_SUPPLIES,
        {'fecha': '2026-05-01', 'costo': 10.0, 'estado': 'ACTIVO'}
    )
    app.crud.create_relationship(
        schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 92001,
        schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 93002,
        schema.REL_SUPPLIES,
        {'fecha': '2026-05-02', 'costo': 12.0, 'estado': 'ACTIVO'}
    )

    resp = client.post('/api/relationships/bulk/delete', json={
        'rel_type': schema.REL_SUPPLIES,
        'filter_label': schema.LABEL_SUPPLIER,
        'filter_prop': schema.PROP_SUPPLIER_ID,
        'filter_values': [92001],
    })

    assert resp.status_code == 200
    assert resp.json['deleted'] >= 1
