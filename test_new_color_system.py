import flet as ft
import math
from flet_confetti import FletConfetti, BlastDirectionality, ParticleShape, ConfettiTheme


def main(page: ft.Page):
    page.title = "New Color System Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900

    # Test 1: Using explicit colors with new system
    confetti_explicit = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=math.pi / 2,  # Down
        particle_shape=ParticleShape.STAR,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=0.3,
        color_source=["red", "blue", "green", "yellow", "purple"],  # NEW WAY
    )

    # Test 2: Using theme with new system
    confetti_theme = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=-math.pi / 2,  # Up
        particle_shape=ParticleShape.HEART,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=-0.3,
        color_source=ConfettiTheme.NEON,  # NEW WAY
    )

    # Test 3: Using default colors (None)
    confetti_default = FletConfetti(
        blast_directionality=BlastDirectionality.EXPLOSIVE,
        particle_shape=ParticleShape.DIAMOND,
        duration_seconds=3,
        number_of_particles=20,
        max_blast_force=40,
        min_blast_force=20,
        gravity=0.2,
        color_source=None,  # NEW WAY - explicit default
    )

    # Test 4: Backward compatibility - using old properties
    confetti_backward = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=0,  # Right
        particle_shape=ParticleShape.FLOWER,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=0.2,
    )
    # Set using old properties (should still work)
    confetti_backward.theme = ConfettiTheme.RAINBOW

    # Status text
    status_text = ft.Text(
        "🎊 Ready to test new color system! 🎊",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    def test_explicit_colors(_):
        """Test explicit colors"""
        try:
            confetti_explicit.play()
            status_text.value = "🎨 Explicit colors: red, blue, green, yellow, purple!"
            print("Explicit colors test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ Explicit colors error: {e}"
            print(f"Explicit colors test: FAILED - {e}")
        page.update()

    def test_theme(_):
        """Test NEON theme"""
        try:
            confetti_theme.play()
            status_text.value = "🌈 NEON theme confetti!"
            print("NEON theme test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ NEON theme error: {e}"
            print(f"NEON theme test: FAILED - {e}")
        page.update()

    def test_default(_):
        """Test default colors"""
        try:
            confetti_default.play()
            status_text.value = "⭐ Default colors confetti!"
            print("Default colors test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ Default colors error: {e}"
            print(f"Default colors test: FAILED - {e}")
        page.update()

    def test_backward_compatibility(_):
        """Test backward compatibility"""
        try:
            confetti_backward.play()
            status_text.value = "🔄 Backward compatibility: RAINBOW theme!"
            print("Backward compatibility test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ Backward compatibility error: {e}"
            print(f"Backward compatibility test: FAILED - {e}")
        page.update()

    def test_dynamic_change(_):
        """Test dynamic color source change"""
        try:
            # Change from explicit colors to theme
            confetti_explicit.color_source = ConfettiTheme.CHRISTMAS
            confetti_explicit.play()
            status_text.value = "🎄 Dynamic change: Explicit → CHRISTMAS theme!"
            print("Dynamic change test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ Dynamic change error: {e}"
            print(f"Dynamic change test: FAILED - {e}")
        page.update()

    def stop_all(_):
        """Stop all confetti"""
        try:
            confetti_explicit.stop(clear_all_particles=True)
            confetti_theme.stop(clear_all_particles=True)
            confetti_default.stop(clear_all_particles=True)
            confetti_backward.stop(clear_all_particles=True)
            status_text.value = "🛑 All confetti stopped!"
        except Exception as e:
            status_text.value = f"❌ Stop error: {e}"
        page.update()

    # Create the layout
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            "🧪 New Color System Test",
                            size=24,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        status_text,
                        ft.Divider(color=ft.Colors.WHITE24, height=40),
                        
                        # Test buttons in a grid
                        ft.Row([
                            ft.ElevatedButton(
                                "🎨 Explicit Colors",
                                on_click=test_explicit_colors,
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.Padding(15, 10, 15, 10)),
                            ),
                            ft.ElevatedButton(
                                "🌈 NEON Theme",
                                on_click=test_theme,
                                bgcolor=ft.Colors.PURPLE_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.Padding(15, 10, 15, 10)),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "⭐ Default Colors",
                                on_click=test_default,
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.Padding(15, 10, 15, 10)),
                            ),
                            ft.ElevatedButton(
                                "🔄 Backward Compat",
                                on_click=test_backward_compatibility,
                                bgcolor=ft.Colors.ORANGE_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.Padding(15, 10, 15, 10)),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "🔄 Dynamic Change",
                                on_click=test_dynamic_change,
                                bgcolor=ft.Colors.TEAL_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.Padding(15, 10, 15, 10)),
                            ),
                            ft.ElevatedButton(
                                "🛑 Stop All",
                                on_click=stop_all,
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.Padding(15, 10, 15, 10)),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.Text(
                            "💡 New unified color system with Union types!",
                            size=14,
                            color=ft.Colors.WHITE70,
                            text_align=ft.TextAlign.CENTER,
                            italic=True,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                
                # Confetti widgets
                confetti_explicit,
                confetti_theme,
                confetti_default,
                confetti_backward,
            ],
            alignment=ft.alignment.center,
        )
    )


if __name__ == "__main__":
    ft.app(main)
