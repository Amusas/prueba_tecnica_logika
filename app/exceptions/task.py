class TaskException(Exception):
    """Clase base para todas las excepciones relacionadas con la gestión de tareas."""
    pass

class TaskNotFoundException(TaskException):
    """Lanzada cuando se intenta acceder a una tarea que no existe o fue eliminada por soft-delete."""
    def __init__(self, detail: str = "Tarea no encontrada"):
        self.detail = detail

class TaskCreationException(TaskException):
    """Lanzada cuando ocurre un error inesperado durante la persistencia de una nueva tarea."""
    def __init__(self, detail: str = "No se pudo crear la tarea"):
        self.detail = detail

class NotTaskOwnerException(TaskException):
    """Lanzada cuando un usuario intenta acceder o modificar una tarea que pertenece a otro usuario."""
    def __init__(self, detail: str = "No tienes permisos para modificar este recurso"):
        self.detail = detail
