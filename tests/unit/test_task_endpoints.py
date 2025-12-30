import pytest
from fastapi.testclient import TestClient
from main import app
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.core.enums import TaskStatus
from unittest.mock import MagicMock, patch
from datetime import datetime

# Mock de usuario
MOCK_USER = User(id=1, email="test@example.com", full_name="Test User")

# Override de dependencias
def override_get_db():
    return MagicMock()

def override_get_current_user():
    return MOCK_USER

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@patch("app.services.task.TaskService.create_task")
def test_create_task_endpoint(mock_create):
    """Prueba el endpoint de creación de tareas."""
    from app.models.task import Task
    mock_task = Task(
        id=1, 
        title="API Task", 
        description="Desc", 
        status=TaskStatus.PENDING, 
        user_id=1,
        created_at=datetime.now() # Agregado para validatión Pydantic
    )
    mock_create.return_value = mock_task
    
    response = client.post("/api/tasks/", json={"title": "API Task", "description": "Desc"})
    
    assert response.status_code == 201
    assert response.json()["data"]["title"] == "API Task"
    assert response.json()["success"] is True

@patch("app.services.task.TaskService.list_tasks")
def test_list_tasks_endpoint(mock_list):
    """Prueba el endpoint de listado de tareas."""
    from app.schemas.pagination import PaginatedResponse
    from app.schemas.task import TaskResponseDTO
    
    mock_dto = TaskResponseDTO(
        id=1, title="Task 1", description="D", status=TaskStatus.PENDING, 
        user_id=1, created_at=datetime.now(), updated_at=None
    )
    mock_list.return_value = PaginatedResponse(
        items=[mock_dto], total=1, page=1, page_size=10, total_pages=1
    )
    
    response = client.get("/api/tasks/")
    
    assert response.status_code == 200
    assert len(response.json()["data"]["items"]) == 1
    assert response.json()["message"] == "Tareas listadas exitosamente"

@patch("app.services.task.TaskService.get_task_by_id")
def test_get_task_not_found_endpoint(mock_get):
    """Prueba el manejo de errores (404) en el endpoint."""
    from app.exceptions.task import TaskNotFoundException
    mock_get.side_effect = TaskNotFoundException(detail="No encontrada")
    
    response = client.get("/api/tasks/999")
    
    assert response.status_code == 404
    assert response.json()["success"] is False
    assert "No encontrada" in response.json()["message"]
