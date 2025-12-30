import sys
from unittest.mock import MagicMock

# Evitar que app.db.session intente conectar a la base de datos real al importarse
# Esto debe hacerse ANTES de que cualquier módulo de la app sea importado
mock_engine = MagicMock()
mock_session_local = MagicMock()

# Mockear sqlalchemy ANTES de cargar los servicios/controladores
import sqlalchemy
sqlalchemy.create_engine = MagicMock(return_value=mock_engine)

# También mockeamos app.db.session de forma preventiva si ya se intentó cargar
if 'app.db.session' in sys.modules:
    sys.modules['app.db.session'].engine = mock_engine
    sys.modules['app.db.session'].SessionLocal = mock_session_local
