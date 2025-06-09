from enum import Enum
from typing import Any, Optional, List, Union
from flet.core.colors import Colors
from flet.core.size import Size
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
)
import math

class BlastDirectionality(Enum):
    """
    Enumeration of confetti emission patterns.

    Defines how particles are distributed when emitted from the confetti source.
    Each pattern creates a different visual effect suitable for various scenarios.
    The emission pattern significantly affects the overall appearance and feel
    of the confetti animation.
    """

    DIRECTIONAL = "directional"
    """
    Particles emit in a specific direction with controlled spread.

    Creates focused, directional effects where particles follow a primary
    trajectory with natural variation. The emission direction is controlled
    by the `blast_direction` property.

    Perfect for:
    - Confetti cannons and launchers
    - Directional celebrations (upward, downward, sideways)
    - Simulating wind or gravity effects
    - Targeted particle streams
    - Realistic physics-based animations

    Use with `blast_direction` to control the emission angle:
    - 0 or 2π: Rightward
    - π/2: Downward
    - π: Leftward
    - 3π/2: Upward
    """

    EXPLOSIVE = "explosive"
    """
    Particles emit in all directions from the center point.

    Creates spectacular burst effects where particles radiate outward
    in a 360-degree pattern from the emission source. The `blast_direction`
    property has no effect in this mode.

    Perfect for:
    - Firework-style bursts and explosions
    - Celebration climax moments
    - Central focal point effects
    - Birthday surprises and achievements
    - Dramatic reveal animations

    Creates maximum visual impact with particles spreading in all
    directions simultaneously.
    """


class ConfettiTheme(Enum):
    """
    Predefined color themes for confetti animations.
    Themes are converted to color lists in Python and sent as colors to Dart.
    """

    # App themes
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"

    # Festive themes
    CHRISTMAS = "christmas"
    HALLOWEEN = "halloween"
    VALENTINE = "valentine"
    EASTER = "easter"
    NEW_YEAR = "new_year"

    # Seasonal themes
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

    # Nature themes
    FOREST = "forest"
    OCEAN = "ocean"
    SUNSET = "sunset"
    RAINBOW = "rainbow"

    # Party themes
    BIRTHDAY = "birthday"
    WEDDING = "wedding"
    GRADUATION = "graduation"

    # Style themes
    NEON = "neon"
    PASTEL = "pastel"
    GOLD = "gold"
    SILVER = "silver"
    MONOCHROME = "monochrome"


# Theme color definitions in Python
THEME_COLORS = {
    # App Colors Primary, Secondary, Tertiary
    "primary": [
        Colors.PRIMARY,
        Colors.ON_PRIMARY,
        Colors.PRIMARY_CONTAINER,
        Colors.ON_PRIMARY_CONTAINER,
    ],
    "secondary": [
        Colors.SECONDARY,
        Colors.ON_SECONDARY,
        Colors.SECONDARY_CONTAINER,
        Colors.ON_SECONDARY_CONTAINER,
    ],
    "tertiary": [
        Colors.TERTIARY,
        Colors.ON_TERTIARY,
        Colors.TERTIARY_CONTAINER,
        Colors.ON_TERTIARY_CONTAINER,
    ],
    # Festive themes
    "christmas": ["#FF0000", "#00FF00", "#FFD700", "#FFFFFF", "#8B0000", "#006400"],
    "halloween": ["#FF8C00", "#000000", "#800080", "#228B22", "#FF4500"],
    "valentine": ["#FF69B4", "#FF0000", "#FFFFFF", "#FFB6C1", "#DC143C"],
    "easter": ["#FFB6C1", "#FFFF00", "#90EE90", "#87CEEB", "#DDA0DD"],
    "new_year": ["#FFD700", "#C0C0C0", "#000000", "#FFFFFF", "#FFA500"],
    # Seasonal themes
    "spring": ["#90EE90", "#87CEEB", "#FFFF00", "#FFB6C1", "#98FB98"],
    "summer": ["#00BFFF", "#FFFF00", "#FF8C00", "#FF0000", "#32CD32"],
    "autumn": ["#FF8C00", "#FF0000", "#8B4513", "#FFFF00", "#DAA520"],
    "winter": ["#87CEEB", "#FFFFFF", "#C0C0C0", "#4682B4", "#B0E0E6"],
    # Nature themes
    "forest": ["#228B22", "#006400", "#32CD32", "#8FBC8F", "#556B2F"],
    "ocean": ["#0000FF", "#008B8B", "#00CED1", "#FFFFFF", "#4682B4"],
    "sunset": ["#FF8C00", "#FF69B4", "#800080", "#FFFF00", "#FF4500"],
    "rainbow": ["#FF0000", "#FF8C00", "#FFFF00", "#00FF00", "#0000FF", "#800080"],
    # Party themes
    "birthday": ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"],
    "wedding": ["#FFFFFF", "#F5F5DC", "#FFB6C1", "#FFD700", "#FFFACD"],
    "graduation": ["#0000FF", "#FFD700", "#FFFFFF", "#000080", "#C0C0C0"],
    # Style themes
    "neon": ["#FF073A", "#39FF14", "#00FFFF", "#FF00FF", "#FFFF00"],
    "pastel": ["#FFB6C1", "#87CEEB", "#98FB98", "#F0E68C", "#DDA0DD"],
    "gold": ["#FFD700", "#FFA500", "#FFFF00", "#DAA520", "#B8860B"],
    "silver": ["#C0C0C0", "#808080", "#DCDCDC", "#A9A9A9", "#D3D3D3"],
    "monochrome": ["#000000", "#FFFFFF", "#808080", "#C0C0C0", "#696969"],
}


class ParticleShape(Enum):
    """
    Enumeration of available confetti particle shapes.

    Defines the visual appearance of individual particles in the animation.
    Each shape is optimized for performance while maintaining visual appeal.
    All shapes are rendered as vector paths for crisp appearance at any size.

    Categories:
        - **Basic**: Simple geometric shapes for universal appeal
        - **Geometric**: Complex polygons for modern aesthetics
        - **Stars**: Various star configurations for celebrations
        - **Fun**: Whimsical shapes for special occasions
        - **Symbols**: Iconic shapes with specific meanings
        - **Special**: Unique shapes for themed applications
    """

    # Basic shapes
    RECTANGLE = "rectangle"
    """Default rectangular particles. Classic confetti shape."""

    CIRCLE = "circle"
    """Perfect circles. Smooth and timeless."""

    SQUARE = "square"
    """Square particles. Clean and geometric."""

    # Geometric shapes
    TRIANGLE = "triangle"
    """Triangular particles. Sharp and dynamic."""

    DIAMOND = "diamond"
    """Diamond-shaped particles. Elegant and sophisticated."""

    HEXAGON = "hexagon"
    """Six-sided particles. Modern and structured."""

    PENTAGON = "pentagon"
    """Five-sided particles. Unique geometric appeal."""

    OCTAGON = "octagon"
    """Eight-sided particles. Complex and interesting."""

    # Star variations
    STAR = "star"
    """Classic 5-pointed star. Perfect for achievements and celebrations."""

    STAR_4 = "star_4"
    """4-pointed star. Simple and bold."""

    STAR_6 = "star_6"
    """6-pointed star. Balanced and harmonious."""

    STAR_8 = "star_8"
    """8-pointed star. Complex and radiant."""

    # Fun shapes
    HEART = "heart"
    """Heart-shaped particles. Ideal for romantic themes and love."""

    FLOWER = "flower"
    """Flower-shaped particles. Natural and organic feel."""

    LEAF = "leaf"
    """Leaf-shaped particles. Perfect for nature and eco themes."""

    BUTTERFLY = "butterfly"
    """Butterfly particles. Graceful and whimsical."""

    # Symbols
    CROSS = "cross"
    """Cross-shaped particles. Religious or medical themes."""

    PLUS = "plus"
    """Plus sign particles. Positive and additive themes."""

    ARROW = "arrow"
    """Arrow-shaped particles. Directional and purposeful."""

    LIGHTNING = "lightning"
    """Lightning bolt particles. Energy and power themes."""

    # Special shapes
    SKULL = "skull"
    """Skull-shaped particles. Halloween and edgy themes."""

    CROWN = "crown"
    """Crown particles. Royal and achievement themes."""

    MUSIC_NOTE = "music_note"
    """Musical note particles. Music apps and audio celebrations."""

    SWORD = "sword"
    """Sword particles. Adventure and fantasy themes."""


# Type alias for color source - can be either explicit colors or a theme
ColorSource = Union[List[ColorValue], ConfettiTheme, None]


class FletConfetti(ConstrainedControl):
    """
    A highly customizable confetti animation widget for Flet applications.

    FletConfetti provides beautiful particle-based confetti animations with extensive
    customization options including colors, shapes, physics, and emission patterns.
    Perfect for celebrations, achievements, and adding visual flair to your apps.

    Features:
        - Multiple particle shapes (stars, hearts, circles, etc.)
        - Predefined color themes or custom color palettes
        - Directional and explosive blast patterns
        - Realistic physics with gravity and drag
        - Customizable particle size, speed, and duration
        - Event callbacks for animation lifecycle
        - High performance with optimized rendering

    Color Configuration:
        Colors can be specified in three ways:

        1. **Explicit colors**: Provide a list of color values
           ```python
           confetti = FletConfetti(colors=["red", "blue", "green", "#FF5733"])
           ```

        2. **Predefined themes**: Use built-in color themes
           ```python
           confetti = FletConfetti(theme=ConfettiTheme.NEON)
           ```

        3. **Default colors**: Automatic colorful palette
           ```python
           confetti = FletConfetti()  # Uses default colors
           ```

    Physics and Animation:
        The confetti system simulates realistic particle physics:
        - **Gravity**: Controls how fast particles fall
        - **Blast force**: Initial velocity of particles
        - **Drag**: Air resistance affecting particle movement
        - **Direction**: Controls emission angle and spread

    Examples:
        Basic usage:
        ```python
        import flet as ft
        from flet_confetti import FletConfetti, ConfettiTheme, ParticleShape

        def main(page: ft.Page):
            # Simple confetti with theme
            confetti = FletConfetti(
                theme=ConfettiTheme.CELEBRATION,
                particle_shape=ParticleShape.STAR
            )

            def celebrate(_):
                confetti.play()

            page.add(
                ft.ElevatedButton("Celebrate!", on_click=celebrate),
                confetti
            )

        ft.app(main)
        ```

        Advanced configuration:
        ```python
        from flet.core.size import Size

        confetti = FletConfetti(
            colors=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"],
            particle_shape=ParticleShape.HEART,
            blast_directionality=BlastDirectionality.DIRECTIONAL,
            blast_direction=math.pi / 2,  # Downward
            number_of_particles=25,
            max_blast_force=35,
            gravity=0.4,
            minimum_size=Size(15, 8),     # Small particles
            maximum_size=Size(35, 20),    # Large particles (creates size variation)
            canvas_size=Size(800, 600),   # Fixed canvas size
            duration_seconds=5,
            on_animation_end=lambda _: print("Celebration complete!")
        )

        # Alternative: Use convenience method for size range
        confetti.set_particle_size_range(
            min_size=Size(10, 5),   # Minimum particle size
            max_size=Size(50, 25)   # Maximum particle size
        )
        ```

    Note:
        This widget requires the flet_confetti package to be properly installed
        and configured in your Flet application. The widget automatically handles
        platform-specific rendering optimizations.
    """

    def __init__(
        self,
        #
        # Control
        #
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # ConstrainedControl
        #
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        #
        # FletConfetti specific
        #
        emission_frequency: OptionalNumber = 0.02,
        number_of_particles: Optional[int] = 10,
        max_blast_force: OptionalNumber = 20,
        min_blast_force: OptionalNumber = 5,
        blast_directionality: Optional[
            BlastDirectionality
        ] = BlastDirectionality.DIRECTIONAL,
        blast_direction: OptionalNumber = math.pi,
        gravity: OptionalNumber = 0.2,
        should_loop: Optional[bool] = False,
        display_target: Optional[bool] = False,
        colors: Optional[List[ColorValue]] = None,
        theme: Optional[ConfettiTheme] = None,
        stroke_color: Optional[ColorValue] = "black",
        stroke_width: OptionalNumber = 0,
        minimum_size: Optional[Size] = None,
        maximum_size: Optional[Size] = None,
        particle_drag: OptionalNumber = 0.05,
        canvas_size: Optional[Size] = None,
        pause_emission_on_low_frame_rate: Optional[bool] = True,
        create_particle_path: Optional[
            str
        ] = None,  # Deprecated: use particle_shape instead
        particle_shape: Optional[ParticleShape] = None,
        custom_particle_path: Optional[str] = None,
        duration_seconds: Optional[int] = 10,
        on_animation_end: OptionalControlEventCallable = None,
    ):
        ConstrainedControl.__init__(
            self,
            tooltip=tooltip,
            opacity=opacity,
            visible=visible,
            data=data,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )

        self.emission_frequency = emission_frequency
        self.number_of_particles = number_of_particles
        self.max_blast_force = max_blast_force
        self.min_blast_force = min_blast_force
        self.blast_directionality = blast_directionality
        self.blast_direction = blast_direction
        self.gravity = gravity
        self.should_loop = should_loop
        self.display_target = display_target
        self.colors = colors
        self.theme = theme
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        # Set default sizes if not provided
        self.minimum_size = minimum_size if minimum_size is not None else Size(20, 10)
        self.maximum_size = maximum_size if maximum_size is not None else Size(30, 15)
        self.particle_drag = particle_drag
        self.canvas_size = canvas_size
        self.pause_emission_on_low_frame_rate = pause_emission_on_low_frame_rate
        self.create_particle_path = create_particle_path
        self.particle_shape = particle_shape
        self.custom_particle_path = custom_particle_path
        self.duration_seconds = duration_seconds
        self.on_animation_end = on_animation_end

    def _get_control_name(self):
        return "flet_confetti"

    # emission_frequency
    @property
    def emission_frequency(self) -> OptionalNumber:
        """
        The frequency at which confetti particles are emitted.

        Controls how often new particles are created during the animation.
        Lower values create more particles per second, while higher values
        create fewer particles with more spacing between emissions.

        Returns:
            float: The emission frequency in seconds between particle bursts.
                  Default is 0.02 (50 particles per second).

        Example:
            ```python
            confetti.emission_frequency = 0.01  # Very frequent (100/sec)
            confetti.emission_frequency = 0.05  # Less frequent (20/sec)
            ```
        """
        return self._get_attr("emission_frequency")

    @emission_frequency.setter
    def emission_frequency(self, value: OptionalNumber):
        """
        Set the frequency at which confetti particles are emitted.

        Args:
            value (float): Emission frequency in seconds. Must be positive.
                          Lower values = more frequent emissions.
                          Typical range: 0.01 to 0.1 seconds.
        """
        self._set_attr("emission_frequency", value)

    # number_of_particles
    @property
    def number_of_particles(self) -> Optional[int]:
        """
        The number of particles emitted in each burst.

        Determines how many confetti particles are created simultaneously
        during each emission cycle. Higher values create denser, more
        spectacular effects but may impact performance on slower devices.

        Returns:
            int: Number of particles per emission burst. Default is 10.

        Example:
            ```python
            confetti.number_of_particles = 5   # Subtle effect
            confetti.number_of_particles = 25  # Dense, dramatic effect
            ```
        """
        return self._get_attr("number_of_particles")

    @number_of_particles.setter
    def number_of_particles(self, value: Optional[int]):
        """
        Set the number of particles emitted in each burst.

        Args:
            value (int): Number of particles per burst. Must be positive.
                        Recommended range: 5-50 particles.
                        Higher values may impact performance.
        """
        self._set_attr("number_of_particles", value)

    # max_blast_force
    @property
    def max_blast_force(self) -> OptionalNumber:
        """
        The maximum initial velocity force applied to confetti particles.

        Controls the upper limit of the random velocity range for particles
        when they are first emitted. Higher values create more energetic,
        far-reaching particles that spread wider and travel further.

        Returns:
            float: Maximum blast force value. Default is 20.0.

        Example:
            ```python
            confetti.max_blast_force = 50.0  # High energy particles
            confetti.max_blast_force = 10.0  # Gentle, close particles
            ```
        """
        return self._get_attr("max_blast_force")

    @max_blast_force.setter
    def max_blast_force(self, value: OptionalNumber):
        """
        Set the maximum initial velocity force for confetti particles.

        Args:
            value (float): Maximum blast force. Must be positive and typically
                          greater than min_blast_force. Range: 1.0 to 100.0.
                          Higher values create more dramatic effects.
        """
        self._set_attr("max_blast_force", value)

    # min_blast_force
    @property
    def min_blast_force(self) -> OptionalNumber:
        """
        The minimum initial velocity force applied to confetti particles.

        Controls the lower limit of the random velocity range for particles
        when they are first emitted. This ensures all particles have at least
        some initial movement, preventing static or barely moving particles.

        Returns:
            float: Minimum blast force value. Default is 5.0.

        Example:
            ```python
            confetti.min_blast_force = 15.0  # All particles energetic
            confetti.min_blast_force = 2.0   # Some slow particles allowed
            ```
        """
        return self._get_attr("min_blast_force")

    @min_blast_force.setter
    def min_blast_force(self, value: OptionalNumber):
        """
        Set the minimum initial velocity force for confetti particles.

        Args:
            value (float): Minimum blast force. Must be positive and typically
                          less than max_blast_force. Range: 0.1 to 50.0.
                          Ensures all particles have minimum movement.
        """
        self._set_attr("min_blast_force", value)

    # blast_directionality
    @property
    def blast_directionality(self) -> Optional[BlastDirectionality]:
        """
        The emission pattern for confetti particles.

        Determines how particles are distributed when emitted, affecting
        the overall visual pattern and spread of the confetti animation.

        Returns:
            BlastDirectionality: The current emission pattern.

        Available patterns:
            - **DIRECTIONAL**: Particles emit in a specific direction with some spread.
                              Perfect for targeted effects like confetti cannons.
            - **EXPLOSIVE**: Particles emit in all directions from the center.
                            Creates spectacular burst effects.

        Example:
            ```python
            # Confetti cannon effect
            confetti.blast_directionality = BlastDirectionality.DIRECTIONAL
            confetti.blast_direction = math.pi / 2  # Downward

            # Firework burst effect
            confetti.blast_directionality = BlastDirectionality.EXPLOSIVE
            ```
        """
        return self.__blast_directionality

    @blast_directionality.setter
    def blast_directionality(self, value: Optional[BlastDirectionality]):
        """
        Set the emission pattern for confetti particles.

        Args:
            value (BlastDirectionality): The emission pattern to use.
                                       Use BlastDirectionality.DIRECTIONAL for
                                       targeted effects or EXPLOSIVE for bursts.
        """
        self.__blast_directionality = value
        self._set_enum_attr("blast_directionality", value, BlastDirectionality)

    # blast_direction
    @property
    def blast_direction(self) -> OptionalNumber:
        """
        The primary emission direction for confetti particles in radians.

        Defines the central angle from which particles are emitted when using
        DIRECTIONAL blast pattern. The angle is measured in radians from the
        positive X-axis (rightward direction), following standard mathematical
        convention.

        Returns:
            float: Direction angle in radians. Default is π (leftward).

        Common directions:
            - 0 or 2π: Rightward (→)
            - π/2: Downward (↓)
            - π: Leftward (←)
            - 3π/2: Upward (↑)

        Example:
            ```python
            import math
            confetti.blast_direction = math.pi / 2    # Downward
            confetti.blast_direction = 0              # Rightward
            confetti.blast_direction = math.pi        # Leftward
            confetti.blast_direction = 3 * math.pi / 2  # Upward
            ```

        Note:
            This property only affects DIRECTIONAL blast patterns.
            EXPLOSIVE patterns ignore this setting.
        """
        return self._get_attr("blast_direction")

    @blast_direction.setter
    def blast_direction(self, value: OptionalNumber):
        """
        Set the primary emission direction for confetti particles.

        Args:
            value (float): Direction angle in radians. Range: 0 to 2π.
                          Use math.pi constants for common directions.
                          Only effective with DIRECTIONAL blast pattern.
        """
        self._set_attr("blast_direction", value)

    # gravity
    @property
    def gravity(self) -> OptionalNumber:
        """
        The gravitational force affecting confetti particles.

        Controls how quickly particles accelerate downward (or upward if negative).
        This creates realistic falling motion and affects the overall trajectory
        and lifespan of particles in the animation.

        Returns:
            float: Gravity value. Default is 0.1.
                  - Positive values: Particles fall downward
                  - Negative values: Particles float upward
                  - Zero: Particles maintain initial velocity

        Example:
            ```python
            confetti.gravity = 0.3   # Fast falling (heavy particles)
            confetti.gravity = 0.05  # Slow falling (light particles)
            confetti.gravity = -0.1  # Floating upward effect
            confetti.gravity = 0     # Zero gravity (space effect)
            ```
        """
        return self._get_attr("gravity")

    @gravity.setter
    def gravity(self, value: OptionalNumber):
        """
        Set the gravitational force for confetti particles.

        Args:
            value (float): Gravity acceleration value.
                          Typical range: -0.5 to 0.5
                          Higher absolute values create more dramatic effects.
        """
        self._set_attr("gravity", value)

    # should_loop
    @property
    def should_loop(self) -> Optional[bool]:
        """
        Whether the confetti animation should loop continuously.

        Controls if the animation repeats automatically after completing
        its duration cycle. When enabled, the animation will restart
        immediately after finishing, creating a continuous effect.

        Returns:
            bool: True if animation loops, False for single play. Default is False.

        Example:
            ```python
            confetti.should_loop = True   # Continuous celebration
            confetti.should_loop = False  # One-time effect
            ```

        Note:
            Looping animations must be manually stopped using stop() method.
            Consider performance impact for long-running loop animations.
        """
        return self._get_attr("should_loop")

    @should_loop.setter
    def should_loop(self, value: Optional[bool]):
        """
        Set whether the confetti animation should loop continuously.

        Args:
            value (bool): True to enable looping, False for single play.
                         Looping animations require manual stopping.
        """
        self._set_attr("should_loop", value)

    # display_target
    @property
    def display_target(self) -> Optional[bool]:
        """
        Whether to display a visual target indicator at the emission point.

        Shows a small visual marker at the confetti emission source for
        debugging and positioning purposes. Useful during development
        to understand particle emission location and direction.

        Returns:
            bool: True to show target indicator, False to hide. Default is False.

        Example:
            ```python
            confetti.display_target = True   # Show emission point
            confetti.display_target = False  # Hide for production
            ```

        Note:
            This is primarily a development and debugging feature.
            Typically disabled in production applications.
        """
        return self._get_attr("display_target")

    @display_target.setter
    def display_target(self, value: Optional[bool]):
        """
        Set whether to display the emission target indicator.

        Args:
            value (bool): True to show target indicator for debugging,
                         False to hide for clean production appearance.
        """
        self._set_attr("display_target", value)

    # colors
    @property
    def colors(self) -> Optional[List[ColorValue]]:
        """
        The list of colors used for confetti particles.

        Defines the color palette for the confetti animation. Colors are
        randomly selected from this list for each particle. Supports various
        color formats including named colors, hex codes, and RGB values.

        When a theme is set, this property returns the colors from that theme.
        Setting explicit colors will override any previously set theme.

        Returns:
            List[ColorValue]: List of color values, or None if using default colors.

        Supported color formats:
            - Named colors: "red", "blue", "green"
            - Hex codes: "#FF5733", "#3498DB"
            - RGB tuples: (255, 87, 51)
            - Flet color constants: ft.Colors.RED

        Example:
            ```python
            # Mixed color formats
            confetti.colors = [
                "red",
                "#00FF00",
                ft.Colors.BLUE,
                (255, 255, 0)  # Yellow
            ]
            ```
        """
        return self._get_attr("colors")

    @colors.setter
    def colors(self, value: Optional[List[ColorValue]]):
        """
        Set the list of colors for confetti particles.

        Setting explicit colors will clear any previously set theme and use
        only the specified colors for the animation.

        Args:
            value (List[ColorValue]): List of color values in any supported format.
                                     Pass None to use default colors.
                                     Empty list will use default colors.

        Example:
            ```python
            # Warm color palette
            confetti.colors = ["#FF6B6B", "#FF8E53", "#FF6B9D", "#C44569"]

            # Clear colors to use defaults
            confetti.colors = None
            ```
        """
        self._set_attr_json("colors", value)

    # theme
    @property
    def theme(self) -> Optional[ConfettiTheme]:
        """
        The predefined color theme for confetti particles.

        Provides access to carefully curated color palettes for different
        occasions and moods. Themes are automatically converted to color
        lists and processed using Flet's color system for optimal compatibility.

        Available themes include:
        - **Festive**: CHRISTMAS, HALLOWEEN, VALENTINE, EASTER, NEW_YEAR
        - **Seasonal**: SPRING, SUMMER, AUTUMN, WINTER
        - **Nature**: FOREST, OCEAN, SUNSET, RAINBOW
        - **Party**: BIRTHDAY, WEDDING, GRADUATION
        - **Style**: NEON, PASTEL, GOLD, SILVER, MONOCHROME

        Returns:
            ConfettiTheme: The currently set theme, or None if using explicit colors.

        Example:
            ```python
            confetti.theme = ConfettiTheme.NEON      # Bright, vibrant colors
            confetti.theme = ConfettiTheme.PASTEL    # Soft, gentle colors
            confetti.theme = ConfettiTheme.RAINBOW   # Full spectrum
            ```
        """
        return self.__theme if hasattr(self, "_FletConfetti__theme") else None

    @theme.setter
    def theme(self, value: Optional[ConfettiTheme]):
        """
        Set a predefined color theme for confetti particles.

        Setting a theme will automatically convert it to the appropriate
        color list and override any previously set explicit colors.
        The theme colors are optimized for visual appeal and accessibility.

        Args:
            value (ConfettiTheme): The theme to apply, or None to clear the theme.
                                  When None, previously set explicit colors remain.

        Example:
            ```python
            # Set a festive theme
            confetti.theme = ConfettiTheme.CHRISTMAS

            # Change to a different mood
            confetti.theme = ConfettiTheme.OCEAN

            # Clear theme (keeps explicit colors if any)
            confetti.theme = None
            ```

        Note:
            Themes are processed in Python and sent as color lists to ensure
            consistent rendering across all platforms and optimal performance.
        """
        self.__theme = value
        if value is not None:
            # Convert theme to colors and set them
            theme_colors = THEME_COLORS.get(value.value, [])
            if theme_colors:
                self._set_attr_json("colors", theme_colors)
                # Clear theme attribute since we're using colors
                self._set_attr("theme", None)
            else:
                # Fallback: send theme string if colors not found
                self._set_attr("theme", value.value)
        else:
            # Clear both theme and colors when theme is None
            self._set_attr("theme", None)
            # Don't clear colors here - let explicit colors remain if set

    # stroke_color
    @property
    def stroke_color(self) -> Optional[ColorValue]:
        """
        The outline color for confetti particles.

        Defines the border color drawn around each particle shape.
        When combined with stroke_width, creates outlined particles
        that stand out better against various backgrounds.

        Returns:
            ColorValue: Stroke color value. Default is "black".

        Example:
            ```python
            confetti.stroke_color = "white"     # White outlines
            confetti.stroke_color = "#000000"   # Black outlines
            confetti.stroke_color = ft.Colors.BLUE  # Blue outlines
            ```

        Note:
            Stroke is only visible when stroke_width > 0.
            Use contrasting colors for better visibility.
        """
        return self._get_attr("stroke_color")

    @stroke_color.setter
    def stroke_color(self, value: Optional[ColorValue]):
        """
        Set the outline color for confetti particles.

        Args:
            value (ColorValue): Color for particle outlines in any supported format.
                               Only visible when stroke_width > 0.
        """
        self._set_attr("stroke_color", value)

    # stroke_width
    @property
    def stroke_width(self) -> OptionalNumber:
        """
        The width of the outline border around confetti particles.

        Controls the thickness of the stroke border drawn around each
        particle shape. A value of 0 disables the stroke entirely.
        Higher values create more prominent outlines.

        Returns:
            float: Stroke width in pixels. Default is 0.0 (no stroke).

        Example:
            ```python
            confetti.stroke_width = 2.0   # Thin outline
            confetti.stroke_width = 5.0   # Thick outline
            confetti.stroke_width = 0.0   # No outline
            ```

        Note:
            Stroke adds visual weight to particles and may impact performance
            with large numbers of particles.
        """
        return self._get_attr("stroke_width")

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        """
        Set the width of the outline border around confetti particles.

        Args:
            value (float): Stroke width in pixels. Use 0 to disable stroke.
                          Typical range: 0.0 to 10.0 pixels.
        """
        self._set_attr("stroke_width", value)

    # minimum_size
    @property
    def minimum_size(self) -> Optional[Size]:
        """
        The minimum size for confetti particles.

        Defines the lower bounds for particle dimensions using Flet's Size dataclass.
        Each particle's size is randomly chosen between minimum and maximum values,
        creating natural size variation and visual interest.

        Returns:
            Size: Minimum particle size (width, height) in pixels. Default is Size(20, 10).

        Example:
            ```python
            from flet.core.size import Size

            confetti.minimum_size = Size(10, 5)   # Small particles
            confetti.minimum_size = Size(30, 20)  # Larger minimum size
            confetti.minimum_size = Size(15, 15)  # Square particles
            ```

        Note:
            Uses Flet's Size dataclass for consistency with the framework.
            Both width and height must be positive values.
        """
        return (
            self.__minimum_size
            if hasattr(self, "_FletConfetti__minimum_size")
            else None
        )

    @minimum_size.setter
    def minimum_size(self, value: Optional[Size]):
        """
        Set the minimum size for confetti particles.

        Args:
            value (Size): Minimum particle size using Flet's Size dataclass.
                         Both width and height must be positive.
                         Pass None to use default size.

        Example:
            ```python
            from flet.core.size import Size
            confetti.minimum_size = Size(width=15, height=8)
            ```

        Note:
            For visible size variation, ensure minimum_size is different from maximum_size.
            If both are identical, all particles will be the same size.
        """
        if value is not None and (value.width <= 0 or value.height <= 0):
            raise ValueError("minimum_size width and height must be positive values")

        self.__minimum_size = value
        if value is not None:
            self._set_attr_json(
                "minimum_size", {"width": value.width, "height": value.height}
            )
        else:
            self._set_attr("minimum_size", None)

    # maximum_size
    @property
    def maximum_size(self) -> Optional[Size]:
        """
        The maximum size for confetti particles.

        Defines the upper bounds for particle dimensions using Flet's Size dataclass.
        Each particle's size is randomly chosen between minimum and maximum values,
        creating natural size variation and visual depth in the animation.

        Returns:
            Size: Maximum particle size (width, height) in pixels. Default is Size(30, 15).

        Example:
            ```python
            from flet.core.size import Size

            confetti.maximum_size = Size(50, 40)  # Large particles
            confetti.maximum_size = Size(25, 12)  # Smaller maximum size
            confetti.maximum_size = Size(20, 20)  # Square particles
            ```

        Note:
            Should typically be larger than minimum_size for proper size variation.
            Uses Flet's Size dataclass for framework consistency.
        """
        return (
            self.__maximum_size
            if hasattr(self, "_FletConfetti__maximum_size")
            else None
        )

    @maximum_size.setter
    def maximum_size(self, value: Optional[Size]):
        """
        Set the maximum size for confetti particles.

        Args:
            value (Size): Maximum particle size using Flet's Size dataclass.
                         Both width and height must be positive and typically
                         larger than minimum_size values.
                         Pass None to use default size.

        Example:
            ```python
            from flet.core.size import Size
            confetti.maximum_size = Size(width=40, height=25)
            ```

        Note:
            For visible size variation, ensure maximum_size is different from minimum_size.
            If both are identical, all particles will be the same size.
        """
        if value is not None and (value.width <= 0 or value.height <= 0):
            raise ValueError("maximum_size width and height must be positive values")

        self.__maximum_size = value
        if value is not None:
            self._set_attr_json(
                "maximum_size", {"width": value.width, "height": value.height}
            )
        else:
            self._set_attr("maximum_size", None)

    def set_particle_size_range(self, min_size: Size, max_size: Size):
        """
        Convenience method to set both minimum and maximum particle sizes with validation.

        Args:
            min_size (Size): Minimum particle size
            max_size (Size): Maximum particle size

        Raises:
            ValueError: If sizes are invalid or min_size >= max_size

        Example:
            ```python
            from flet.core.size import Size

            # Create size variation for visual interest
            confetti.set_particle_size_range(
                min_size=Size(10, 5),   # Small particles
                max_size=Size(50, 25)   # Large particles
            )
            ```
        """
        if min_size.width <= 0 or min_size.height <= 0:
            raise ValueError("min_size width and height must be positive")
        if max_size.width <= 0 or max_size.height <= 0:
            raise ValueError("max_size width and height must be positive")
        if min_size.width >= max_size.width or min_size.height >= max_size.height:
            raise ValueError(
                "min_size must be smaller than max_size in both dimensions"
            )

        self.minimum_size = min_size
        self.maximum_size = max_size

    # particle_drag
    @property
    def particle_drag(self) -> OptionalNumber:
        """
        The air resistance coefficient affecting particle movement.

        Simulates air resistance that gradually slows down particles
        over time. Higher values create more realistic physics with
        particles that decelerate more quickly, while lower values
        allow particles to maintain velocity longer.

        Returns:
            float: Drag coefficient. Default is 0.05.
                  - 0.0: No air resistance (space-like)
                  - 0.1: Heavy air resistance
                  - 0.05: Realistic air resistance

        Example:
            ```python
            confetti.particle_drag = 0.1   # Heavy air resistance
            confetti.particle_drag = 0.02  # Light air resistance
            confetti.particle_drag = 0.0   # No air resistance
            ```
        """
        return self._get_attr("particle_drag")

    @particle_drag.setter
    def particle_drag(self, value: OptionalNumber):
        """
        Set the air resistance coefficient for particle movement.

        Args:
            value (float): Drag coefficient. Range: 0.0 to 1.0.
                          Higher values slow particles more quickly.
                          0.0 disables air resistance entirely.
        """
        self._set_attr("particle_drag", value)

    # canvas_size
    @property
    def canvas_size(self) -> Optional[Size]:
        """
        The size of the confetti animation canvas.

        Defines the boundaries for the confetti animation using Flet's Size dataclass.
        Particles are clipped to this area. If not specified, the canvas uses the
        full available size of the parent container with automatic sizing.

        Returns:
            Size: Canvas size (width, height) in pixels, or None for auto-sizing.

        Example:
            ```python
            from flet.core.size import Size

            confetti.canvas_size = Size(800, 600)  # Fixed 800x600 canvas
            confetti.canvas_size = Size(400, 300)  # Smaller canvas
            confetti.canvas_size = None            # Auto-size to container
            ```

        Note:
            Auto-sizing (None) is recommended for responsive layouts.
            Fixed sizes are useful for precise control over animation boundaries.
        """
        return (
            self.__canvas_size if hasattr(self, "_FletConfetti__canvas_size") else None
        )

    @canvas_size.setter
    def canvas_size(self, value: Optional[Size]):
        """
        Set the size of the confetti animation canvas.

        Args:
            value (Size): Canvas size using Flet's Size dataclass, or None for auto-sizing.
                         Both width and height must be positive if specified.

        Example:
            ```python
            from flet.core.size import Size
            confetti.canvas_size = Size(width=1000, height=800)
            ```
        """
        self.__canvas_size = value
        if value is not None:
            self._set_attr_json(
                "canvas_size", {"width": value.width, "height": value.height}
            )
        else:
            self._set_attr("canvas_size", None)

    # pause_emission_on_low_frame_rate
    @property
    def pause_emission_on_low_frame_rate(self) -> Optional[bool]:
        """
        Whether to pause particle emission when frame rate drops.

        Automatically pauses new particle creation when the animation
        frame rate falls below optimal levels. This helps maintain
        smooth performance on slower devices by reducing particle
        density during performance bottlenecks.

        Returns:
            bool: True to enable auto-pause, False to disable. Default is True.

        Example:
            ```python
            confetti.pause_emission_on_low_frame_rate = True   # Auto-optimize
            confetti.pause_emission_on_low_frame_rate = False  # Always emit
            ```

        Note:
            Recommended to keep enabled for better user experience
            across different device capabilities.
        """
        return self._get_attr("pause_emission_on_low_frame_rate")

    @pause_emission_on_low_frame_rate.setter
    def pause_emission_on_low_frame_rate(self, value: Optional[bool]):
        """
        Set whether to pause emission during low frame rates.

        Args:
            value (bool): True to enable automatic performance optimization,
                         False to maintain constant emission regardless of performance.
        """
        self._set_attr("pause_emission_on_low_frame_rate", value)

    # create_particle_path (deprecated)
    @property
    def create_particle_path(self) -> Optional[str]:
        """
        Custom particle path definition (deprecated).

        Legacy property for defining custom particle shapes using path strings.
        This property is deprecated in favor of the more robust particle_shape
        enumeration which provides better type safety and predefined shapes.

        Returns:
            str: Custom path string, or None.

        Note:
            DEPRECATED: Use particle_shape property instead for better
            type safety and predefined shape options.
        """
        return self._get_attr("create_particle_path")

    @create_particle_path.setter
    def create_particle_path(self, value: Optional[str]):
        """
        Set custom particle path definition (deprecated).

        Args:
            value (str): Custom path string definition.

        Warning:
            DEPRECATED: Use particle_shape property instead.
            This property is maintained for backward compatibility only.
        """
        self._set_attr("create_particle_path", value)

    # particle_shape
    @property
    def particle_shape(self) -> Optional[ParticleShape]:
        """
        The shape of individual confetti particles.

        Determines the visual appearance of each particle in the animation.
        Different shapes can create different moods and themes for your
        confetti effects.

        Returns:
            ParticleShape: The current particle shape.

        Available shapes:
            - **CIRCLE**: Classic round confetti pieces
            - **SQUARE**: Square-shaped particles
            - **TRIANGLE**: Triangular confetti pieces
            - **STAR**: Star-shaped particles (festive)
            - **HEART**: Heart-shaped particles (romantic)
            - **DIAMOND**: Diamond-shaped particles (elegant)
            - **FLOWER**: Flower-shaped particles (natural)
            - **BUTTERFLY**: Butterfly-shaped particles (whimsical)
            - **SNOWFLAKE**: Snowflake-shaped particles (winter theme)
            - **MUSIC_NOTE**: Musical note particles (celebration)

        Example:
            ```python
            confetti.particle_shape = ParticleShape.STAR     # Festive
            confetti.particle_shape = ParticleShape.HEART    # Romantic
            confetti.particle_shape = ParticleShape.SNOWFLAKE # Winter
            ```
        """
        return self.__particle_shape

    @particle_shape.setter
    def particle_shape(self, value: Optional[ParticleShape]):
        """
        Set the shape of confetti particles.

        Setting a predefined shape will clear any custom particle path.

        Args:
            value (ParticleShape): The shape to use for particles.
                                  Choose from predefined shapes that match
                                  your app's theme and occasion.
        """
        self.__particle_shape = value
        if value is not None:
            # Clear custom path when setting predefined shape
            self.__custom_particle_path = None
            self._set_attr("custom_particle_path", None)
        self._set_enum_attr("particle_shape", value, ParticleShape)

    # custom_particle_path
    @property
    def custom_particle_path(self) -> Optional[str]:
        """
        Custom SVG path string for defining particle shapes.

        Allows you to create completely custom particle shapes using SVG path syntax.
        This provides unlimited flexibility for creating unique confetti effects that
        match your brand, theme, or specific design requirements.

        When set, this property takes priority over the particle_shape property,
        allowing you to override predefined shapes with your own custom designs.

        Returns:
            str: SVG path string, or None if using predefined shapes.

        SVG Path Syntax:
            - **M x,y**: Move to point (x, y)
            - **L x,y**: Line to point (x, y)
            - **Q x1,y1 x,y**: Quadratic curve to (x, y) with control point (x1, y1)
            - **C x1,y1 x2,y2 x,y**: Cubic curve with two control points
            - **Z**: Close path (return to start point)
            - **H x**: Horizontal line to x coordinate
            - **V y**: Vertical line to y coordinate

        Examples:
            ```python
            # Custom star shape
            confetti.custom_particle_path = "M10,1 L12,7 L19,7 L14,11 L16,18 L10,14 L4,18 L6,11 L1,7 L8,7 Z"

            # Heart shape
            confetti.custom_particle_path = "M12,21.35l-1.45-1.32C5.4,15.36,2,12.28,2,8.5 C2,5.42,4.42,3,7.5,3c1.74,0,3.41,0.81,4.5,2.09C13.09,3.81,14.76,3,16.5,3 C19.58,3,22,5.42,22,8.5c0,3.78-3.4,6.86-8.55,11.54L12,21.35z"

            # Lightning bolt
            confetti.custom_particle_path = "M7,2 L13,2 L11,8 L17,8 L7,18 L9,12 L3,12 Z"

            # Custom logo (example)
            confetti.custom_particle_path = "M5,5 L15,5 L15,15 L5,15 Z M7,7 L13,7 L13,13 L7,13 Z"
            ```

        Design Tips:
            - Keep paths simple for better performance
            - Use coordinates roughly in 0-20 range for best scaling
            - Test with different particle sizes to ensure good appearance
            - Consider the visual impact at small sizes (particles can be tiny)

        Note:
            Setting a custom path will automatically clear any previously set
            particle_shape. The custom path takes priority and will be used
            for all particles in the animation.
        """
        return (
            self.__custom_particle_path
            if hasattr(self, "_FletConfetti__custom_particle_path")
            else None
        )

    @custom_particle_path.setter
    def custom_particle_path(self, value: Optional[str]):
        """
        Set a custom SVG path string for particle shapes.

        Setting a custom path will override any previously set particle_shape,
        giving you complete control over the particle appearance.

        Args:
            value (str): SVG path string using standard SVG path syntax.
                        Pass None to clear custom path and use particle_shape.

        Path Validation:
            - Must be a valid SVG path string
            - Should use coordinates in reasonable range (0-100)
            - Complex paths may impact performance

        Examples:
            ```python
            # Set custom star
            confetti.custom_particle_path = "M10,1 L12,7 L19,7 L14,11 L16,18 L10,14 L4,18 L6,11 L1,7 L8,7 Z"

            # Clear custom path (use particle_shape instead)
            confetti.custom_particle_path = None
            ```

        Performance Notes:
            - Custom paths are cached for optimal performance
            - Simple paths (< 10 commands) are recommended
            - Very complex paths may cause frame rate drops with many particles
        """
        self.__custom_particle_path = value
        if value is not None:
            # Clear predefined shape when setting custom path
            self.__particle_shape = None
            self._set_attr("particle_shape", None)
            self._set_attr("custom_particle_path", value)
        else:
            self._set_attr("custom_particle_path", None)

    # duration_seconds
    @property
    def duration_seconds(self) -> Optional[int]:
        """
        The duration of the confetti animation in seconds.

        Defines how long the animation runs before automatically stopping.
        After this duration, no new particles are emitted, but existing
        particles continue their natural motion until they disappear.

        Returns:
            int: Animation duration in seconds. Default is 10.

        Example:
            ```python
            confetti.duration_seconds = 5    # Short celebration
            confetti.duration_seconds = 30   # Extended celebration
            confetti.duration_seconds = 1    # Quick burst
            ```

        Note:
            When should_loop is True, the animation restarts after
            this duration. Use stop() to halt looping animations.
        """
        return self._get_attr("duration_seconds")

    @duration_seconds.setter
    def duration_seconds(self, value: Optional[int]):
        """
        Set the duration of the confetti animation.

        Args:
            value (int): Duration in seconds. Must be positive.
                        Typical range: 1 to 60 seconds.
                        Longer durations may impact performance.
        """
        self._set_attr("duration_seconds", value)

    # on_animation_end
    @property
    def on_animation_end(self) -> OptionalControlEventCallable:
        """
        Event handler called when the confetti animation completes.

        This callback is triggered when the animation duration expires
        and the animation naturally stops. Useful for chaining animations,
        updating UI state, or performing cleanup actions.

        Returns:
            Callable: Event handler function, or None if not set.

        Example:
            ```python
            def celebration_complete(e):
                print("Confetti animation finished!")
                # Update UI or trigger next action

            confetti.on_animation_end = celebration_complete
            ```

        Note:
            Not triggered when animation is manually stopped using stop().
            For looping animations, called after each cycle completion.
        """
        return self._get_event_handler("on_animation_end")

    @on_animation_end.setter
    def on_animation_end(self, handler: OptionalControlEventCallable):
        """
        Set the event handler for animation completion.

        Args:
            handler (Callable): Function to call when animation ends naturally.
                               Receives a control event parameter.
                               Pass None to remove the handler.

        Example:
            ```python
            confetti.on_animation_end = lambda e: print("Done!")
            ```
        """
        self._add_event_handler("on_animation_end", handler)

    # Control methods
    def play(self):
        """
        Start the confetti animation.

        Begins emitting confetti particles according to the configured settings.
        The animation will run for the specified duration or until manually stopped.
        If the animation is already playing, this method has no effect.

        Returns:
            bool: True if the animation started successfully, False otherwise.

        Example:
            ```python
            # Start a celebration
            confetti.play()

            # Chain with other actions
            if confetti.play():
                print("Confetti started!")
            ```

        Note:
            The animation respects the `duration_seconds` property and will
            automatically stop after the specified time unless `should_loop`
            is set to True.
        """
        return self.invoke_method("play", wait_for_result=True)

    def stop(self, clear_all_particles: bool = False):
        """
        Stop the confetti animation.

        Halts the emission of new particles and optionally clears existing
        particles from the screen. This method provides control over how
        the animation ends.

        Args:
            clear_all_particles (bool): Controls particle cleanup behavior.
                                       - True: Immediately removes all particles
                                         from the screen for instant cleanup.
                                       - False: Allows existing particles to
                                         complete their natural animation cycle.
                                       Default is False.

        Returns:
            bool: True if the animation stopped successfully, False otherwise.

        Example:
            ```python
            # Graceful stop - let particles finish
            confetti.stop()

            # Immediate cleanup
            confetti.stop(clear_all_particles=True)

            # Conditional stopping
            if user_wants_to_stop:
                confetti.stop(clear_all_particles=True)
            ```

        Note:
            This method can be called at any time during the animation.
            If no animation is currently playing, the method has no effect.
        """
        args = {"clear_all_particles": str(clear_all_particles).lower()}
        return self.invoke_method("stop", args, wait_for_result=True)

    def reload(self):
        """
        Reload/reset the confetti controller completely.
        This reinitializes the controller and can help recover from any state issues.
        """
        return self.invoke_method("reload", wait_for_result=True)

    def reset(self):
        """
        Reset the confetti controller completely.
        Alias for reload() method.
        """
        return self.invoke_method("reset", wait_for_result=True)

    def get_controller_state(self):
        """
        Get the current state of the confetti controller.
        Useful for debugging purposes.
        """
        return self.invoke_method("get_state", wait_for_result=True)
