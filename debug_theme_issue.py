import flet as ft
import math
from flet_confetti import FletConfetti, BlastDirectionality, ParticleShape, ConfettiTheme


def main(page: ft.Page):
    page.title = "Debug Theme Issue"
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
        color_source=["red", "blue", "green"],
    )

    # Test 2: NEON theme (the problematic one)
    confetti_neon = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=-math.pi / 2,
        particle_shape=ParticleShape.HEART,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=-0.3,
        color_source=ConfettiTheme.NEON,
    )

    # Test 3: Using old API (backward compatibility)
    confetti_old = FletConfetti(
        blast_directionality=BlastDirectionality.EXPLOSIVE,
        particle_shape=ParticleShape.DIAMOND,
        duration_seconds=3,
        number_of_particles=20,
        max_blast_force=40,
        min_blast_force=20,
        gravity=0.2,
    )
    confetti_old.theme = ConfettiTheme.RAINBOW  # Old way

    status_text = ft.Text(
        "🔍 Debug Theme Issue",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    def test_colors(_):
        try:
            print("Testing explicit colors...")
            confetti_colors.play()
            status_text.value = "✅ Explicit colors working!"
        except Exception as e:
            status_text.value = f"❌ Colors error: {e}"
            print(f"Colors error: {e}")
        page.update()

    def test_neon(_):
        try:
            print("Testing NEON theme...")
            print(f"confetti_neon.color_source = {confetti_neon.color_source}")
            print(f"confetti_neon.theme = {confetti_neon.theme}")
            print(f"confetti_neon.colors = {confetti_neon.colors}")
            confetti_neon.play()
            status_text.value = "✅ NEON theme working!"
        except Exception as e:
            status_text.value = f"❌ NEON error: {e}"
            print(f"NEON error: {e}")
        page.update()

    def test_old_api(_):
        try:
            print("Testing old API...")
            print(f"confetti_old.color_source = {confetti_old.color_source}")
            print(f"confetti_old.theme = {confetti_old.theme}")
            confetti_old.play()
            status_text.value = "✅ Old API working!"
        except Exception as e:
            status_text.value = f"❌ Old API error: {e}"
            print(f"Old API error: {e}")
        page.update()

    def debug_attributes(_):
        print("\n=== DEBUG ATTRIBUTES ===")
        print(f"confetti_neon._get_attr('colors'): {confetti_neon._get_attr('colors')}")
        print(f"confetti_neon._get_attr('theme'): {confetti_neon._get_attr('theme')}")
        print(f"confetti_neon.color_source: {confetti_neon.color_source}")
        print(f"confetti_neon.color_source type: {type(confetti_neon.color_source)}")
        
        print(f"\nconfetti_colors._get_attr('colors'): {confetti_colors._get_attr('colors')}")
        print(f"confetti_colors._get_attr('theme'): {confetti_colors._get_attr('theme')}")
        print(f"confetti_colors.color_source: {confetti_colors.color_source}")
        print("=== END DEBUG ===\n")
        
        status_text.value = "🔍 Debug info printed to console"
        page.update()

    def stop_all(_):
        try:
            confetti_colors.stop(clear_all_particles=True)
            confetti_neon.stop(clear_all_particles=True)
            confetti_old.stop(clear_all_particles=True)
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
                            "🔍 Debug Theme Issue",
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
                                "🔄 Test Old API",
                                on_click=test_old_api,
                                bgcolor=ft.Colors.ORANGE_600,
                                color=ft.Colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                "🔍 Debug Attrs",
                                on_click=debug_attributes,
                                bgcolor=ft.Colors.TEAL_600,
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
                confetti_old,
            ],
            alignment=ft.alignment.center,
        )
    )


if __name__ == "__main__":
    ft.app(main)
