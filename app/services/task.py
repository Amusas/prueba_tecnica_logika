from sqlalchemy.orm import Session
from app.models.task import Task
from app.exceptions.task import TaskNotFoundException, TaskCreationException, NotTaskOwnerException
from app.mappers.task import TaskMapper
from app.schemas.task import TaskCreateDTO, TaskResponseDTO
from app.core.logging import logger
from datetime import datetime
from app.core.utils import sanitize_pagination
from app.schemas.pagination import PaginatedResponse
from app.core.enums import TaskStatus

class TaskService:
    """
    Capa de servicio para la gestión de tareas.
    Contiene la lógica de negocio y validaciones de propiedad (ownership).
    """

    @staticmethod
    def list_tasks(db: Session, page: int, page_size: int, user_id: int) -> PaginatedResponse[TaskResponseDTO]:
        """
        Obtiene una lista paginada de tareas que pertenecen específicamente al usuario autenticado.
        """
        page, page_size = sanitize_pagination(page, page_size)
        
        # Filtro por estado no eliminado y pertenencia al usuario
        query = db.query(Task).filter(
            Task.status != TaskStatus.DELETED,
            Task.user_id == user_id
        )
        
        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Task.created_at.desc()).offset(offset).limit(page_size).all()
        
        logger.info("Tareas listadas desde el servicio", user_id=user_id, count=len(items), total=total)
        # Importación local para evitar dependencia circular
        from app.mappers.task import TaskMapper
        return TaskMapper.to_paginated_dto(items, total, page, page_size)

    @staticmethod
    def create_task(db: Session, task_dto: TaskCreateDTO, user_id: int) -> Task:
        """
        Crea una nueva tarea vinculándola al usuario proporcionado.
        """
        try:
            task = TaskMapper.to_entity(task_dto, user_id)
            db.add(task)
            db.commit()
            db.refresh(task)
            logger.info("Tarea creada exitosamente en el servicio", user_id=user_id, task_id=task.id)
            return task
        except Exception as e:
            logger.error(f"Error al crear la tarea: {e}", user_id=user_id)
            raise TaskCreationException()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
        """
        Busca una tarea por su ID y verifica que pertenezca al usuario solicitante.
        Lanza excepciones si la tarea no existe o no hay permisos.
        """
        # Se filtran las tareas marcadas como eliminadas
        task = db.query(Task).filter(Task.id == task_id, Task.status != TaskStatus.DELETED).first()
        if not task:
            logger.warning("Tarea no encontrada en el servicio", task_id=task_id, user_id=user_id)
            raise TaskNotFoundException(detail=f"Tarea con id {task_id} no encontrada")
        
        # Validación de propiedad
        if task.user_id != user_id:
            logger.warning("Intento de acceso no autorizado a tarea", task_id=task_id, user_id=user_id, owner_id=task.user_id)
            raise NotTaskOwnerException("No tienes permiso para acceder a este recurso")
            
        logger.info("Tarea obtenida exitosamente en el servicio", task_id=task_id, user_id=user_id)
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, update_dto, user_id: int) -> Task:
        """
        Actualiza una tarea existente previa validación de propiedad.
        """
        task = TaskService.get_task_by_id(db, task_id, user_id)
        
        from app.mappers.task import TaskMapper
        task = TaskMapper.update_entity(task, update_dto)
        task.updated_at = datetime.now()
        db.commit()
        db.refresh(task)
        logger.info("Tarea actualizada exitosamente en el servicio", task_id=task_id, user_id=user_id)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> None:
        """
        Realiza un borrado lógico (soft delete) de una tarea.
        """
        task = TaskService.get_task_by_id(db, task_id, user_id)
        
        task.status = TaskStatus.DELETED
        task.updated_at = datetime.now()
        db.commit()
        logger.info("Tarea eliminada (soft delete) en el servicio", task_id=task_id, user_id=user_id)
