import requests
import sys

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
TASKS_URL = f"{BASE_URL}/api/v1/tasks/"

def obtener_token(email, password):
    """Auxiliar para obtener el token JWT."""
    payload = {"email": email, "password": password}
    response = requests.post(LOGIN_URL, json=payload)
    if response.status_code == 200:
        return response.json()["data"]["access_token"]
    else:
        print(f"❌ Error de inicio de sesión para {email}")
        sys.exit(1)

def probar_seguridad_propiedad():
    """Verifica que un usuario no pueda acceder a las tareas de otro."""
    print("--- Iniciando Pruebas de Seguridad de Propiedad ---")
    
    # 1. Login de dos usuarios diferentes
    token_juan = obtener_token("juan.perez@example.com", "password123")
    token_maria = obtener_token("maria.garcia@example.com", "password123")
    
    headers_juan = {"Authorization": f"Bearer {token_juan}"}
    headers_maria = {"Authorization": f"Bearer {token_maria}"}

    # 2. Juan crea una tarea
    print("Juan crea una tarea...")
    res_crear = requests.post(TASKS_URL, json={"title": "Tarea Secreta de Juan"}, headers=headers_juan)
    task_id = res_crear.json()["data"]["id"]
    print(f"Tarea {task_id} creada por Juan")
    
    # 3. María intenta ver la tarea de Juan (Debe fallar 403)
    print(f"María intenta OBTENER la Tarea {task_id} de Juan...")
    res_get = requests.get(f"{TASKS_URL}{task_id}", headers=headers_maria)
    if res_get.status_code == 403:
        print("✅ Acceso Denegado Verificado (403)")
    else:
        print(f"❌ ERROR: María pudo acceder o recibió un código inesperado: {res_get.status_code}")

    # 4. María intenta actualizar la tarea de Juan (Debe fallar 403)
    print(f"María intenta ACTUALIZAR la Tarea {task_id} de Juan...")
    res_put = requests.put(f"{TASKS_URL}{task_id}", json={"title": "Hackeado por María"}, headers=headers_maria)
    if res_put.status_code == 403:
        print("✅ Actualización Denegada Verificada (403)")
    else:
        print(f"❌ ERROR: Código inesperado en actualización: {res_put.status_code}")

    # 5. María intenta eliminar la tarea de Juan (Debe fallar 403)
    print(f"María intenta ELIMINAR la Tarea {task_id} de Juan...")
    res_del = requests.delete(f"{TASKS_URL}{task_id}", headers=headers_maria)
    if res_del.status_code == 403:
        print("✅ Eliminación Denegada Verificada (403)")
    else:
        print(f"❌ ERROR: Código inesperado en eliminación: {res_del.status_code}")

    # 6. María lista sus tareas (La tarea de Juan NO debe aparecer)
    print("María lista sus tareas...")
    res_list = requests.get(TASKS_URL, headers=headers_maria)
    tareas_maria = res_list.json()["data"]["items"]
    if any(t["id"] == task_id for t in tareas_maria):
        print(f"❌ ERROR: La tarea de Juan aparece en la lista de María")
    else:
        print("✅ La tarea de Juan no aparece en el listado de María")

    # 7. Limpieza: Juan elimina su tarea
    print("Limpiando datos (Juan elimina su tarea)...")
    requests.delete(f"{TASKS_URL}{task_id}", headers=headers_juan)
    print("✅ Tarea de Juan eliminada")

if __name__ == "__main__":
    probar_seguridad_propiedad()
    print("--- Pruebas de propiedad completadas ---")
