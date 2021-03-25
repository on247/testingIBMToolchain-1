import json


def test_index(app, client):
    del app
    res = client.get('/')
    assert res.status_code == 200
    expected = {'hello': 'world'}
    assert expected == json.loads(res.get_data(as_text=True))

def test_home(app, client):
    del app
    res = client.get('/home')
    assert res.status_code == 200
    expected = "<h1 style='color:red'>This is home!</h1>"
    assert expected == res.get_data(as_text=True)

def test_qrst_bad(app, client):
    del app
    res = client.get('/qstr')
    assert res.status_code == 404
    expected = {"error": "No Query String"}
    assert expected == json.loads(res.get_data(as_text=True))

def test_qrst_good(app, client):
    del app
    res = client.get('/qstr?test=test')
    assert res.status_code == 200
    expected = {"test": "test"}
    assert expected == json.loads(res.get_data(as_text=True))

def test_json(app, client):
    del app
    res = client.get('/json')
    assert res.status_code == 200
    expected = {
        "clouds": {
            "AMAZON": "AWS",
            "IBM": "IBM CLOUD",
            "MICROSOFT": "AZURE"
        },
        "colors": {
            "b": "blue",
            "g": "green",
            "r": "red"
        },
        "languages": {
            "en": "English",
            "es": "Spanish",
            "fr": "French"
        }
    }
    assert expected == json.loads(res.get_data(as_text=True))

def test_json_colors(app, client):
    del app
    res = client.get('/json/colors/r')
    assert res.status_code == 203
    expected = {"res":"red"}
    assert expected == json.loads(res.get_data(as_text=True))
    res = client.get('/json/colors/f')
    assert res.status_code == 404
    expected = {"error":"Not found"}
    assert expected == json.loads(res.get_data(as_text=True))

def test_json_post_collection_bad(app, client):
    del app
    res = client.post('/json/colors')
    assert res.status_code == 400
    expected = {"error": "Collection already exists"}
    assert expected == json.loads(res.get_data(as_text=True))

def test_json_post_collection_good(app, client):
    del app
    res = client.post('/json/cars', json={
            "f":"Ferrari",
            "b":"BMW",
            "d":"dodge"
    })
    assert res.status_code == 201
    expected = {"message": "Collection created"}
    assert expected == json.loads(res.get_data(as_text=True))

def test_json_put_collection_good(app, client):
    del app
    res = client.put('/json/cars/f', json={
            "new":"Ford"
    })
    assert res.status_code == 200
    expected = {'res': {'b': 'BMW', 'd': 'dodge', 'f': 'Ford'}}
    assert expected == json.loads(res.get_data(as_text=True))

def test_json_delete_collection_good(app, client):
    del app
    res = client.delete('/json/cars')
    assert res.status_code == 200
    expected = {
                'clouds': {
                    'AMAZON': 'AWS',
                    'IBM': 'IBM CLOUD',
                    'MICROSOFT': 'AZURE'
                },
                'colors': {
                    'b': 'blue', 
                    'g': 'green', 
                    'r': 'red'
                },
                'languages': {
                    'en': 'English', 
                    'es': 'Spanish', 
                    'fr': 'French'
                }
            }
    assert expected == json.loads(res.get_data(as_text=True))
