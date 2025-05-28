# Introduction

FletPackageGuide for Flet.

## Examples

```
import flet as ft

from flet_package_guide import FletPackageGuide


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletPackageGuide(
                    tooltip="My new FletPackageGuide Control tooltip",
                    value = "My new FletPackageGuide Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletPackageGuide](FletPackageGuide.md)


