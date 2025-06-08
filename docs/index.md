# Introduction

FletConfetti for Flet.

## Examples

```
import flet as ft

from flet_confetti import FletConfetti


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletConfetti(
                    tooltip="My new FletConfetti Control tooltip",
                    value = "My new FletConfetti Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletConfetti](FletConfetti.md)


