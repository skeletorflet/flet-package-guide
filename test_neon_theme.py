import flet as ft
import math
from flet_confetti import FletConfetti, BlastDirectionality, ParticleShape, ConfettiTheme


def main(page: ft.Page):
    page.title = "Test NEON Theme Fix"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900

    # Test confetti with NEON theme (this was causing the issue)
    confetti_neon = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=math.pi / 2,  # Down
        particle_shape=ParticleShape.STAR,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=0.3,
        theme=ConfettiTheme.NEON,  # This should work now
    )

    # Test confetti with explicit colors (should override theme)
    confetti_explicit = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=-math.pi / 2,  # Up
        colors=["red", "blue", "green"],  # Explicit colors
        theme=ConfettiTheme.NEON,  # This should be ignored
        particle_shape=ParticleShape.HEART,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=-0.3,
    )

    # Status text
    status_text = ft.Text(
        "🎊 Ready to test NEON theme! 🎊",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    def test_neon_theme(_):
        """Test NEON theme confetti"""
        try:
            confetti_neon.play()
            status_text.value = "🌈 NEON theme confetti playing!"
            print("NEON theme test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ NEON theme error: {e}"
            print(f"NEON theme test: FAILED - {e}")
        page.update()

    def test_explicit_colors(_):
        """Test explicit colors (should override theme)"""
        try:
            confetti_explicit.play()
            status_text.value = "🎨 Explicit colors confetti playing!"
            print("Explicit colors test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ Explicit colors error: {e}"
            print(f"Explicit colors test: FAILED - {e}")
        page.update()

    def stop_all(_):
        """Stop all confetti"""
        try:
            confetti_neon.stop(clear_all_particles=True)
            confetti_explicit.stop(clear_all_particles=True)
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
                            "🧪 NEON Theme Fix Test",
                            size=24,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        status_text,
                        ft.Divider(color=ft.Colors.WHITE24, height=40),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "🌈 Test NEON Theme",
                                on_click=test_neon_theme,
                                bgcolor=ft.Colors.PURPLE_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(20, 15, 20, 15),
                                ),
                            ),
                            ft.ElevatedButton(
                                "🎨 Test Explicit Colors",
                                on_click=test_explicit_colors,
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(20, 15, 20, 15),
                                ),
                            ),
                            ft.ElevatedButton(
                                "🛑 Stop All",
                                on_click=stop_all,
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(20, 15, 20, 15),
                                ),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.Text(
                            "💡 The NEON theme should work without errors now!",
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
                confetti_neon,
                confetti_explicit,
            ],
            alignment=ft.alignment.center,
        )
    )


if __name__ == "__main__":
    ft.app(main)
