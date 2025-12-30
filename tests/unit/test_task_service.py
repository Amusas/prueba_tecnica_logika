import pytest
from unittest.mock import MagicMock
from app.services.task import TaskService
from app.models.task import Task
from app.schemas.task import TaskCreateDTO
from app.exceptions.task import TaskNotFoundException, NotTaskOwnerException
from app.core.enums import TaskStatus

def test_create_task_success():
    """Prueba la creación exitosa de una tarea en el servicio."""
    db = MagicMock()
    task_dto = TaskCreateDTO(title="Test Task", description="Desc")
    user_id = 1
    
    task = TaskService.create_task(db, task_dto, user_id)
    
    assert task.title == "Test Task"
    assert task.user_id == user_id
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_get_task_by_id_success():
    """Prueba la obtención exitosa de una tarea propia."""
    db = MagicMock()
    mock_task = Task(id=1, title="My Task", user_id=1, status=TaskStatus.PENDING)
    db.query().filter().first.return_value = mock_task
    
    task = TaskService.get_task_by_id(db, 1, 1)
    
    assert task.id == 1
    assert task.title == "My Task"

def test_get_task_not_found():
    """Prueba que el servicio lance una excepción si la tarea no existe."""
    db = MagicMock()
    db.query().filter().first.return_value = None
    
    with pytest.raises(TaskNotFoundException):
        TaskService.get_task_by_id(db, 999, 1)

def test_get_task_not_owner():
    """Prueba que el servicio deniegue el acceso a tareas ajenas."""
    db = MagicMock()
    mock_task = Task(id=1, title="Other's Task", user_id=2, status=TaskStatus.PENDING)
    db.query().filter().first.return_value = mock_task
    
    with pytest.raises(NotTaskOwnerException):
        TaskService.get_task_by_id(db, 1, 1)

def test_delete_task_soft_delete():
    """Prueba que la eliminación sea un borrado lógico (soft delete)."""
    db = MagicMock()
    mock_task = Task(id=1, title="To Delete", user_id=1, status=TaskStatus.PENDING)
    # Mocking get_task_by_id internally by making the query return current task
    db.query().filter().first.return_value = mock_task
    
    TaskService.delete_task(db, 1, 1)
    
    assert mock_task.status == TaskStatus.DELETED
    db.commit.assert_called()
