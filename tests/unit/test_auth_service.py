import pytest
from unittest.mock import MagicMock, patch
from app.services.auth import authenticate_user
from app.exceptions.auth import InvalidCredentialsException, UserNotFoundException
from app.models.user import User

@patch("app.services.auth.verify_password")
@patch("app.services.auth.create_access_token")
def test_authenticate_user_success(mock_create_token, mock_verify):
    """Prueba la autenticación exitosa de un usuario."""
    db = MagicMock()
    mock_user = User(id=1, email="admin@logika.com", hashed_password="hashed")
    db.query().filter().first.return_value = mock_user
    mock_verify.return_value = True
    mock_create_token.return_value = "fake-jwt-token"
    
    token = authenticate_user(db, "admin@logika.com", "password")
    
    assert token == "fake-jwt-token"
    mock_verify.assert_called_once()
    mock_create_token.assert_called_once()

def test_authenticate_user_not_found():
    """Prueba el fallo cuando el usuario no existe."""
    db = MagicMock()
    db.query().filter().first.return_value = None
    
    with pytest.raises(UserNotFoundException):
        authenticate_user(db, "no@existe.com", "password")

@patch("app.services.auth.verify_password")
def test_authenticate_user_wrong_password(mock_verify):
    """Prueba el fallo cuando la contraseña es incorrecta."""
    db = MagicMock()
    mock_user = User(id=1, email="admin@logika.com", hashed_password="hashed")
    db.query().filter().first.return_value = mock_user
    mock_verify.return_value = False
    
    with pytest.raises(InvalidCredentialsException):
        authenticate_user(db, "admin@logika.com", "wrong")
