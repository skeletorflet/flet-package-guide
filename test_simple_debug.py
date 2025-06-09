import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import flet as ft
from flet_confetti import FletConfetti, ConfettiTheme

def main(page: ft.Page):
    page.title = "Simple Debug"
    page.bgcolor = ft.Colors.BLACK

    # Test NEON theme
    confetti = FletConfetti(theme=ConfettiTheme.NEON)

    # Debug what's being sent
    print(f"ConfettiTheme.NEON = {ConfettiTheme.NEON}")
    print(f"ConfettiTheme.NEON.value = {ConfettiTheme.NEON.value}")
    print(f"confetti.theme = {confetti.theme}")
    print(f"confetti._get_attr('theme') = {confetti._get_attr('theme')}")
    print(f"confetti._get_attr('colors') = {confetti._get_attr('colors')}")

    # Test explicit colors too
    confetti2 = FletConfetti(colors=["red", "blue"])
    print(f"confetti2._get_attr('colors') = {confetti2._get_attr('colors')}")
    print(f"confetti2._get_attr('theme') = {confetti2._get_attr('theme')}")

    def test_play(_):
        print("Playing NEON confetti...")
        confetti.play()

    def test_play2(_):
        print("Playing colors confetti...")
        confetti2.play()

    page.add(
        ft.Column([
            ft.ElevatedButton("Play NEON", on_click=test_play),
            ft.ElevatedButton("Play Colors", on_click=test_play2),
            confetti,
            confetti2
        ])
    )

if __name__ == "__main__":
    ft.app(main)
