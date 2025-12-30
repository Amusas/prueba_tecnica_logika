from sqlalchemy.orm import Session
from app.models.user import User
from app.models.task import Task
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.logging import logger
from app.core.enums import TaskStatus
import random

def init_db(db: Session) -> None:
    """
    Inicializa la base de datos con datos semilla (usuarios y tareas).
    
    Este proceso es idempotente: solo crea registros si no existen previamente.
    Se asegura de contar con al menos 3 usuarios y una base de 20+ tareas
    para pruebas inmediatas.
    """
    
    # 1. Semillas de Usuarios
    seed_users = [
        {
            "email": "admin@logika.com",
            "password": "adminpassword",
            "full_name": "Administrador del Sistema"
        },
        {
            "email": "juan.perez@example.com",
            "password": "password123",
            "full_name": "Juan Pérez"
        },
        {
            "email": "maria.garcia@example.com",
            "password": "password123",
            "full_name": "María García"
        }
    ]
    
    db_users = []
    for u_data in seed_users:
        user = db.query(User).filter(User.email == u_data["email"]).first()
        if not user:
            user = User(
                email=u_data["email"],
                hashed_password=get_password_hash(u_data["password"]),
                full_name=u_data["full_name"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Usuario semilla creado: {user.email}")
        else:
            logger.info(f"Usuario {user.email} ya existe")
        db_users.append(user)

    # 2. Semillas de Tareas
    # Solo inyectar si la base de datos está vacía o tiene pocos registros
    task_count = db.query(Task).count()
    if task_count < 20:
        logger.info(f"Inyectando tareas (actual: {task_count})...")
        
        tareas_data = [
            ("Completar informe mensual", "Preparar el documento con los KPIs de diciembre."),
            ("Revisión de código", "Revisar los Pull Requests pendientes en el repositorio de backend."),
            ("Reunión con cliente", "Discutir los nuevos requerimientos para el módulo de inventario."),
            ("Actualizar documentación", "Actualizar el manual de usuario con las últimas funcionalidades."),
            ("Optimizar base de datos", "Analizar índices y planes de ejecución para mejorar el rendimiento."),
            ("Pruebas de integración", "Ejecutar la suite de pruebas en el entorno de staging."),
            ("Diseño de UI", "Crear mockups para la nueva pantalla de perfil de usuario."),
            ("Corregir bug de login", "Investigar por qué algunos usuarios experimentan timeout al iniciar sesión."),
            ("Configurar CI/CD", "Ajustar los pipelines de GitHub Actions para despliegue automático."),
            ("Investigación de mercado", "Analizar a la competencia y documentar hallazgos."),
            ("Backup de seguridad", "Verificar que las copias de seguridad se estén realizando correctamente."),
            ("Capacitación interna", "Preparar charla sobre buenas prácticas de seguridad en APIs."),
            ("Migración de servidor", "Planificar el paso de AWS a Google Cloud."),
            ("Análisis de seguridad", "Realizar escaneo de vulnerabilidades en la infraestructura."),
            ("Planificación de sprint", "Definir las tareas para el próximo ciclo de desarrollo."),
            ("Revisión de logs", "Buscar errores recurrentes en los registros de producción."),
            ("Mejorar accesibilidad", "Asegurar que la web cumpla con los estándares WCAG 2.1."),
            ("Refactorización de servicios", "Limpiar el código duplicado en la capa de servicios."),
            ("Configuración de monitoreo", "Añadir alertas de Prometheus para el uso de memoria."),
            ("Entrevista técnica", "Evaluar candidatos para la posición de desarrollador Senior."),
            ("Elaboración de presupuesto", "Estimar costos de infraestructura para el próximo trimestre."),
            ("Soporte nivel 2", "Atender tickets escalados por el equipo de primera línea.")
        ]
        
        for title, desc in tareas_data:
            # Asignación aleatoria entre los usuarios semilla
            owner = random.choice(db_users)
            # Estado aleatorio para variedad visual en la app
            status = random.choice([TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
            
            new_task = Task(
                title=title,
                description=desc,
                status=status,
                user_id=owner.id
            )
            db.add(new_task)
        
        db.commit()
        logger.info(f"{len(tareas_data)} tareas inyectadas exitosamente.")
    else:
        logger.info("Ya existen suficientes tareas en la base de datos.")
