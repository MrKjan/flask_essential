from urlshort import create_app

def test_has_header(client):
    response = client.get('/')
    assert b'Shorten' in response.data
