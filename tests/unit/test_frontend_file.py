import os


def test_frontend_file_exists_and_has_key_ids():
    base = os.path.dirname(os.path.dirname(__file__))
    # repo structure: tests/unit -> go up two levels to project root
    project_root = os.path.abspath(os.path.join(base, '..'))
    frontend_path = os.path.join(project_root, 'app', 'code.html')
    assert os.path.exists(frontend_path), f"Frontend file not found: {frontend_path}"

    content = open(frontend_path, 'r', encoding='utf-8').read()
    # check for several important IDs/elements used by the JS
    assert 'id="section-dashboard"' in content
    assert 'id="toast"' in content
    assert 'id="graph-container"' in content
    assert 'id="csv-file"' in content
