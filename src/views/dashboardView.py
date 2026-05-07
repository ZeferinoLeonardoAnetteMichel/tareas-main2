import flet as ft

def DashboardView(page: ft.Page, tarea_controller):
    user = getattr(page, "user_data", None)

    foto_ruta = "assets/predeterminado.png"

    foto_perfil = ft.CircleAvatar(
        foreground_image_src=foto_ruta,
        content=ft.Icon(ft.Icons.PERSON),
        radius=40,
        bgcolor=ft.Colors.PURPLE_100
    )

    avatar_mini = ft.CircleAvatar(
        foreground_image_src=foto_ruta,
        content=ft.Icon(ft.Icons.PERSON, size=15),
        radius=15,
        bgcolor=ft.Colors.PURPLE_100
    )

    txt_ultimo_acceso = ft.Text(
        value=f"Último ingreso: {user.get('ultimo_acceso', 'Primera vez') if user else ''}",
        size=12,
        italic=True,
        color=ft.Colors.BLUE_GREY
    )

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def eliminar_tarea(id_tarea):
        success, msg = tarea_controller.eliminar_tarea(id_tarea)
        if success:
            cargar_tareas()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_200)
            page.snack_bar.open = True
            page.update()

    def cargar_tareas():
        if user and 'id_usuario' in user:
            lista_tareas.controls.clear()
            tareas = tarea_controller.obtener_lista(user['id_usuario'])
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        elevation=5,
                        content=ft.Container(
                            bgcolor=ft.Colors.PURPLE_50,
                            border_radius=10,
                            padding=10,
                            content=ft.ListTile(
                                title=ft.Text(t['titulo'], weight="bold", color=ft.Colors.PURPLE_900),
                                subtitle=ft.Text(
                                    f"{t.get('descripcion', '')}\nPrioridad: {t.get('prioridad', 'media')}",
                                    color=ft.Colors.BLUE_GREY_700
                                ),
                                trailing=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text(t.get('estado', 'pendiente'), color=ft.Colors.WHITE),
                                            bgcolor=ft.Colors.PURPLE_300,
                                            padding=5,
                                            border_radius=5
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED,
                                            on_click=lambda e, id_t=t['id_tarea']: eliminar_tarea(id_t)
                                        )
                                    ],
                                    tight=True
                                )
                            )
                        )
                    )
                )
            page.update()

    txt_titulo = ft.TextField(label="Titulo", expand=True, bgcolor=ft.Colors.PURPLE_50)
    txt_descripcion = ft.TextField(label="Descripcion", expand=True, bgcolor=ft.Colors.PURPLE_50)

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
            ft.Radio(value="hogar", label="Hogar"),
            ft.Radio(value="salud", label="Salud"),
            ft.Radio(value="otro", label="Otro"), 
        ])
    )

    estado = ft.RadioGroup(
        value="pendiente",
        content=ft.Row([
            ft.Radio(value="pendiente", label="Pendiente"),
            ft.Radio(value="completada", label="Completada"),
            ft.Radio(value="En progreso", label="En progreso"),
            ft.Radio(value="Cancelada", label="Cancelada"),
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

    foto_input = ft.TextField(label="Ruta de la imagen", hint_text="assets/imagen.png")

    def cambiar_foto(e):
        nueva_ruta = foto_input.value
        foto_perfil.foreground_image_src = nueva_ruta
        avatar_mini.foreground_image_src = nueva_ruta
        page.update()

    dialogo = ft.AlertDialog(
        title=ft.Text("Perfil del Usuario", weight="bold", color=ft.Colors.PURPLE_900),
        bgcolor=ft.Colors.PURPLE_50,
        content=ft.Column([
            ft.Row([foto_perfil], alignment=ft.MainAxisAlignment.CENTER),
            ft.ElevatedButton("Cambiar foto", icon=ft.Icons.IMAGE, bgcolor=ft.Colors.PURPLE_200, on_click=cambiar_foto),
            foto_input,
            ft.Divider(color=ft.Colors.PURPLE_200),
            ft.Text(f"ID: {user.get('id_usuario', '')}"),
            ft.Text(f"Nombre: {user.get('nombre', '')}"),
            ft.Text(f"Apellido: {user.get('apellido', '')}"),
            ft.Text(f"Email: {user.get('email', '')}"),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.overlay.append(dialogo)

    def mostrar_perfil(e):
        if not user:
            return
        dialogo.open = True
        page.update()

    cargar_tareas()

    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Bienvenid@, {user.get('nombre', 'Usuario') if user else 'Usuario'}", color=ft.Colors.PURPLE_900),
                actions=[
                    ft.TextButton(
                        content=ft.Row([avatar_mini, ft.Text("Mi Perfil", color=ft.Colors.PURPLE_900)], spacing=5),
                        on_click=mostrar_perfil
                    ),
                    ft.IconButton(ft.Icons.LOGOUT, icon_color=ft.Colors.RED, on_click=lambda _: page.go("/"))
                ],
                bgcolor=ft.Colors.PURPLE_100
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Nueva Tarea:", size=30, weight="bold", color=ft.Colors.PURPLE_900),
                    ft.Row([txt_titulo, txt_descripcion]),
                    ft.Row([
                    ft.Column([
                        ft.Text("Prioridad:", weight="bold", color=ft.Colors.PURPLE_900),
                        prioridad,
                        ft.Divider(color=ft.Colors.PURPLE_100),
                        ft.Text("Clasificación:", weight="bold", color=ft.Colors.PURPLE_900),
                        clasificacion,
                        ft.Divider(color=ft.Colors.PURPLE_100),
                        ft.Text("Estado:", weight="bold", color=ft.Colors.PURPLE_900),
                        estado,
            ] , spacing=5, alignment=ft.MainAxisAlignment.START)

                    ], spacing=30, vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.ElevatedButton("Guardar", bgcolor=ft.Colors.PURPLE_300, on_click=agregar_tarea),
                    ft.Divider(color=ft.Colors.PURPLE_200),
                    ft.Text("Mis Tareas:", size=23, weight="bold", color=ft.Colors.PURPLE_900),
                    lista_tareas,
                    txt_ultimo_acceso,
                ], expand=True),
                padding=20,
                expand=True,
                bgcolor=ft.Colors.PURPLE_50,
                border_radius=15,
                
            ),
        ]
    )
