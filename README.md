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
3.  **Logs Estructurados**: Implementación de `structlog` para logs profesionales que facilitan la auditoría.
4.  **Inicialización Automática (Seeders)**: El sistema inyecta automáticamente 3 usuarios y 22 tareas de ejemplo al iniciar, permitiendo pruebas inmediatas sin configuración manual.
5.  **Pruebas Unitarias e Integración**: Suite de pruebas con `pytest` y scripts de verificación end-to-end.

---

## 📂 Estructura del Código

```text
.
├── alembic/                # Historial de migraciones de la base de datos
├── app/
│   ├── api/                # Enrutadores (Endpoints) y dependencias de seguridad
│   ├── core/               # Configuraciones globales, seguridad JWT y lógica de logging
│   ├── db/                 # Gestión de la sesión de SQLAlchemy y scripts de datos semilla
│   ├── exceptions/         # Definición de excepciones personalizadas y sus manejadores HTTP
│   ├── mappers/            # Capa de transformación para convertir Entidades ORM a DTOs de respuesta
│   ├── models/             # Definición de tablas de la base de datos (SQLAlchemy)
│   └── schemas/            # Definición de modelos de validación y entrada/salida (Pydantic)
├── tests/                  # Pruebas unitarias automatizadas
├── Dockerfile              # Configuración de la imagen de la aplicación (Multi-stage)
├── docker-compose.yml      # Definición de servicios (App de FastAPI + Base de Datos Postgres)
├── entrypoint.sh           # Script que asegura que la DB esté lista antes de migrar e iniciar
├── main.py                 # Inicialización de la aplicación FastAPI y registro de routers
└── .gitignore              # Archivos y carpetas excluidos del control de versiones
```

---

## 🛠️ Instrucciones de Ejecución Paso a Paso

### Opción A: Ejecución con Docker (Recomendada)
Docker es la opción preferida ya que crea un entorno aislado y configura la base de datos automáticamente.

1.  **Requisitos**: Tener instalado [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/).
2.  **Configuración de Variables**: Aunque el `docker-compose.yml` tiene valores por defecto para pruebas rápidas, se recomienda crear un archivo `.env` en la carpeta raíz con el siguiente contenido:
    ```env
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=logika_db
    DB_USER=postgres
    DB_PASSWORD=postgres
    SECRET_KEY=clave_secreta_para_jwt_aqui
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```
3.  **Lanzar el proyecto**: Abre una terminal en la raíz del proyecto y ejecuta:
    ```bash
    docker compose up --build
    ```
    *   **¿Qué sucede detrás de cámaras?**:
        *   Se descarga la imagen de PostgreSQL y se crea la base de datos.
        *   Se construye la imagen de la aplicación Python.
        *   El script `entrypoint.sh` detecta cuando la base de datos está lista para recibir conexiones.
        *   Se ejecutan las **migraciones de Alembic** para crear las tablas y los **usuarios iniciales**.
        *   La aplicación se inicia en el puerto `8000`.
4.  **Verificación**:
    *   Visita `http://localhost:8000/docs` para ver la documentación interactiva de Swagger.

---

### Opción B: Ejecución Local (Desarrollo Manual)
Si prefieres tener control manual sobre el proceso o no deseas usar Docker para la aplicación:

1.  **Base de Datos**: Debes tener una instancia de PostgreSQL accesible.
2.  **Entorno Virtual**: Crea un entorno de Python 3.11.8 para evitar conflictos de librerías:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # MacOS/Linux
    # .venv\Scripts\activate   # Windows
    ```
3.  **Instalación**: Instala todas las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuración**: Crea un archivo `.env` y asegúrate de que `DB_HOST` apunte a tu servidor de Postgres (normalmente `localhost`).
5.  **Migraciones y Datos**: Ejecuta este comando para crear las tablas y las semillas:
    ```bash
    alembic upgrade head
    ```
6.  **Arranque**: Inicia el servidor de desarrollo:
    ```bash
    uvicorn main:app --reload
    ```

---

## 👤 Usuarios de Prueba e Inicio de Sesión

Para probar la API, puedes usar las siguientes credenciales pre-cargadas:

| Email | Contraseña | Objetivo de Prueba |
| :--- | :--- | :--- |
| **admin@logika.com** | `adminpassword` | Verificar acceso total y datos semilla iniciales. |
| **juan.perez@example.com** | `password123` | Probar la creación y edición de tareas propias. |
| **maria.garcia@example.com** | `password123` | Verificar que no puede ver las tareas de `juan.perez`. |

---

## 🧪 Cómo Ejecutar las Pruebas

### 1. Pruebas Unitarias (Slogan: "Calidad de Código")
Ejecuta la suite de pruebas internas para validar la lógica sin depender de una base de datos real:
```bash
pytest tests/unit
```

### 2. Pruebas de Integración (Slogan: "Flujo Real")
Con el servidor corriendo (`docker compose up`), abre otra terminal y ejecuta estos scripts para validar el comportamiento real punto a punto:
*   `python verify_auth.py`: Valida el proceso de autenticación JWT.
*   `python verify_tasks.py`: Valida el CRUD completo, incluyendo el borrado suave y la paginación.
*   `python verify_ownership.py`: Valida la seguridad de aislamiento (Ownership) entre diferentes usuarios.

---

## 📌 Decisiones Técnicas Destacadas

*   **Paginación**: Se utiliza el estándar REST de parámetros `page` y `page_size`, devolviendo una estructura que incluye el total de páginas para facilitar la navegación en el frontend.
*   **Aislamiento de Recursos**: Se implementó una lógica donde el `user_id` es inyectado desde el token JWT en cada consulta, impidiendo que un ID de tarea manipulado por el usuario pueda exponer datos de terceros.
*   **Logging en Tiempo Real**: Configurado para mostrar marcas de tiempo y niveles de severidad claramente en la consola, facilitando la depuración durante el desarrollo.

---
**¡Prueba Finalizada con Éxito!**
*Desarrollado para el proceso de selección de Logika.*
