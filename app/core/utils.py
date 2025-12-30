def sanitize_pagination(page: int, page_size: int) -> tuple[int, int]:
    """
    Sanitiza y valida los parámetros de paginación.
    
    Asegura que el número de página sea al menos 1 y que el tamaño de página
    esté dentro de un rango razonable (1-100) para evitar sobrecarga.
    
    Args:
        page: Número de página solicitado.
        page_size: Cantidad de elementos por página.
        
    Returns:
        Tupla con (página, tamaño_página) ya validados.
    """
    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 10
    elif page_size > 100:
        page_size = 100
        
    return page, page_size
