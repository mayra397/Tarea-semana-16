# RestauranteApp - Semana 16: Manejo de Eventos

## Descripción General
Esta entrega corresponde a la **Semana 16** de la asignatura Programación Orientada a Objetos. Se ha evolucionado la aplicación gráfica `restaurante_app` incorporando el **manejo de eventos en Tkinter** aplicado al módulo de **Gestión de Usuarios**.

## Arquitectura Modular
El proyecto mantiene una separación en capas rigurosa:
- **`modelos/`**: Define la entidad `Usuario` con soporte para el atributo `rol` (`Administrador`, `Empleado`, `Cliente`).
- **`servicios/`**: `RestauranteServicio` centraliza la lógica de negocio, validaciones y coordinación con `ArchivoServicio` para la persistencia JSON.
- **`ui/`**: `MainView` gestiona la interfaz gráfica mediante componentes `ttk` y captura la interacción del usuario a través de eventos y comandos.
- **`datos/`**: Almacenamiento persistente en formato JSON (`usuarios.json`).
- **`assets/`**: Recursos visuales (logotipos e íconos) integrados en botones y títulos.

## Eventos Implementados (`bind` vs `command`)

1. **`<<TreeviewSelect>>`**:
   - **Mecanismo:** `bind("<<TreeviewSelect>>", callback)`
   - **Función:** Al hacer clic en una fila del `Treeview`, obtiene el identificador (`ID`) de la celda y consulta la entidad completa mediante `RestauranteServicio`, cargando los campos en el formulario sin exponer contraseñas en la tabla.

2. **`<<ComboboxSelected>>`**:
   - **Mecanismo:** `bind("<<ComboboxSelected>>", callback)`
   - **Función:** Responde dinámicamente al cambio de opción en el selector de rol actualizando la etiqueta descriptiva de la interfaz.

3. **Atajo Teclado `<Return>`**:
   - **Mecanismo:** `bind("<Return>", callback)`
   - **Función:** Permite confirmar el registro de un nuevo usuario presionando la tecla **Enter**, reutilizando la lógica del botón `Registrar`.

4. **Atajo Teclado `<Escape>`**:
   - **Mecanismo:** `bind("<Escape>", callback)`
   - **Función:** Cancela la selección actual en el `Treeview` y limpia todos los campos del formulario devolviéndolo a su estado inicial.

5. **Acciones Principales (`command=`)**:
   - Los botones **Registrar**, **Actualizar**, **Eliminar** y **Limpiar** utilizan la propiedad `command=` para invocar métodos directos de la vista.

## Instrucciones de Ejecución

1. Clonar el repositorio y asegurarse de tener instalado Python 3.10+ y la biblioteca `Pillow`:
   ```bash
   pip install pillow