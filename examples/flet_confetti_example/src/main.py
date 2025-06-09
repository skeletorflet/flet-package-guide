import flet as ft
import math
import random
from flet_confetti import (
    FletConfetti,
    BlastDirectionality,
    ParticleShape,
    ConfettiTheme,
)


def main(page: ft.Page):
    page.title = "Flet Confetti - Visual Properties & Directional Demo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900

    # Create main confetti (center - debug mode)
    confetti_center = FletConfetti(
        blast_directionality=BlastDirectionality.EXPLOSIVE,
        colors=["red", "blue", "green", "orange", "purple"],  # Explicit colors
        particle_shape=ParticleShape.HEART,
        duration_seconds=5,
        number_of_particles=10,
        should_loop=False,
        max_blast_force=40,
        min_blast_force=20,
        gravity=0.4,
    )

    # Create directional confettis
    confetti_top = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=math.pi / 2,  # Down
        theme=ConfettiTheme.FOREST,  # Using theme - this should work now!
        # STAR,
        custom_particle_path="M10,1 L12,7 L19,7 L14,11 L16,18 L10,14 L4,18 L6,11 L1,7 L8,7 Z",
        duration_seconds=3,
        number_of_particles=15,
        minimum_size=ft.Size(50, 50),
        maximum_size=ft.Size(50, 50),
        max_blast_force=30,
        min_blast_force=15,
        gravity=0.3,
        top=0,
    )

    confetti_bottom = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=-math.pi / 2,  # Up
        colors=["blue", "cyan", "teal"],  # Explicit colors
        particle_shape=ParticleShape.TRIANGLE,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        gravity=-0.3,  # Negative gravity for upward
        bottom=0,
    )

    confetti_left = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=0,  # Right
        colors=["green", "lime", "emerald"],  # Explicit colors
        particle_shape=ParticleShape.DIAMOND,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        left=0,
        gravity=0.2,
    )

    confetti_right = FletConfetti(
        blast_directionality=BlastDirectionality.DIRECTIONAL,
        blast_direction=math.pi,  # Left
        colors=["purple", "magenta", "pink"],  # Explicit colors
        particle_shape=ParticleShape.FLOWER,
        duration_seconds=3,
        number_of_particles=15,
        max_blast_force=30,
        min_blast_force=15,
        right=0,
        gravity=0.2,
    )

    # Create property display texts that will update in real-time
    prop_shape = ft.Text(
        "Shape: heart", size=12, color=ft.Colors.YELLOW, weight=ft.FontWeight.W_500
    )
    prop_directionality = ft.Text(
        "Directionality: explosive",
        size=12,
        color=ft.Colors.CYAN,
        weight=ft.FontWeight.W_500,
    )
    prop_direction = ft.Text(
        "Direction: 0.00", size=12, color=ft.Colors.GREEN, weight=ft.FontWeight.W_500
    )
    prop_particles = ft.Text(
        "Particles: 10", size=12, color=ft.Colors.ORANGE, weight=ft.FontWeight.W_500
    )
    prop_max_force = ft.Text(
        "Max Force: 40.0", size=12, color=ft.Colors.RED, weight=ft.FontWeight.W_500
    )
    prop_min_force = ft.Text(
        "Min Force: 20.0", size=12, color=ft.Colors.PINK, weight=ft.FontWeight.W_500
    )
    prop_gravity = ft.Text(
        "Gravity: 0.40", size=12, color=ft.Colors.PURPLE, weight=ft.FontWeight.W_500
    )
    prop_emission = ft.Text(
        "Emission: 0.050", size=12, color=ft.Colors.BLUE, weight=ft.FontWeight.W_500
    )
    prop_duration = ft.Text(
        "Duration: 5s", size=12, color=ft.Colors.LIME, weight=ft.FontWeight.W_500
    )
    prop_colors = ft.Text(
        "Colors: 5 colors", size=12, color=ft.Colors.AMBER, weight=ft.FontWeight.W_500
    )

    # Function to update all property displays
    def update_properties():
        prop_shape.value = f"Shape: {confetti_center.particle_shape.value if confetti_center.particle_shape else 'None'}"
        prop_directionality.value = (
            f"Directionality: {confetti_center.blast_directionality.value}"
        )
        prop_direction.value = f"Direction: {confetti_center.blast_direction:.2f}"
        prop_particles.value = f"Particles: {confetti_center.number_of_particles}"
        prop_max_force.value = f"Max Force: {confetti_center.max_blast_force:.1f}"
        prop_min_force.value = f"Min Force: {confetti_center.min_blast_force:.1f}"
        prop_gravity.value = f"Gravity: {confetti_center.gravity:.2f}"
        prop_emission.value = f"Emission: {confetti_center.emission_frequency:.3f}"
        prop_duration.value = f"Duration: {confetti_center.duration_seconds}s"
        # Handle color display
        if confetti_center.colors:
            prop_colors.value = f"Colors: {len(confetti_center.colors)} explicit colors"
        elif confetti_center.theme:
            prop_colors.value = f"Colors: {confetti_center.theme.value} theme"
        else:
            prop_colors.value = "Colors: default colors"
        page.update()

    # Status text
    status_text = ft.Text(
        "🎊 Ready to blast confetti! 🎊",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    # Event handlers
    def on_animation_end(_):
        status_text.value = "✨ Animation ended!"
        page.update()

    def randomize_center_confetti():
        """Randomize center confetti properties and update display"""
        # Randomize colors
        confetti_center.colors = [
            ft.Colors.random() for _ in range(random.randint(3, 6))
        ]

        # Randomize shape
        shapes = [shape for shape in ParticleShape if shape.value != "None"]
        confetti_center.particle_shape = random.choice(shapes)

        # Randomize other properties
        if random.random() < 0.5:
            confetti_center.blast_directionality = BlastDirectionality.DIRECTIONAL
        else:
            confetti_center.blast_directionality = BlastDirectionality.EXPLOSIVE

        confetti_center.blast_direction = random.uniform(0, 2 * math.pi)
        confetti_center.max_blast_force = random.uniform(20, 80)
        confetti_center.min_blast_force = random.uniform(10, 40)
        confetti_center.emission_frequency = random.uniform(0.01, 0.09)
        confetti_center.gravity = random.uniform(-0.6, 0.6)
        confetti_center.number_of_particles = random.randint(5, 20)
        confetti_center.minimum_size = ft.Size(10, 10)
        confetti_center.maximum_size = ft.Size(100, 100)

        # Update property display
        update_properties()

    def on_center_play(_):
        """Play center confetti with randomized properties"""
        try:
            randomize_center_confetti()
            confetti_center.reload()
            result = confetti_center.play()
            status_text.value = (
                f"🎊 Center: {confetti_center.particle_shape.value} confetti!"
            )
            print(f"Center confetti: {result}")
        except Exception as e:
            status_text.value = f"❌ Center error: {e}"
        page.update()

    def on_top_play(_):
        """Play top confetti"""
        try:
            confetti_top.play()
            status_text.value = "⬇️ Top confetti blasting down!"
        except Exception as e:
            status_text.value = f"❌ Top error: {e}"
        page.update()

    def on_bottom_play(_):
        """Play bottom confetti"""
        try:
            confetti_bottom.play()
            status_text.value = "⬆️ Bottom confetti blasting up!"
        except Exception as e:
            status_text.value = f"❌ Bottom error: {e}"
        page.update()

    def on_left_play(_):
        """Play left confetti"""
        try:
            confetti_left.play()
            status_text.value = "➡️ Left confetti blasting right!"
        except Exception as e:
            status_text.value = f"❌ Left error: {e}"
        page.update()

    def on_right_play(_):
        """Play right confetti"""
        try:
            confetti_right.play()
            status_text.value = "⬅️ Right confetti blasting left!"
        except Exception as e:
            status_text.value = f"❌ Right error: {e}"
        page.update()

    def stop_all(_):
        """Stop all confetti"""
        try:
            confetti_center.stop(clear_all_particles=True)
            confetti_top.stop(clear_all_particles=True)
            confetti_bottom.stop(clear_all_particles=True)
            confetti_left.stop(clear_all_particles=True)
            confetti_right.stop(clear_all_particles=True)
            status_text.value = "🛑 All confetti stopped!"
        except Exception as e:
            status_text.value = f"❌ Stop error: {e}"
        page.update()

    # Set event handlers
    confetti_center.on_animation_end = on_animation_end

    # Initialize property display
    update_properties()

    # Create the main layout using Column and Row structure
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                # Main layout structure
                ft.Column(
                    [
                        # Top row with top button
                        ft.Container(
                            content=ft.ElevatedButton(
                                "⬇️ TOP",
                                on_click=on_top_play,
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.Padding(20, 10, 20, 10),
                                ),
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.Padding(0, 10, 0, 5),
                        ),
                        # Middle row with left, center, right
                        ft.Row(
                            [
                                # Left button
                                ft.ElevatedButton(
                                    "➡️\nLEFT",
                                    on_click=on_left_play,
                                    bgcolor=ft.Colors.GREEN_400,
                                    color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.Padding(10, 30, 10, 30),
                                    ),
                                ),
                                # Center debug area
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "🎊 CONFETTI DEBUG CENTER 🎊",
                                                size=18,
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                            status_text,
                                            ft.Divider(
                                                color=ft.Colors.WHITE24, height=20
                                            ),
                                            # Properties display in a grid
                                            ft.Column(
                                                [
                                                    ft.Row(
                                                        [
                                                            prop_shape,
                                                            prop_directionality,
                                                        ],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        spacing=20,
                                                    ),
                                                    ft.Row(
                                                        [
                                                            prop_direction,
                                                            prop_particles,
                                                        ],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        spacing=20,
                                                    ),
                                                    ft.Row(
                                                        [
                                                            prop_max_force,
                                                            prop_min_force,
                                                        ],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        spacing=20,
                                                    ),
                                                    ft.Row(
                                                        [prop_gravity, prop_emission],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        spacing=20,
                                                    ),
                                                    ft.Row(
                                                        [prop_duration, prop_colors],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        spacing=20,
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Divider(
                                                color=ft.Colors.WHITE24, height=20
                                            ),
                                            # Center control buttons
                                            ft.Row(
                                                [
                                                    ft.ElevatedButton(
                                                        "🎉 PLAY CENTER",
                                                        on_click=on_center_play,
                                                        bgcolor=ft.Colors.ORANGE_600,
                                                        color=ft.Colors.WHITE,
                                                        style=ft.ButtonStyle(
                                                            padding=ft.Padding(
                                                                15, 8, 15, 8
                                                            ),
                                                        ),
                                                    ),
                                                    ft.ElevatedButton(
                                                        "🛑 STOP ALL",
                                                        on_click=stop_all,
                                                        bgcolor=ft.Colors.RED_600,
                                                        color=ft.Colors.WHITE,
                                                        style=ft.ButtonStyle(
                                                            padding=ft.Padding(
                                                                15, 8, 15, 8
                                                            ),
                                                        ),
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                spacing=15,
                                            ),
                                            ft.Text(
                                                "💡 Properties update in real-time!",
                                                size=12,
                                                color=ft.Colors.WHITE70,
                                                text_align=ft.TextAlign.CENTER,
                                                italic=True,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=10,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(
                                        0.8, ft.Colors.BLACK
                                    ),
                                    border_radius=15,
                                    padding=20,
                                    expand=True,
                                ),
                                # Right button
                                ft.ElevatedButton(
                                    "⬅️\nRIGHT",
                                    on_click=on_right_play,
                                    bgcolor=ft.Colors.PURPLE_400,
                                    color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.Padding(10, 30, 10, 30),
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            expand=True,
                            spacing=20,
                        ),
                        # Bottom row with bottom button
                        ft.Container(
                            content=ft.ElevatedButton(
                                "⬆️ BOTTOM",
                                on_click=on_bottom_play,
                                bgcolor=ft.Colors.BLUE_400,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.Padding(20, 10, 20, 10),
                                ),
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.Padding(0, 5, 0, 10),
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),
                # All confetti widgets (positioned for effects)
                confetti_top,
                confetti_bottom,
                confetti_left,
                confetti_right,
                confetti_center,
            ],
            alignment=ft.alignment.center,
        )
    )


if __name__ == "__main__":
    ft.app(main)
