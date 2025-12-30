from enum import Enum

class TaskStatus(str, Enum):
    """
    Representa los posibles estados de una tarea en el sistema.
    Hereda de str para facilitar la serialización JSON.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    DELETED = "deleted"
