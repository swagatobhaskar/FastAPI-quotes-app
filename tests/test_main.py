
# pass the client fixture from confTest.py

def test_root(client):
    response = client.get("/root")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_home_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_all_quotes_route(client):
    response = client.get("/api/all-quotes")
    assert response.status_code == 200

# pass the client fixture as an argument
def test_new_quote(client):
    response = client.post(
        "/api/new-quote",
        json={"author": "bob", "text": "bob's test quote."}
        )
    data = response.json()
    assert response.status_code == 200
    assert data['author'] == 'bob'
    assert data["text"] == "bob's test quote."
    assert "id" in data
    assert isinstance(data["id"], int)
