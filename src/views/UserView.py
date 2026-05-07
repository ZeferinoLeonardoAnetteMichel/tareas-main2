import flet as ft

def UserView(page, auth_controller):
    page.title = "Perfil"
    user = getattr(page, "user_data", None)

    foto_inicial = user.get('foto_perfil', None) if user else None
    
    avatar_perfil = ft.CircleAvatar(
        foreground_image_url=foto_inicial,
        content=ft.Icon(ft.icons.PERSON, size=80),
        radius=60,
    )

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files and e.files[0].path:
            nueva_ruta = e.files[0].path
            if nueva_ruta.lower().endswith((".png", ".jpg", ".jpeg")):
                if user:
                    user['foto_perfil'] = nueva_ruta
                    page.session.set("foto_perfil", nueva_ruta)

                avatar_perfil.foreground_image_url = nueva_ruta
                avatar_perfil.update()

                page.snack_bar = ft.SnackBar(
                    ft.Text("Foto de perfil actualizada"),
                    bgcolor=ft.colors.GREEN
                )
                page.snack_bar.open = True
                page.update()

    pick_files_dialog = ft.FilePicker(on_result=on_file_picked)
    if pick_files_dialog not in page.overlay:
        page.overlay.append(pick_files_dialog)

    btn_cambiar_foto = ft.ElevatedButton(
        "Cambiar foto",
        icon=ft.icons.EDIT,
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"]
        ),
        bgcolor=ft.colors.PURPLE_200,
        color=ft.colors.WHITE,
    )

    return ft.View(
        route="/perfil",
        controls=[
            ft.AppBar(
                title=ft.Text("Perfil de Usuario", size=30),
                actions=[
                    ft.IconButton(ft.Icons.BOOK, on_click=lambda _: page.go("/dashboard")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
                bgcolor=ft.colors.PURPLE_200,
                color=ft.colors.WHITE,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            avatar_perfil,
                            btn_cambiar_foto,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Divider(thickness=3, color=ft.colors.BLUE_GREY_100), 
                    ft.Text(f"Nombre: {user['nombre'] if user else 'Usuario'}", size=20),
                    ft.Text(f"Apellido: {user['apellido'] if user else 'Usuario'}", size=20),
                    ft.Text(f"Email: {user['email'] if user else 'Usuario'}", size=20),
                ], expand=True),
                padding=20,
            ),
        ]
    )
