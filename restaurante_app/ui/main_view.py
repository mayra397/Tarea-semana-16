import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Tk):
    def __init__(self, usuario_autenticado: Usuario, servicio: RestauranteServicio):
        super().__init__()
        self.usuario_actual = usuario_autenticado
        self.servicio = servicio

        self.title("RestauranteApp - Gestión de Restaurante")
        self.geometry("1024x680")
        self.minsize(900, 600)

        # Carga de Recursos Visuales (assets)
        self.iconos = {}
        self._cargar_assets()

        # Estilos visuales ttk
        self._configurar_estilos()

        # Contenedor Principal
        self._crear_layout()

    def _cargar_assets(self):
        """Carga imágenes e íconos desde la carpeta assets/."""
        ruta_assets = os.path.join(os.path.dirname(__file__), "..", "assets")
        
        def _obtener_img(nombre, size=(20, 20)):
            path = os.path.join(ruta_assets, nombre)
            if os.path.exists(path):
                img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            return None

        self.iconos["logo"] = _obtener_img("logo.png", size=(40, 40))
        self.iconos["add"] = _obtener_img("icon_add.png")
        self.iconos["update"] = _obtener_img("icon_update.png")
        self.iconos["delete"] = _obtener_img("icon_delete.png")
        self.iconos["clean"] = _obtener_img("icon_clean.png")

        if self.iconos["logo"]:
            self.iconphoto(False, self.iconos["logo"])

    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Estilos generales
        style.configure("TFrame", background="#F5F6FA")
        style.configure("Header.TFrame", background="#2C3E50")
        style.configure("Header.TLabel", background="#2C3E50", foreground="#FFFFFF", font=("Segoe UI", 12, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), background="#F5F6FA", foreground="#2C3E50")
        style.configure("Status.TLabel", font=("Segoe UI", 9, "italic"), background="#F5F6FA", foreground="#7F8C8D")

        # Treeview
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=26, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#ECF0F1", foreground="#2C3E50")
        style.map("Treeview", background=[("selected", "#3498DB")], foreground=[("selected", "#FFFFFF")])

    def _crear_layout(self):
        # Header / Barra Superior
        header = ttk.Frame(self, style="Header.TFrame", padding=10)
        header.pack(fill=tk.X, side=tk.TOP)

        if self.iconos["logo"]:
            lbl_logo = ttk.Label(header, image=self.iconos["logo"], style="Header.TLabel")
            lbl_logo.pack(side=tk.LEFT, padx=(0, 10))

        lbl_titulo = ttk.Label(header, text="RESTAURANTE APP - SISTEMA DE GESTIÓN", style="Header.TLabel")
        lbl_titulo.pack(side=tk.LEFT)

        info_user = f"Usuario: {self.usuario_actual.nombre} | Rol: {self.usuario_actual.rol}"
        lbl_user = ttk.Label(header, text=info_user, style="Header.TLabel")
        lbl_user.pack(side=tk.RIGHT)

        # Panel de Pestañas / Cuaderno
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Pestaña Gestión de Usuarios (Solo Administrador)
        if self.usuario_actual.rol == "Administrador":
            self.tab_usuarios = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.tab_usuarios, text="Gestión de Usuarios")
            self._construir_modulo_usuarios()
        else:
            self.tab_bloqueada = ttk.Frame(self.notebook, padding=20)
            self.notebook.add(self.tab_bloqueada, text="Panel General")
            ttk.Label(self.tab_bloqueada, text="Bienvenido al sistema. Su rol actual no requiere administración de usuarios.", font=("Segoe UI", 11)).pack(pady=20)

    # -------------------------------------------------------------------------
    # MÓDULO DE GESTIÓN DE USUARIOS (SEMANA 16)
    # -------------------------------------------------------------------------
    def _construir_modulo_usuarios(self):
        # Layout dividido: Izquierda Formulario, Derecha Tabla
        frame_izq = ttk.Frame(self.tab_usuarios)
        frame_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        frame_der = ttk.Frame(self.tab_usuarios)
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- FORMULARIO DE USUARIOS ---
        lbl_form = ttk.Label(frame_izq, text="Formulario de Usuario", style="Title.TLabel")
        lbl_form.pack(anchor=tk.W, pady=(0, 10))

        form_grid = ttk.Frame(frame_izq)
        form_grid.pack(fill=tk.X)

        ttk.Label(form_grid, text="ID Usuario:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.ent_id = ttk.Entry(form_grid, width=22)
        self.ent_id.grid(row=0, column=1, pady=4, padx=(5, 0))

        ttk.Label(form_grid, text="Nombre Completo:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.ent_nombre = ttk.Entry(form_grid, width=22)
        self.ent_nombre.grid(row=1, column=1, pady=4, padx=(5, 0))

        ttk.Label(form_grid, text="Usuario:").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.ent_usuario = ttk.Entry(form_grid, width=22)
        self.ent_usuario.grid(row=2, column=1, pady=4, padx=(5, 0))

        ttk.Label(form_grid, text="Contraseña:").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.ent_clave = ttk.Entry(form_grid, show="*", width=22)
        self.ent_clave.grid(row=3, column=1, pady=4, padx=(5, 0))

        ttk.Label(form_grid, text="Rol:").grid(row=4, column=0, sticky=tk.W, pady=4)
        self.cmb_rol = ttk.Combobox(form_grid, values=["Administrador", "Empleado", "Cliente"], state="readonly", width=20)
        self.cmb_rol.current(1)  # Por defecto Empleado
        self.cmb_rol.grid(row=4, column=1, pady=4, padx=(5, 0))

        # Indicador de estado del rol seleccionado (Respuesta visual a <<ComboboxSelected>>)
        self.lbl_rol_info = ttk.Label(frame_izq, text="Rol seleccionado: Empleado", style="Status.TLabel")
        self.lbl_rol_info.pack(anchor=tk.W, pady=(5, 10))

        # --- BOTONES DE ACCIÓN (utilizando command=) ---
        frame_btn = ttk.Frame(frame_izq)
        frame_btn.pack(fill=tk.X, pady=10)

        self.btn_registrar = ttk.Button(frame_btn, text="Registrar", image=self.iconos.get("add"), compound=tk.LEFT, command=self._cmd_registrar)
        self.btn_registrar.grid(row=0, column=0, padx=2, pady=2, sticky=tk.EW)

        self.btn_actualizar = ttk.Button(frame_btn, text="Actualizar", image=self.iconos.get("update"), compound=tk.LEFT, command=self._cmd_actualizar)
        self.btn_actualizar.grid(row=0, column=1, padx=2, pady=2, sticky=tk.EW)

        self.btn_eliminar = ttk.Button(frame_btn, text="Eliminar", image=self.iconos.get("delete"), compound=tk.LEFT, command=self._cmd_eliminar)
        self.btn_eliminar.grid(row=1, column=0, padx=2, pady=2, sticky=tk.EW)

        self.btn_limpiar = ttk.Button(frame_btn, text="Limpiar", image=self.iconos.get("clean"), compound=tk.LEFT, command=self._cmd_limpiar)
        self.btn_limpiar.grid(row=1, column=1, padx=2, pady=2, sticky=tk.EW)

        frame_btn.columnconfigure(0, weight=1)
        frame_btn.columnconfigure(1, weight=1)

        # Atajos Teclado e Instrucciones
        lbl_help = ttk.Label(frame_izq, text="Atajos:\n• [Enter] → Confirmar Registro\n• [Escape] → Limpiar Formulario", style="Status.TLabel", justify=tk.LEFT)
        lbl_help.pack(anchor=tk.W, pady=(10, 0))

        # --- TABLA TREEVIEW DE USUARIOS ---
        ttk.Label(frame_der, text="Lista de Usuarios Registrados", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 10))

        columnas = ("id", "nombre", "usuario", "rol")
        self.tree_usuarios = ttk.Treeview(frame_der, columns=columnas, show="headings", selectmode="browse")

        self.tree_usuarios.heading("id", text="ID")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("usuario", text="Usuario")
        self.tree_usuarios.heading("rol", text="Rol")

        self.tree_usuarios.column("id", width=70, anchor=tk.CENTER)
        self.tree_usuarios.column("nombre", width=180, anchor=tk.W)
        self.tree_usuarios.column("usuario", width=120, anchor=tk.W)
        self.tree_usuarios.column("rol", width=110, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame_der, orient=tk.VERTICAL, command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscroll=scrollbar.set)

        self.tree_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- EVENT BINDINGS (REQUERIMIENTO PRINCIPAL SEMANA 16) ---
        # 1. Selección en la tabla
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_treeview_select)
        # 2. Cambio de opción en Combobox
        self.cmb_rol.bind("<<ComboboxSelected>>", self._on_combobox_selected)
        # 3. Tecla Return (Enter) para registrar
        self.bind("<Return>", self._on_key_return)
        # 4. Tecla Escape para limpiar selección y formulario
        self.bind("<Escape>", self._on_key_escape)

        # Carga Inicial de Datos
        self._actualizar_treeview()

    # -------------------------------------------------------------------------
    # CALLBACKS Y MANEJO DE EVENTOS (bind)
    # -------------------------------------------------------------------------
    def _on_treeview_select(self, event):
        """Callback <<TreeviewSelect>>: Carga el usuario seleccionado usando su ID."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return

        item = self.tree_usuarios.item(seleccion[0])
        id_usuario = item["values"][0]

        # Consulta segura mediante RestauranteServicio
        usuario = self.servicio.obtener_usuario_por_id(str(id_usuario))
        if usuario:
            self.ent_id.delete(0, tk.END)
            self.ent_id.insert(0, usuario.id)
            self.ent_id.configure(state="disabled")  # Deshabilitar ID para evitar cambios en actualización

            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, usuario.nombre)

            self.ent_usuario.delete(0, tk.END)
            self.ent_usuario.insert(0, usuario.usuario)

            self.ent_clave.delete(0, tk.END)
            self.ent_clave.insert(0, "")  # No exponer la contraseña en texto claro

            self.cmb_rol.set(usuario.rol)
            self.lbl_rol_info.configure(text=f"Rol seleccionado: {usuario.rol}")

    def _on_combobox_selected(self, event):
        """Callback <<ComboboxSelected>>: Responde dinámicamente a la selección de rol."""
        rol = self.cmb_rol.get()
        self.lbl_rol_info.configure(text=f"Rol seleccionado: {rol}")

    def _on_key_return(self, event):
        """Callback <Return>: Atajo para ejecutar el registro reutilizando el comando existente."""
        # Evita ejecutar si la caja de ID está deshabilitada (modo edición)
        if self.ent_id.cget("state") != "disabled":
            self._cmd_registrar()

    def _on_key_escape(self, event):
        """Callback <Escape>: Atajo para limpiar formulario y cancelar selección."""
        self._cmd_limpiar()

    # -------------------------------------------------------------------------
    # LÓGICA DE COMANDOS (command=) Y REUTILIZACIÓN
    # -------------------------------------------------------------------------
    def _cmd_registrar(self):
        id_u = self.ent_id.get().strip()
        nombre = self.ent_nombre.get().strip()
        usr = self.ent_usuario.get().strip()
        clave = self.ent_clave.get().strip()
        rol = self.cmb_rol.get()

        exito, msg = self.servicio.registrar_usuario(id_u, nombre, usr, clave, rol)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._actualizar_treeview()
            self._cmd_limpiar()
        else:
            messagebox.showwarning("Atención", msg)

    def _cmd_actualizar(self):
        id_u = self.ent_id.get().strip()
        nombre = self.ent_nombre.get().strip()
        usr = self.ent_usuario.get().strip()
        clave = self.ent_clave.get().strip()
        rol = self.cmb_rol.get()

        if self.ent_id.cget("state") != "disabled":
            messagebox.showwarning("Atención", "Seleccione primero un usuario de la tabla para actualizar.")
            return

        exito, msg = self.servicio.actualizar_usuario(id_u, nombre, usr, clave, rol)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._actualizar_treeview()
            self._cmd_limpiar()
        else:
            messagebox.showwarning("Atención", msg)

    def _cmd_eliminar(self):
        id_u = self.ent_id.get().strip()
        if not id_u or self.ent_id.cget("state") != "disabled":
            messagebox.showwarning("Atención", "Seleccione un usuario desde la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el usuario con ID '{id_u}'?")
        if confirmar:
            exito, msg = self.servicio.eliminar_usuario(id_u, self.usuario_actual.id)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self._actualizar_treeview()
                self._cmd_limpiar()
            else:
                messagebox.showerror("Error", msg)

    def _cmd_limpiar(self):
        """Limpia el formulario y deselecciona la fila del Treeview."""
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_usuario.delete(0, tk.END)
        self.ent_clave.delete(0, tk.END)
        self.cmb_rol.current(1)
        self.lbl_rol_info.configure(text="Rol seleccionado: Empleado")

        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())

    def _actualizar_treeview(self):
        """Refresca las filas del Treeview recuperando los usuarios desde RestauranteServicio."""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        usuarios = self.servicio.obtener_usuarios()
        for u in usuarios:
            self.tree_usuarios.insert("", tk.END, values=(u.id, u.nombre, u.usuario, u.rol))