import flet as ft
import math
from flet_confetti import FletConfetti, BlastDirectionality, ParticleShape, ConfettiTheme


def main(page: ft.Page):
    page.title = "Final Test - Fixed Theme Issue"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900

    # Test 1: Explicit colors (should work)
    confetti_colors = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=math.pi / 2,
        particle_shape=ParticleShape.STAR,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=0.3,
        colors=["red", "blue", "green"],  # Simple approach
    )

    # Test 2: NEON theme (the problematic one - should work now)
    confetti_neon = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=-math.pi / 2,
        particle_shape=ParticleShape.HEART,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=-0.3,
        theme=ConfettiTheme.NEON,  # Simple approach
    )

    # Test 3: Default colors
    confetti_default = FletConfetti(
        blast_directionality=BlastDirectionality.EXPLOSIVE,
        particle_shape=ParticleShape.DIAMOND,
        duration_seconds=3,
        number_of_particles=20,
        max_blast_force=40,
        min_blast_force=20,
        gravity=0.2,
        # No colors or theme - should use defaults
    )

    status_text = ft.Text(
        "🔧 Final Test - Fixed Theme Issue",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    def test_colors(_):
        try:
            print("Testing explicit colors...")
            print(f"confetti_colors.colors = {confetti_colors.colors}")
            print(f"confetti_colors.theme = {confetti_colors.theme}")
            confetti_colors.play()
            status_text.value = "✅ Explicit colors working!"
        except Exception as e:
            status_text.value = f"❌ Colors error: {e}"
            print(f"Colors error: {e}")
        page.update()

    def test_neon(_):
        try:
            print("Testing NEON theme...")
            print(f"confetti_neon.colors = {confetti_neon.colors}")
            print(f"confetti_neon.theme = {confetti_neon.theme}")
            print(f"confetti_neon._get_attr('colors') = {confetti_neon._get_attr('colors')}")
            print(f"confetti_neon._get_attr('theme') = {confetti_neon._get_attr('theme')}")
            confetti_neon.play()
            status_text.value = "✅ NEON theme working!"
        except Exception as e:
            status_text.value = f"❌ NEON error: {e}"
            print(f"NEON error: {e}")
        page.update()

    def test_default(_):
        try:
            print("Testing default colors...")
            print(f"confetti_default.colors = {confetti_default.colors}")
            print(f"confetti_default.theme = {confetti_default.theme}")
            confetti_default.play()
            status_text.value = "✅ Default colors working!"
        except Exception as e:
            status_text.value = f"❌ Default error: {e}"
            print(f"Default error: {e}")
        page.update()

    def test_dynamic_change(_):
        try:
            print("Testing dynamic theme change...")
            # Change from colors to theme
            confetti_colors.theme = ConfettiTheme.RAINBOW
            confetti_colors.colors = None  # Clear colors
            print(f"After change - colors: {confetti_colors.colors}, theme: {confetti_colors.theme}")
            confetti_colors.play()
            status_text.value = "✅ Dynamic change working!"
        except Exception as e:
            status_text.value = f"❌ Dynamic error: {e}"
            print(f"Dynamic error: {e}")
        page.update()

    def stop_all(_):
        try:
            confetti_colors.stop(clear_all_particles=True)
            confetti_neon.stop(clear_all_particles=True)
            confetti_default.stop(clear_all_particles=True)
            status_text.value = "🛑 All stopped!"
        except Exception as e:
            status_text.value = f"❌ Stop error: {e}"
        page.update()

    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "🔧 Final Test - Fixed Theme Issue",
                            size=24,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        status_text,
                        ft.Divider(color=ft.Colors.WHITE24, height=40),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "🎨 Test Colors",
                                on_click=test_colors,
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                "🌈 Test NEON",
                                on_click=test_neon,
                                bgcolor=ft.Colors.PURPLE_600,
                                color=ft.Colors.WHITE,
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "⭐ Test Default",
                                on_click=test_default,
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                "🔄 Dynamic Change",
                                on_click=test_dynamic_change,
                                bgcolor=ft.Colors.ORANGE_600,
                                color=ft.Colors.WHITE,
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.ElevatedButton(
                            "🛑 Stop All",
                            on_click=stop_all,
                            bgcolor=ft.Colors.RED_600,
                            color=ft.Colors.WHITE,
                        ),
                        
                        ft.Text(
                            "Check console for debug output",
                            size=12,
                            color=ft.Colors.WHITE70,
                            text_align=ft.TextAlign.CENTER,
                            italic=True,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                
                confetti_colors,
                confetti_neon,
                confetti_default,
            ],
            alignment=ft.alignment.center,
        )
    )


if __name__ == "__main__":
    ft.app(main)
