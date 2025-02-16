# test_main_page.py
def test_main_page(client):  # `client` is passed as an argument
    response = client.get('/')  # Simulates GET request to /
    assert response.status_code == 200  # Check if status code is 200
    assert response.json == {'message': 'Flask run'}  # Check if response is correct

    # check for false positive case
    response = client.post('/') # Simulates POST request to / 
    assert response.status_code == 405 # Check if status code is 405