from models.UserModel import UsuarioModel
class AuthController:
    def __init__(self):
        self.usuario_model = UsuarioModel()

    def login(self, email, password):
        try:
            user_db = self.usuario_model.validar_login(email, password)

            if not user_db:
                return None, "Correo o contraseña incorrectos"

            user = {
                "id_usuario": user_db["id_usuario"],
                "nombre": user_db["nombre"],
                "apellido": user_db["apellido"],
                "email": user_db["email"]
            }

            return user, "Login exitoso"

        except Exception as e:
            return None, f"Error en login: {str(e)}"
    
    def registrar(self, usuario_data):
        try:
            if self.usuario_model.email_existe(usuario_data.email):
                return False, "El correo electrónico ya está registrado"
            exito = self.usuario_model.registrar(usuario_data)
            
            if exito:
                return True, "Usuario registrado exitosamente"
            else:
                return False, "Error al registrar usuario"
                
        except Exception as e:
            return False, f"Error en registro: {str(e)}"
        
def login_exitoso(page, user_data): 
    cuentas = page.client_storage.get("perfiles_activos") or []
    
    nuevo_perfil = {
        "id": user_data['id_usuario'],
        "nombre": user_data['nombre'],
        "fecha": user_data.get('ultimo_acceso', 'Reciente')
    }
    
    # Evitar duplicados
    if not any(p['id'] == nuevo_perfil['id'] for p in cuentas):
        cuentas.append(nuevo_perfil)
        page.client_storage.set("perfiles_activos", cuentas)
    
    # Después de guardar, usualmente querrás navegar al dashboard
    page.go("/dashboard")