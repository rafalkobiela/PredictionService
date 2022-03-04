def test_alive(test_client):
    test_client.get("/alive").raise_for_status()
