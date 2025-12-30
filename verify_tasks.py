import requests
import sys

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
TASKS_URL = f"{BASE_URL}/api/v1/tasks/"

def iniciar_sesion(email, password):
    """Obtiene el token de acceso para un usuario."""
    print(f"Iniciando sesión como {email}...")
    payload = {"email": email, "password": password}
    try:
        response = requests.post(LOGIN_URL, json=payload)
        if response.status_code == 200:
            token = response.json()["data"]["access_token"]
            print("✅ Inicio de sesión exitoso")
            return token
        else:
            print(f"❌ Error al iniciar sesión: {response.json()}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción durante el inicio de sesión: {e}")
        sys.exit(1)

def probrar_acceso_no_autorizado():
    """Verifica que no se pueda acceder a las tareas sin token."""
    print("Probando acceso no autorizado...")
    try:
        response = requests.get(TASKS_URL)
        if response.status_code == 401:
            print("✅ Acceso no autorizado verificado (401)")
        else:
            print(f"❌ Error: Se esperaba 401, pero se obtuvo {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_creacion_tarea(token):
    """Verifica la creación de una tarea."""
    print("Probando creación de tarea...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Tarea de Prueba de Integración",
        "description": "Descripción detallada",
        "status": "pending"
    }
    try:
        response = requests.post(TASKS_URL, json=payload, headers=headers)
        if response.status_code == 201:
            task_id = response.json()["data"]["id"]
            print(f"✅ Tarea {task_id} creada correctamente")
            return task_id
        else:
            print(f"❌ Fallo al crear tarea: {response.json()}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_obtener_tarea(task_id, token):
    """Verifica la obtención de una tarea específica."""
    print(f"Probando obtención de tarea {task_id}...")
    url = f"{TASKS_URL}{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.json()["data"]["id"] == task_id:
            print("✅ Obtención de tarea verificada")
        else:
            print("❌ Error al obtener la tarea")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_actualizacion_tarea(task_id, token):
    """Verifica la edición de una tarea."""
    print(f"Probando actualización de tarea {task_id}...")
    url = f"{TASKS_URL}{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Título Actualizado",
        "status": "in_progress"
    }
    try:
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == 200 and response.json()["data"]["title"] == "Título Actualizado":
            print("✅ Actualización de tarea verificada")
        else:
            print("❌ Fallo al actualizar la tarea")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_eliminacion_tarea(task_id, token):
    """Verifica el borrado lógico de una tarea."""
    print(f"Probando eliminación de tarea {task_id}...")
    url = f"{TASKS_URL}{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("✅ Eliminación de tarea verificada")
        else:
            print("❌ Fallo al eliminar la tarea")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_paginacion(token):
    """Verifica que la paginación funcione y limpia los datos creados."""
    print("Probando paginación...")
    headers = {"Authorization": f"Bearer {token}"}
    ids_creados = []
    
    # Crear tareas para probar paginación
    for i in range(5):
        payload = {"title": f"Tarea Paginada {i}", "description": "desc", "status": "pending"}
        res = requests.post(TASKS_URL, json=payload, headers=headers)
        if res.status_code == 201:
            ids_creados.append(res.json()["data"]["id"])
    
    url = f"{TASKS_URL}?page=1&page_size=3"
    try:
        response = requests.get(url, headers=headers)
        res_json = response.json()
        if len(res_json["data"]["items"]) <= 3:
            print("✅ Paginación verificada correctamente")
        else:
            print(f"❌ Error en paginación: Se obtuvieron {len(res_json['data']['items'])} elementos")
    
        # Limpieza (Eliminar tareas creadas para la prueba)
        print("Limpiando datos de prueba...")
        for t_id in ids_creados:
            requests.delete(f"{TASKS_URL}{t_id}", headers=headers)
        print("✅ Datos de prueba eliminados")
            
    except Exception as e:
        print(f"❌ Excepción en paginación: {e}")

if __name__ == "__main__":
    print("--- Iniciando Pruebas de Integración (Tareas) ---")
    probrar_acceso_no_autorizado()
    token = iniciar_sesion("admin@logika.com", "adminpassword")
    task_id = probar_creacion_tarea(token)
    probar_obtener_tarea(task_id, token)
    probar_actualizacion_tarea(task_id, token)
    probar_eliminacion_tarea(task_id, token)
    probar_paginacion(token)
    print("--- Todas las pruebas de tareas completadas con éxito ---")
