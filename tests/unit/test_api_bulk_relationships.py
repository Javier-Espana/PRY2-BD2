from types import SimpleNamespace

import src.api as api


def _client(monkeypatch, crud):
    monkeypatch.setattr(api, "sc_app", SimpleNamespace(crud=crud))
    return api.app.test_client()


def test_bulk_update_relationships_missing_properties_returns_400(monkeypatch):
    client = _client(monkeypatch, SimpleNamespace(add_properties_to_multiple_relationships=lambda *args, **kwargs: 1))

    resp = client.post('/api/relationships/bulk/update', json={
        'rel_type': 'SUMINISTRA',
        'filter_label': 'Supplier',
        'filter_prop': 'id_proveedor',
        'filter_values': [1],
    })

    assert resp.status_code == 400


def test_bulk_remove_relationship_props_missing_property_names_returns_400(monkeypatch):
    client = _client(monkeypatch, SimpleNamespace(remove_properties_from_multiple_relationships=lambda *args, **kwargs: 1))

    resp = client.post('/api/relationships/bulk/remove-properties', json={
        'rel_type': 'SUMINISTRA',
        'filter_label': 'Supplier',
        'filter_prop': 'id_proveedor',
        'filter_values': [1],
    })

    assert resp.status_code == 400


def test_bulk_delete_relationships_success_calls_crud(monkeypatch):
    calls = {}

    def fake_delete(rel_type, filter_label, filter_prop, filter_values):
        calls['rel_type'] = rel_type
        calls['filter_label'] = filter_label
        calls['filter_prop'] = filter_prop
        calls['filter_values'] = filter_values
        return 3

    client = _client(monkeypatch, SimpleNamespace(delete_multiple_relationships=fake_delete))

    resp = client.post('/api/relationships/bulk/delete', json={
        'rel_type': 'SUMINISTRA',
        'filter_label': 'Supplier',
        'filter_prop': 'id_proveedor',
        'filter_values': [1, 2],
    })

    assert resp.status_code == 200
    assert resp.json['deleted'] == 3
    assert calls == {
        'rel_type': 'SUMINISTRA',
        'filter_label': 'Supplier',
        'filter_prop': 'id_proveedor',
        'filter_values': [1, 2],
    }
