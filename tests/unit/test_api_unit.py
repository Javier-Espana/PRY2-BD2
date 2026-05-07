import json
import pytest
from types import SimpleNamespace

import src.api as api


def test_health_endpoint():
    client = api.app.test_client()
    resp = client.get('/api/health')
    assert resp.status_code == 200
    assert resp.json.get('success') is True


def test_create_node_missing_labels(monkeypatch):
    # ensure sc_app is present but create_node will be rejected due to missing labels
    fake = SimpleNamespace(crud=SimpleNamespace())
    monkeypatch.setattr(api, 'sc_app', fake)
    client = api.app.test_client()
    resp = client.post('/api/nodes', json={})
    assert resp.status_code == 400


def test_create_node_calls_crud_single_label(monkeypatch):
    called = {}

    def fake_create(label, properties):
        called['label'] = label
        called['properties'] = properties
        return {'dummy': True}

    fake_crud = SimpleNamespace(create_node_single_label=fake_create,
                                create_node_multi_label=lambda l, p: None)
    monkeypatch.setattr(api, 'sc_app', SimpleNamespace(crud=fake_crud))

    client = api.app.test_client()
    payload = {'labels': ['Supplier'], 'properties': {'id_proveedor': 555}}
    resp = client.post('/api/nodes', json=payload)
    assert resp.status_code == 201
    assert called['label'] == 'Supplier'
    assert called['properties']['id_proveedor'] == 555
