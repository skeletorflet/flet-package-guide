import flet as ft
import math
from flet_confetti import FletConfetti, BlastDirectionality

def main(page: ft.Page):
    page.title = "Flet Confetti Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.colors.GREY_900
    
    # Create different confetti controls with various configurations
    
    # Center blast with stars
    confetti_center = FletConfetti(
        emission_frequency=0.02,
        number_of_particles=50,
        blast_directionality=BlastDirectionality.EXPLOSIVE,
        should_loop=False,
        colors=["green", "blue", "pink", "orange", "purple"],
        create_particle_path="star",
        width=200,
        height=200,
    )
    
    # Right side - emit left
    confetti_right = FletConfetti(
        blast_direction=math.pi,  # LEFT
        particle_drag=0.05,
        emission_frequency=0.05,
        number_of_particles=20,
        gravity=0.05,
        should_loop=False,
        colors=["green", "blue", "pink"],
        stroke_width=1,
        stroke_color="white",
        width=200,
        height=200,
    )
    
    # Left side - emit right
    confetti_left = FletConfetti(
        blast_direction=0,  # RIGHT
        emission_frequency=0.6,
        minimum_size_width=10,
        minimum_size_height=10,
        maximum_size_width=50,
        maximum_size_height=50,
        number_of_particles=1,
        gravity=0.1,
        width=200,
        height=200,
    )
    
    # Top center - shoot down
    confetti_top = FletConfetti(
        blast_direction=math.pi / 2,
        max_blast_force=5,
        min_blast_force=2,
        emission_frequency=0.05,
        number_of_particles=50,
        gravity=1,
        width=200,
        height=200,
    )
    
    # Bottom center - shoot up
    confetti_bottom = FletConfetti(
        blast_direction=-math.pi / 2,
        emission_frequency=0.01,
        number_of_particles=20,
        max_blast_force=100,
        min_blast_force=80,
        gravity=0.3,
        width=200,
        height=200,
    )
    
    def on_animation_end(e):
        print(f"Animation ended for control: {e.control}")
    
    # Set event handlers
    confetti_center.on_animation_end = on_animation_end
    confetti_right.on_animation_end = on_animation_end
    confetti_left.on_animation_end = on_animation_end
    confetti_top.on_animation_end = on_animation_end
    confetti_bottom.on_animation_end = on_animation_end
    
    # Create buttons to trigger confetti
    def play_center(e):
        confetti_center.play()
    
    def play_right(e):
        confetti_right.play()
    
    def play_left(e):
        confetti_left.play()
    
    def play_top(e):
        confetti_top.play()
    
    def play_bottom(e):
        confetti_bottom.play()
    
    def stop_all(e):
        confetti_center.stop()
        confetti_right.stop()
        confetti_left.stop()
        confetti_top.stop()
        confetti_bottom.stop()
    
    # Layout
    page.add(
        ft.Column([
            ft.Text(
                "Flet Confetti Demo",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(color=ft.colors.WHITE24),
            
            # Top row
            ft.Row([
                ft.Container(width=100),
                ft.Stack([
                    confetti_top,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Goliath",
                            on_click=play_top,
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ], width=200, height=200),
                ft.Container(width=100),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            # Middle row
            ft.Row([
                ft.Stack([
                    confetti_left,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Singles",
                            on_click=play_left,
                            bgcolor=ft.colors.GREEN,
                            color=ft.colors.WHITE,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ], width=200, height=200),
                
                ft.Stack([
                    confetti_center,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Blast\nStars",
                            on_click=play_center,
                            bgcolor=ft.colors.PURPLE,
                            color=ft.colors.WHITE,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ], width=200, height=200),
                
                ft.Stack([
                    confetti_right,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Pump Left",
                            on_click=play_right,
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ], width=200, height=200),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            # Bottom row
            ft.Row([
                ft.Container(width=100),
                ft.Stack([
                    confetti_bottom,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Hard and\nInfrequent",
                            on_click=play_bottom,
                            bgcolor=ft.colors.RED,
                            color=ft.colors.WHITE,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ], width=200, height=200),
                ft.Container(width=100),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Divider(color=ft.colors.WHITE24),
            
            # Control buttons
            ft.Row([
                ft.ElevatedButton(
                    "Stop All",
                    on_click=stop_all,
                    bgcolor=ft.colors.RED_400,
                    color=ft.colors.WHITE,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Text(
                "Click the buttons to trigger different confetti animations!",
                color=ft.colors.WHITE70,
                text_align=ft.TextAlign.CENTER,
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        )
    )

ft.app(main)
