from app.app import app

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"ROLL NO" in response.data
    assert b"AYUSH MORE" in response.data

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "broken"
    assert payload["service"] == "nexus-devops-dashboard"
    assert payload["uptime_seconds"] >= 0

def test_pipeline_source_endpoint():
    client = app.test_client()
    response = client.get("/api/pipeline-source")
    assert response.status_code == 200
    source = response.get_json()["source"]
    assert "stage('Test')" in source
    assert "docker build" in source
