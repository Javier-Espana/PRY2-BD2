from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_FILE = PROJECT_ROOT / 'app' / 'code.html'


def test_frontend_exposes_bulk_controls_and_views():
    html = FRONTEND_FILE.read_text(encoding='utf-8')

    expected_controls = [
        'id="section-dashboard"',
        'id="section-entities"',
        'id="section-relationships"',
        'id="section-analytics"',
        'onclick="bulkUpdate()"',
        'onclick="bulkRemoveProps()"',
        'onclick="bulkDelete()"',
        'onclick="bulkRelUpdate()"',
        'onclick="bulkRelRemoveProps()"',
        'onclick="bulkRelDelete()"',
        'id="csv-file"',
        'id="graph-container"',
    ]

    for token in expected_controls:
        assert token in html


def test_frontend_calls_backend_bulk_and_core_endpoints():
    html = FRONTEND_FILE.read_text(encoding='utf-8')

    expected_endpoints = [
        '/api/health',
        '/api/init',
        '/api/stats',
        '/api/suppliers',
        '/api/products',
        '/api/orders',
        '/api/inventories',
        '/api/centers',
        '/api/transports',
        '/api/relationship-types',
        '/api/nodes/',
        '/api/nodes/${curLabel}/bulk/update',
        '/api/nodes/${curLabel}/bulk/remove-properties',
        '/api/nodes/${curLabel}/bulk/delete',
        '/api/relationships/bulk/update',
        '/api/relationships/bulk/remove-properties',
        '/api/relationships/bulk/delete',
        '/api/import/csv',
        '/api/queries/products-by-category/',
        '/api/queries/top-suppliers',
        '/api/queries/pending-orders',
        '/api/queries/transport-status',
        '/api/queries/inventory-for-product/',
        '/api/analytics/stockouts',
        '/api/analytics/reorder',
        '/api/analytics/top-suppliers',
        '/api/analytics/transport-overview',
        '/api/graph-sample',
    ]

    for endpoint in expected_endpoints:
        assert endpoint in html


def test_frontend_bulk_relationship_buttons_map_to_relationship_endpoints():
    html = FRONTEND_FILE.read_text(encoding='utf-8')

    patterns = [
        r'function\s+bulkRelUpdate\(\)\s*\{.*?/api/relationships/bulk/update',
        r'function\s+bulkRelRemoveProps\(\)\s*\{.*?/api/relationships/bulk/remove-properties',
        r'function\s+bulkRelDelete\(\)\s*\{.*?/api/relationships/bulk/delete',
    ]

    for pattern in patterns:
        assert re.search(pattern, html, re.S)
