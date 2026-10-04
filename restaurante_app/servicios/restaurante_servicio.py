import os
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Servicio encargado de gestionar las operaciones y lógica de negocio del restaurante."""

    RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

    def __init__(self):
        self.usuarios = self._cargar_usuarios()

    def _cargar_usuarios(self) -> list[Usuario]:
        datos = ArchivoServicio.cargar_json(self.RUTA_USUARIOS)
        return [Usuario.from_dict(item) for item in datos]

    def _guardar_usuarios(self) -> bool:
        datos = [u.to_dict() for u in self.usuarios]
        return ArchivoServicio.guardar_json(self.RUTA_USUARIOS, datos)

    # --- AUTENTICACIÓN ---
    def autenticar(self, usuario_str: str, clave_str: str) -> Usuario | None:
        """Valida credenciales de acceso."""
        for u in self.usuarios:
            if u.usuario.strip() == usuario_str.strip() and u.clave == clave_str:
                return u
        return None

    # --- CRUD DE USUARIOS ---
    def obtener_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def obtener_usuario_por_id(self, id_usuario: str) -> Usuario | None:
        for u in self.usuarios:
            if u.id == id_usuario:
                return u
        return None

    def registrar_usuario(self, id_usuario: str, nombre: str, usuario_str: str, clave: str, rol: str) -> tuple[bool, str]:
        """Crea y persiste un nuevo usuario tras validar que no exista el ID ni el nombre de usuario."""
        if not all([id_usuario, nombre, usuario_str, clave, rol]):
            return False, "Todos los campos son obligatorios."

        if self.obtener_usuario_por_id(id_usuario):
            return False, f"El ID '{id_usuario}' ya está registrado."

        for u in self.usuarios:
            if u.usuario.lower() == usuario_str.lower():
                return False, f"El nombre de usuario '{usuario_str}' ya existe."

        nuevo_usuario = Usuario(id_usuario, nombre, usuario_str, clave, rol)
        self.usuarios.append(nuevo_usuario)
        if self._guardar_usuarios():
            return True, "Usuario registrado exitosamente."
        return False, "Error al guardar en el archivo JSON."

    def actualizar_usuario(self, id_usuario: str, nombre: str, usuario_str: str, clave: str, rol: str) -> tuple[bool, str]:
        """Actualiza un usuario existente."""
        u = self.obtener_usuario_por_id(id_usuario)
        if not u:
            return False, "El usuario seleccionado no existe."

        if not all([nombre, usuario_str, rol]):
            return False, "Los campos Nombre, Usuario y Rol no pueden estar vacíos."

        # Verificar unicidad de username excluyendo el propio usuario
        for otro in self.usuarios:
            if otro.id != id_usuario and otro.usuario.lower() == usuario_str.lower():
                return False, f"El nombre de usuario '{usuario_str}' ya está en uso por otra cuenta."

        u.nombre = nombre
        u.usuario = usuario_str
        if clave.strip():  # Actualiza clave solo si se proporciona una nueva
            u.clave = clave
        u.rol = rol

        if self._guardar_usuarios():
            return True, "Usuario actualizado correctamente."
        return False, "Error al actualizar la persistencia JSON."

    def eliminar_usuario(self, id_usuario: str, id_autenticado: str) -> tuple[bool, str]:
        """Elimina un usuario del sistema, protegiendo la cuenta en sesión actual."""
        if id_usuario == id_autenticado:
            return False, "No puede eliminar la cuenta con la que ha iniciado sesión actualmente."

        u = self.obtener_usuario_por_id(id_usuario)
        if not u:
            return False, "El usuario a eliminar no existe."

        self.usuarios.remove(u)
        if self._guardar_usuarios():
            return True, f"Usuario '{u.usuario}' eliminado correctamente."
        return False, "Error al guardar los cambios en JSON."