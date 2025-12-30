from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.task import TaskCreateDTO, TaskResponseDTO, TaskUpdateDTO
from app.schemas.pagination import PaginatedResponse
from app.schemas.auth import CustomResponse, ErrorResponse
from app.services.task import TaskService
from app.mappers.task import TaskMapper
from app.core.logging import logger

router = APIRouter()

# Respuestas comunes para endpoints protegidos
AUTH_RESPONSES = {
    401: {"model": ErrorResponse, "description": "No autorizado - Token inválido o expirado"},
}

OWNERSHIP_RESPONSES = {
    **AUTH_RESPONSES,
    403: {"model": ErrorResponse, "description": "Acceso denegado - El usuario no es el propietario de la tarea"},
    404: {"model": ErrorResponse, "description": "Tarea no encontrada"},
}

@router.post(
    "/", 
    response_model=CustomResponse[TaskResponseDTO], 
    status_code=status.HTTP_201_CREATED,
    responses={
        **AUTH_RESPONSES,
        400: {"model": ErrorResponse, "description": "Error al crear la tarea"},
    },
    summary="Crear una nueva tarea",
    description="Crea una tarea asociada al usuario autenticado. Devuelve la tarea creada y establece la cabecera 'Location'."
)
def create_task(
    task_dto: TaskCreateDTO,
    request: Request,
    response: Response,
    db: Session = Depends(deps.get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    logger.info("Petición para crear tarea", user_id=current_user.id, title=task_dto.title)
    new_task_entity = TaskService.create_task(db, task_dto, current_user.id)
    response_dto = TaskMapper.to_dto(new_task_entity)

    response.headers["Location"] = str(
        request.url_for("get_task_by_id", task_id=response_dto.id)
    )

    return CustomResponse(
        success=True,
        code=201,
        message="Tarea creada exitosamente",
        data=response_dto
    )

@router.get(
    "/{task_id}", 
    response_model=CustomResponse[TaskResponseDTO], 
    name="get_task_by_id",
    responses=OWNERSHIP_RESPONSES,
    summary="Obtener una tarea",
    description="Recupera los detalles de una tarea específica si el usuario autenticado es su propietario."
)
def get_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    logger.info("Petición para obtener tarea", user_id=current_user.id, task_id=task_id)
    task_entity = TaskService.get_task_by_id(db, task_id, current_user.id)
    response_dto = TaskMapper.to_dto(task_entity)
    
    return CustomResponse(
        success=True,
        code=200,
        message="Tarea obtenida exitosamente",
        data=response_dto
    )

@router.get(
    "/", 
    response_model=CustomResponse[PaginatedResponse[TaskResponseDTO]],
    responses=AUTH_RESPONSES,
    summary="Listar tareas",
    description="Lista las tareas del usuario autenticado de forma paginada. No incluye tareas eliminadas suavemente (soft-delete)."
)
def list_tasks(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    logger.info("Petición para listar tareas", user_id=current_user.id, page=page, page_size=page_size)
    paginated_response = TaskService.list_tasks(db, page, page_size, current_user.id)
    
    return CustomResponse(
        success=True,
        code=200,
        message="Tareas listadas exitosamente",
        data=paginated_response
    )

@router.put(
    "/{task_id}", 
    response_model=CustomResponse[TaskResponseDTO],
    responses=OWNERSHIP_RESPONSES,
    summary="Actualizar una tarea",
    description="Modifica una tarea existente. Solo el propietario puede realizar esta acción."
)
def update_task(
    task_id: int,
    update_dto: TaskUpdateDTO, 
    request: Request,
    response: Response,
    db: Session = Depends(deps.get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    logger.info("Petición para actualizar tarea", user_id=current_user.id, task_id=task_id)
    updated_task = TaskService.update_task(db, task_id, update_dto, current_user.id)
    response_dto = TaskMapper.to_dto(updated_task)

    response.headers["Location"] = str(
        request.url_for("get_task_by_id", task_id=response_dto.id)
    )
    
    return CustomResponse(
        success=True,
        code=200,
        message="Tarea actualizada exitosamente",
        data=response_dto
    )

@router.delete(
    "/{task_id}", 
    response_model=CustomResponse[None],
    responses=OWNERSHIP_RESPONSES,
    summary="Eliminar una tarea",
    description="Realiza un borrado lógico (soft-delete) de una tarea. Solo el propietario puede eliminarla."
)
def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    logger.info("Petición para eliminar tarea", user_id=current_user.id, task_id=task_id)
    TaskService.delete_task(db, task_id, current_user.id)

    return CustomResponse(
        success=True,
        code=200,
        message="Tarea eliminada exitosamente",
        data=None
    )
