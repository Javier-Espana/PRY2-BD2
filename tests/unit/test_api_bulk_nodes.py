from types import SimpleNamespace

import src.api as api


def _client(monkeypatch, crud):
    monkeypatch.setattr(api, "sc_app", SimpleNamespace(crud=crud))
    return api.app.test_client()


def test_bulk_update_nodes_missing_filter_prop_returns_400(monkeypatch):
    client = _client(monkeypatch, SimpleNamespace(add_properties_to_multiple_nodes=lambda *args, **kwargs: 1))

    resp = client.post('/api/nodes/Supplier/bulk/update', json={
        'filter_values': ['GT'],
        'properties': {'activo': True},
    })

    assert resp.status_code == 400


def test_bulk_delete_nodes_missing_filter_values_returns_400(monkeypatch):
    client = _client(monkeypatch, SimpleNamespace(delete_multiple_nodes=lambda *args, **kwargs: 1))

    resp = client.post('/api/nodes/Supplier/bulk/delete', json={
        'filter_prop': 'pais',
    })

    assert resp.status_code == 400


def test_bulk_remove_node_props_missing_property_names_returns_400(monkeypatch):
    client = _client(monkeypatch, SimpleNamespace(remove_properties_from_multiple_nodes=lambda *args, **kwargs: 1))

    resp = client.post('/api/nodes/Supplier/bulk/remove-properties', json={
        'filter_prop': 'pais',
        'filter_values': ['GT'],
    })

    assert resp.status_code == 400


def test_bulk_update_nodes_success_calls_crud(monkeypatch):
    calls = {}

    def fake_add(label, filter_prop, filter_values, properties):
        calls['label'] = label
        calls['filter_prop'] = filter_prop
        calls['filter_values'] = filter_values
        calls['properties'] = properties
        return 2

    client = _client(monkeypatch, SimpleNamespace(add_properties_to_multiple_nodes=fake_add))

    resp = client.post('/api/nodes/Supplier/bulk/update', json={
        'filter_prop': 'pais',
        'filter_values': ['GT'],
        'properties': {'activo': True},
    })

    assert resp.status_code == 200
    assert resp.json['updated'] == 2
    assert calls == {
        'label': 'Supplier',
        'filter_prop': 'pais',
        'filter_values': ['GT'],
        'properties': {'activo': True},
    }
