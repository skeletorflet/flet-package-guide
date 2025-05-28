import flet as ft
from flet_package_guide import FletPackageGuide


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def get_random():
        return FletPackageGuide(
            colors=[ft.Colors.RED, ft.Colors.BLUE, ft.Colors.PRIMARY],
            content=ft.Icon(ft.Icons.ABC),
            on_something=lambda e: print(e.data),
            complex_data={
                "hello": "world",
                "foo": "bar",
                "arrs": {"int": 1, "bool": True, "double": 1.123, "list": ["a", 2, True, [[2], 1]], "size": {"width":300, "height":300}},
            },
        )

    def click(e):
        package.colors = [ft.Colors.random() for i in range(3)]
        package.content = ft.Icon(ft.Icons.random(), color=ft.Colors.random())
        print(package.complex_data["hello"])
        package.update()

    package = get_random()

    page.add(
        ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.PURPLE_200,
            content=ft.Column([package], expand=True),
        ),
        ft.Button("Go!", on_click=click),
        ft.Button("Go!", on_click=lambda e: print(package.play(" hello"))),
        ft.Button("Go!", on_click=lambda e: print(package.stop(" bye bye"))),
    )


ft.app(main)
