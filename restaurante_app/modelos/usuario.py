class Usuario:
    """Modelo de dominio que representa a un usuario del restaurante."""

    def __init__(self, id_usuario: str, nombre: str, usuario: str, clave: str, rol: str = "Cliente"):
        self.id = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.rol = rol  # "Administrador", "Empleado", "Cliente"

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para la persistencia JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia de Usuario a partir de un diccionario."""
        return cls(
            id_usuario=data.get("id", ""),
            nombre=data.get("nombre", ""),
            usuario=data.get("usuario", ""),
            clave=data.get("clave", ""),
            rol=data.get("rol", "Cliente")
        )