# 📋 Prueba Técnica Logika - API de Gestión de Tareas

Esta es una solución robusta y profesional desarrollada para la prueba técnica de **Logika**. El sistema implementa una API REST completa para la gestión de tareas, con un fuerte enfoque en seguridad, arquitectura modular y trazabilidad profesional.

**Autor:** Andres Felipe Rendon Nieto

---

## 🚀 Cumplimiento de Requerimientos

Este proyecto ha sido diseñado para cumplir con los estándares más altos de calidad solicitados:

*   **Stack**: Python 3.11.8, FastAPI, SQLAlchemy, PostgreSQL.
*   **Autenticación**: JWT (JSON Web Tokens) con hash de contraseñas mediante **Bcrypt**.
*   **Entidad Task**: ID, título, descripción, estado (Enum), creado en, actualizado en y **propietario (user_id)**.
*   **Funcionalidades**: CRUD completo, paginación real, manejo de errores estandarizado (400, 401, 403, 404, 422).
*   **Persistencia**: Gestión de migraciones con **Alembic**.
*   **Despliegue**: Dockerización completa (App + DB) con orquestación mediante **Docker Compose**.

---

## 🌟 Características Adicionales (Plus)

1.  **Seguridad de Propiedad (Ownership)**: Se implementó un aislamiento estricto. Un usuario autenticado **solo puede ver, editar o eliminar sus propias tareas**.
2.  **Arquitectura Modular**: Separación clara en capas: Routers (API), Servicios (Lógica), Modelos (ORM), Schemas (Pydantic), y Mappers (Conversión de datos).
3.  **Logs Estructurados**: Implementación de `structlog` para logs en formato JSON, ideales para monitoreo y auditoría.
4.  **Inicialización Automática (Seeders)**: El sistema inyecta automáticamente 3 usuarios y 22 tareas de ejemplo al iniciar, permitiendo pruebas inmediatas.
5.  **Pruebas Unitarias e Integración**: Suite de pruebas con `pytest` y scripts de verificación end-to-end.
6.  **Dockerfile Profesional**: Uso de *multi-stage builds*, usuario no-root y `entrypoint.sh` con espera activa de base de datos.
7.  **Swagger con JWT**: Configuración de `HTTPBearer` en Swagger para facilitar la introducción del token JWT directamente.

---

## 📂 Estructura del Código

```text
.
├── alembic/                # Historial de migraciones de DB
├── app/
│   ├── api/                # Enrutadores y dependencias de seguridad
│   ├── core/               # Configuración, seguridad JWT y logging
│   ├── db/                 # Conexión, sesión y semillas (Seeder)
│   ├── exceptions/         # Excepciones personalizadas y handlers
│   ├── mappers/            # Capa de transformación (ORM <-> DTO)
│   ├── models/             # Modelos de SQLAlchemy (Entidades)
│   └── schemas/            # Esquemas de Pydantic (Validación)
├── tests/                  # Pruebas unitarias de servicios y endpoints
├── Dockerfile              # Imagen optimizada y segura
├── docker-compose.yml      # Orquestación de servicios (API + PostgreSQL)
├── entrypoint.sh           # Script de arranque (espera DB + migraciones)
├── main.py                 # Punto de entrada FastAPI
└── .env                    # Variables de entorno (Debe crearse manualmente)
```

---

## 🛠️ Instrucciones de Ejecución

### Opción A: Ejecución con Docker (Recomendada)
Esta es la forma más rápida y segura de ejecutar el proyecto, ya que Docker se encarga de configurar la base de datos y todas las dependencias.

1.  **Clonar el repositorio** e ingresar a la carpeta del proyecto.
2.  **Preparar el entorno**: Crea un archivo llamado `.env` en la raíz del proyecto. Puedes usar el siguiente bloque como plantilla:
    ```env
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=logika_db
    DB_USER=postgres
    DB_PASSWORD=postgres
    SECRET_KEY=supersecretkey
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```
3.  **Construir y levantar**: Ejecuta el siguiente comando en tu terminal:
    ```bash
    docker compose up --build
    ```
    *   *Nota*: El script `entrypoint.sh` esperará a que PostgreSQL esté listo, ejecutará automáticamente las migraciones de Alembic e iniciará el servidor Uvicorn.
4.  **Acceder a la API**:
    *   API Base: `http://localhost:8000`
    *   Documentación Swagger: `http://localhost:8000/docs`

---

### Opción B: Ejecución Local (Desarrollo)
Si prefieres no usar Docker para la aplicación, sigue estos pasos:

1.  **Base de Datos**: Asegúrate de tener una instancia de PostgreSQL corriendo (puedes usar Docker solo para la DB: `docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres`).
2.  **Crear archivo .env**: Ajusta los valores de conexión (ej. `DB_HOST=localhost`).
3.  **Entorno Virtual**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Linux/Mac
    # .venv\Scripts\activate   # En Windows
    ```
4.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Ejecutar Migraciones**: Esto creará las tablas y el usuario inicial.
    ```bash
    alembic upgrade head
    ```
6.  **Iniciar la Aplicación**:
    ```bash
    uvicorn main:app --reload
    ```

---

## 👤 Usuarios Iniciales (Credenciales)

Al ejecutar las migraciones o iniciar la app por primera vez, se inyectan estos usuarios:

| Email | Contraseña | Rol / Descripción |
| :--- | :--- | :--- |
| **admin@logika.com** | `adminpassword` | Usuario Administrador Principal |
| **juan.perez@example.com** | `password123` | Usuario de prueba para CRUD |
| **maria.garcia@example.com** | `password123` | Segundo usuario para pruebas de propiedad |

---

## 🧪 Pruebas y Validación

### Pruebas Unitarias
Orientadas a probar la lógica de los servicios y endpoints de forma aislada.
```bash
pytest tests/unit
```

### Scripts de Integración (Pruebas End-to-End)
Estos scripts ejecutan peticiones HTTP reales contra la API levantada. **Importante**: Asegúrate de que la app esté corriendo en `http://localhost:8000`.

1.  **Autenticación**: `python verify_auth.py`
2.  **Gestión de Tareas**: `python verify_tasks.py` (Limpia sus propios datos al terminar).
3.  **Propiedad (Security)**: `python verify_ownership.py` (Verifica que el Usuario A no vea lo del Usuario B).

---

## 📌 Justificación Técnica

*   **Índices**: Se indexó `user_id` porque es la columna de unión principal y filtro de seguridad. `status` y `created_at` se indexaron para optimizar el listado paginado y ordenado que la UI suele requerir.
*   **Aislamiento**: El uso de `Depends(get_current_user)` en todos los endpoints de `tasks` garantiza que ningún dato sea expuesto sin una sesión válida.
*   **Paginación**: Se implementó una paginación basada en `offset` y `limit`, devolviendo también metadatos como `total_pages` para facilitar el consumo desde el frontend.

---
**¡Prueba Finalizada con Éxito!**
