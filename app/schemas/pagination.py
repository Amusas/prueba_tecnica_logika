from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Estructura genérica para respuestas que incluyen paginación.
    
    Attributes:
        items: Lista de elementos de tipo T.
        total: Cantidad total de registros en la base de datos.
        page: Página actual consultada.
        page_size: Cantidad de registros por página.
        total_pages: Cálculo total de páginas disponibles.
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
