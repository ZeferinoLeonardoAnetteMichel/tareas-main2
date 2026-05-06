import flet as ft

def DashboardView(page, tarea_controller):
    user = getattr(page, "user_data", None)
    txt_ultimo_acceso = ft.Text(
        value=f"Último ingreso: {user.get('ultimo_acceso', 'Primera vez') if user else ''}",
        size=12,
        italic=True,
    )
    
    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def eliminar_tarea(id_tarea):
        success, msg = tarea_controller.eliminar_tarea(id_tarea)
        if success:
            cargar_tareas()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
            page.snack_bar.open = True
            page.update()
    
    def cargar_tareas():
        if user and 'id_usuario' in user:
            lista_tareas.controls.clear()
            tareas = tarea_controller.obtener_lista(user['id_usuario'])
            
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(t['titulo'], weight="bold"),
                                subtitle=ft.Text(f"{t.get('descripcion', '')}\nPrioridad: {t.get('prioridad', 'media')}"),
                                trailing=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text(t.get('estado', 'pendiente')),
                                            padding=5,
                                            border_radius=5
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="black",
                                            on_click=lambda e, id_t=t['id_tarea']: eliminar_tarea(id_t)
                                        )
                                    ],
                                    tight=True
                                )
                            ),
                            padding=10
                        )
                    )
                )
            page.update()
    
    txt_titulo = ft.TextField(label="Titulo", expand=True)
    txt_descripcion = ft.TextField(label="Descripcion", expand=True)
    
    prioridad = ft.RadioGroup(
        value="media",
        content=ft.Row([
            ft.Radio(value="alta", label="Alta"),
            ft.Radio(value="media", label="Media"),
            ft.Radio(value="baja", label="Baja"),
        ])
    )
    
    clasificacion = ft.RadioGroup(
        value="personal",
        content=ft.Row([
            ft.Radio(value="personal", label="Personal"),
            ft.Radio(value="trabajo", label="Trabajo"),
            ft.Radio(value="estudio", label="Estudio"),
        ])
    )
    
    estado = ft.RadioGroup(
        value="pendiente",
        content=ft.Row([
            ft.Radio(value="pendiente", label="Pendiente"),
            ft.Radio(value="completada", label="Completada"),
        ])
    )
    
    def agregar_tarea(e):
        if user and 'id_usuario' in user:
            if not txt_titulo.value:
                return
            
            success, msg = tarea_controller.guardar_nueva(
                user['id_usuario'],
                txt_titulo.value,
                txt_descripcion.value,
                prioridad.value,
                clasificacion.value,
                estado.value
            )
            
            if success:
                txt_titulo.value = ""
                txt_descripcion.value = ""
                cargar_tareas()
                page.update()
    
    def mostrar_perfil(e):
        if not user:
            return
        
        dialogo = ft.AlertDialog(
            title=ft.Text("Perfil"),
            content=ft.Column([
                ft.Text(f"ID: {user.get('id_usuario', '')}"),
                ft.Text(f"Nombre: {user.get('nombre', '')}"),
                ft.Text(f"Apellido: {user.get('apellido', '')}"),
                ft.Text(f"Email: {user.get('email', '')}"),
            ], tight=True)
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()
    
    cargar_tareas()
    
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Bienvenid@, {user.get('nombre', 'Usuario') if user else 'Usuario'}"),
                actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=mostrar_perfil),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Nueva Tarea:", size=30, weight="bold",color="purple"),
                    ft.Row([txt_titulo, txt_descripcion]),
                    ft.Row([
                        ft.Column([ft.Text("Prioridad:"), prioridad], spacing=5),
                        ft.Column([ft.Text("Clasificacion:"), clasificacion], spacing=5),
                        ft.Column([ft.Text("Estado:"), estado], spacing=5),
                    ], spacing=30, vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.ElevatedButton("Guardar", on_click=agregar_tarea),
                    txt_ultimo_acceso,
                    ft.Divider(),
                    ft.Text("Mis Tareas:", size=23, weight="bold",color="purple"),
                    lista_tareas
                ], expand=True),
                padding=20,
                expand=True
            ),
        ]
    )