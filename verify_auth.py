import requests
import sys

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"

def probar_inicio_sesion_exitoso():
    """Verifica que un usuario con credenciales correctas pueda obtener un token."""
    print(f"Probando inicio de sesión exitoso en {LOGIN_URL}...")
    payload = {
        "email": "admin@logika.com",
        "password": "adminpassword"
    }
    try:
        response = requests.post(LOGIN_URL, json=payload)
        print(f"Estado: {response.status_code}")
        if response.status_code == 200 and response.json()["success"]:
            print("✅ Inicio de sesión exitoso verificado")
            return response.json()["data"]["access_token"]
        else:
            print(f"❌ Fallo en inicio de sesión exitoso: {response.json()}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_fallo_inicio_sesion_password():
    """Verifica que el sistema rechace contraseñas incorrectas."""
    print("Probando fallo de inicio de sesión (contraseña incorrecta)...")
    payload = {
        "email": "admin@logika.com",
        "password": "password_equivocada"
    }
    try:
        response = requests.post(LOGIN_URL, json=payload)
        print(f"Estado: {response.status_code}")
        # Según handlers.py, InvalidCredentialsException retorna 400
        if response.status_code == 400 and response.json()["success"] == False:
            print("✅ Fallo por contraseña incorrecta verificado (400)")
        else:
            print(f"❌ Error: Se esperaba 400, se obtuvo {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

def probar_fallo_inicio_sesion_usuario():
    """Verifica que el sistema rechace usuarios inexistentes."""
    print("Probando fallo de inicio de sesión (usuario inexistente)...")
    payload = {
        "email": "noexiste@logika.com",
        "password": "cualquiercosa"
    }
    try:
        response = requests.post(LOGIN_URL, json=payload)
        print(f"Estado: {response.status_code}")
        # Según handlers.py, UserNotFoundException retorna 404
        if response.status_code == 404 and response.json()["success"] == False:
            print("✅ Fallo por usuario inexistente verificado (404)")
        else:
            print(f"❌ Error: Se esperaba 404, se obtuvo {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Excepción: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("--- Iniciando Pruebas de Autenticación ---")
    probar_fallo_inicio_sesion_password()
    probar_fallo_inicio_sesion_usuario()
    probar_inicio_sesion_exitoso()
    print("✅ Todas las pruebas de autenticación pasaron")
