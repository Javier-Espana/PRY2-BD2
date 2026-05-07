import pytest


def test_create_and_get_supplier(monkeypatch, app, clean_db, test_supplier_data):
    """Integration: create supplier via API and retrieve it (uses real Neo4j connection from fixtures)."""
    import src.api as api

    # use the fixture SupplyChainApp instance as the sc_app used by the Flask module
    monkeypatch.setattr(api, 'sc_app', app)
    client = api.app.test_client()

    # create supplier
    resp = client.post('/api/suppliers', json=test_supplier_data)
    assert resp.status_code == 201
    data = resp.json.get('data')
    assert data is not None
    # id_proveedor should be present in returned data (from props)
    assert str(test_supplier_data['id_proveedor']) in str(data.values()) or 'id_proveedor' in str(data)

    # retrieve supplier
    resp2 = client.get(f"/api/suppliers/{test_supplier_data['id_proveedor']}")
    assert resp2.status_code == 200
    got = resp2.json.get('data')
    assert got is not None
    assert int(got.get('id_proveedor') or got.get('id')) == test_supplier_data['id_proveedor']


def test_invalid_delete_id_returns_400(monkeypatch, app):
    import src.api as api
    monkeypatch.setattr(api, 'sc_app', app)
    client = api.app.test_client()
    # invalid id values like 'undefined' should be rejected
    resp = client.delete('/api/nodes/Supplier/undefined')
    assert resp.status_code == 400
