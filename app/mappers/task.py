from app.models.task import Task
from app.schemas.task import TaskCreateDTO, TaskResponseDTO
from app.schemas.pagination import PaginatedResponse
import math

class TaskMapper:
    """
    Transformador de datos entre entidades del dominio (ORM) y DTOs de la API.
    Aísla la lógica de conversión para mantener los servicios limpios.
    """

    @staticmethod
    def to_paginated_dto(items: list[Task], total: int, page: int, page_size: int) -> PaginatedResponse[TaskResponseDTO]:
        """Convierte una lista de entidades en una respuesta paginada estructurada."""
        dtos = [TaskResponseDTO.model_validate(item) for item in items]
        total_pages = math.ceil(total / page_size) if page_size > 0 else 0
        
        return PaginatedResponse[TaskResponseDTO](
            items=dtos,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def to_entity(create_dto: TaskCreateDTO, user_id: int) -> Task:
        """Crea una instancia de la entidad Task a partir de un DTO de creación."""
        return Task(
            title=create_dto.title,
            description=create_dto.description,
            status=create_dto.status,
            user_id=user_id
        )

    @staticmethod
    def to_dto(entity: Task) -> TaskResponseDTO:
        """Convierte una entidad individual en un DTO de respuesta."""
        return TaskResponseDTO.model_validate(entity)

    @staticmethod
    def update_entity(entity: Task, update_dto) -> Task:
        """
        Aplica los cambios de un DTO de actualización sobre una entidad existente.
        Solo actualiza los campos que no son None en el DTO.
        """
        if update_dto.title is not None:
            entity.title = update_dto.title
        if update_dto.description is not None:
            entity.description = update_dto.description
        if update_dto.status is not None:
            entity.status = update_dto.status
        return entity
