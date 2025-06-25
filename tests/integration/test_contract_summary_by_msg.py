def test_export_contract_route_exists(client):
    response = client.post("/export-contract", json={"message": "cc"})
    assert response.status_code == 200
    
