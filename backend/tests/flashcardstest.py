import pytest
from app import create_app, db
from app.flashcards.models import User

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('app.config.TestingConfig')
    with app.app_context():
        yield app   

@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def test_login(test_app, test_database):
    client = test_app.test_client()
    user = add_user('testuser', 'test@test.com', 'testpassword')

    response = client.post('/api/flashcards/login',
                           json={'username': 'testuser', 'password': 'testpassword'},
                           content_type='application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data

    # Testing for invalid password
    response = client.post('/api/flashcards/login',
                           json={'username': 'testuser', 'password': 'wrongpassword'},
                           content_type='application/json')
    data = response.get_json()
    assert response.status_code == 401
    assert 'msg' in data

def test_registration(test_app, test_database):
    client = test_app.test_client()

    # Testing successful registration
    response = client.post('/api/flashcards/register',
                           json={'username': 'newuser', 'email': 'new@test.com', 'password': 'newpassword'},
                           content_type='application/json')
    data = response.get_json()
    assert response.status_code == 201
    assert 'username' in data
    assert 'email' in data

    # Testing registration with already registered username
    response = client.post('/api/flashcards/register',
                           json={'username': 'newuser', 'email': 'different@test.com', 'password': 'newpassword'},
                           content_type='application/json')
    data = response.get_json()
    assert response.status_code == 400
    assert 'message' in data
    assert data['message'] == 'User with this username already exists.'

    # Testing registration with already registered email
    response = client.post('/api/flashcards/register',
                           json={'username': 'differentuser', 'email': 'new@test.com', 'password': 'newpassword'},
                           content_type='application/json')
    data = response.get_json()
    assert response.status_code == 400
    assert 'message' in data
    assert data['message'] == 'User with this email already exists.'

def test_flashcard_creation(test_app, test_database):
    client = test_app.test_client()
    user = add_user('flashcarduser', 'flashcard@test.com', 'testpassword')

    response = client.post('/api/flashcards/login',
                           json={'username': 'flashcarduser', 'password': 'testpassword'},
                           content_type='application/json')
    data = response.get_json()
    token = data['access_token']

    # Testing successful flashcard creation
    response = client.post('/api/flashcards/',
                           json={'word': 'testword', 'definition': 'testdefinition'},
                           headers={'Authorization': f'Bearer {token}'},
                           content_type='application/json')
    data = response.get_json()
    assert response.status_code == 201
    assert 'word' in data
    assert 'definition' in data

def test_flashcard_update(test_app, test_database):
    client = test_app.test_client()
    user = add_user('testuser', 'test@test.com', 'testpassword')
    flashcard = add_flashcard(user.id, 'testword', 'testdefinition')

    response = client.post('/api/flashcards/login',
                           json={'username': 'testuser', 'password': 'testpassword'},
                           content_type='application/json')
    data = response.get_json()
    token = data['access_token']

    # Testing successful flashcard update
    response = client.put(f'/api/flashcards/{flashcard.id}',
                          json={'word': 'updatedword', 'definition': 'updateddefinition'},
                          headers={'Authorization': f'Bearer {token}'},
                          content_type='application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert 'word' in data
    assert 'definition' in data
    assert data['word'] == 'updatedword'
    assert data['definition'] == 'updateddefinition'

def test_flashcard_delete(test_app, test_database):
    client = test_app.test_client()
    user = add_user('testuser', 'test@test.com', 'testpassword')
    flashcard = add_flashcard(user.id, 'testword', 'testdefinition')

    response = client.post('/api/flashcards/login',
                           json={'username': 'testuser', 'password': 'testpassword'},
                           content_type='application/json')
    data = response.get_json()
    token = data['access_token']

    # Testing successful flashcard deletion
    response = client.delete(f'/api/flashcards/{flashcard.id}',
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 204

    # Testing deletion of already deleted flashcard
    response = client.delete(f'/api/flashcards/{flashcard.id}',
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
