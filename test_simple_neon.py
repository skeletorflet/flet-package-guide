import flet as ft
import math
from flet_confetti import FletConfetti, BlastDirectionality, ParticleShape, ConfettiTheme


def main(page: ft.Page):
    page.title = "Simple NEON Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900

    # Simple NEON theme test with new system
    confetti = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=math.pi / 2,  # Down
        particle_shape=ParticleShape.STAR,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=0.3,
        color_source=ConfettiTheme.NEON,  # This should work now!
    )

    status_text = ft.Text(
        "🎊 Ready to test NEON theme! 🎊",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    def test_neon(_):
        try:
            confetti.play()
            status_text.value = "🌈 NEON theme working perfectly!"
            print("NEON theme test: SUCCESS")
        except Exception as e:
            status_text.value = f"❌ Error: {e}"
            print(f"NEON theme test: FAILED - {e}")
        page.update()

    def stop_confetti(_):
        try:
            confetti.stop(clear_all_particles=True)
            status_text.value = "🛑 Confetti stopped!"
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
                            "🧪 Simple NEON Test",
                            size=24,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        status_text,
                        ft.Divider(color=ft.Colors.WHITE24, height=40),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "🌈 Test NEON",
                                on_click=test_neon,
                                bgcolor=ft.Colors.PURPLE_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(20, 15, 20, 15),
                                ),
                            ),
                            ft.ElevatedButton(
                                "🛑 Stop",
                                on_click=stop_confetti,
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(20, 15, 20, 15),
                                ),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        
                        ft.Text(
                            "💡 Using new unified color_source system!",
                            size=14,
                            color=ft.Colors.WHITE70,
                            text_align=ft.TextAlign.CENTER,
                            italic=True,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                
                confetti,
            ],
            alignment=ft.alignment.center,
        )
    )


if __name__ == "__main__":
    ft.app(main)
