from enum import Enum
from typing import Any, Optional, List, Union

from flet.core.size import Size
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
)
import math

class BlastDirectionality(Enum):
    DIRECTIONAL = "directional"
    EXPLOSIVE = "explosive"


class ConfettiTheme(Enum):
    """
    Predefined color themes for confetti animations.
    Theme names are sent to Dart as strings and interpreted there.
    If colors are explicitly set, the theme will be ignored.
    """

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


class ParticleShape(Enum):
    """
    Predefined particle shapes for confetti animations.
    Each shape corresponds to a Path implementation in Dart.
    """

    # Basic shapes
    RECTANGLE = "rectangle"  # Default rectangular particles
    CIRCLE = "circle"
    SQUARE = "square"

    # Geometric shapes
    TRIANGLE = "triangle"
    DIAMOND = "diamond"
    HEXAGON = "hexagon"
    PENTAGON = "pentagon"
    OCTAGON = "octagon"

    # Star variations
    STAR = "star"  # 5-pointed star (existing)
    STAR_4 = "star_4"  # 4-pointed star
    STAR_6 = "star_6"  # 6-pointed star
    STAR_8 = "star_8"  # 8-pointed star

    # Fun shapes
    HEART = "heart"
    FLOWER = "flower"
    LEAF = "leaf"
    BUTTERFLY = "butterfly"

    # Symbols
    CROSS = "cross"
    PLUS = "plus"
    ARROW = "arrow"
    LIGHTNING = "lightning"

    # Special shapes (for you to add complex paths later)
    SKULL = "skull"
    CROWN = "crown"
    SNOWFLAKE = "snowflake"
    MUSIC_NOTE = "music_note"


# Type alias for color source - can be either explicit colors or a theme
ColorSource = Union[List[ColorValue], ConfettiTheme, None]


class FletConfetti(ConstrainedControl):
    """
    FletConfetti Control - A confetti animation widget for Flet.

    Provides customizable confetti animations with various parameters for
    emission frequency, particle count, blast direction, colors, and more.

    Color Configuration:
    - Use colors parameter for explicit colors: colors=["red", "blue", "green"]
    - Use theme parameter for predefined themes: theme=ConfettiTheme.NEON
    - If both are provided, colors takes priority
    - If neither is provided, default colors are used

    Examples:
        # Using explicit colors
        confetti = FletConfetti(colors=["red", "blue", "green"])

        # Using a theme
        confetti = FletConfetti(theme=ConfettiTheme.NEON)

        # Using default colors
        confetti = FletConfetti()
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
        minimum_size_width: OptionalNumber = 20,
        minimum_size_height: OptionalNumber = 10,
        maximum_size_width: OptionalNumber = 30,
        maximum_size_height: OptionalNumber = 15,
        particle_drag: OptionalNumber = 0.05,
        canvas_width: OptionalNumber = None,
        canvas_height: OptionalNumber = None,
        pause_emission_on_low_frame_rate: Optional[bool] = True,
        create_particle_path: Optional[
            str
        ] = None,  # Deprecated: use particle_shape instead
        particle_shape: Optional[ParticleShape] = None,
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
        self.minimum_size_width = minimum_size_width
        self.minimum_size_height = minimum_size_height
        self.maximum_size_width = maximum_size_width
        self.maximum_size_height = maximum_size_height
        self.particle_drag = particle_drag
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.pause_emission_on_low_frame_rate = pause_emission_on_low_frame_rate
        self.create_particle_path = create_particle_path
        self.particle_shape = particle_shape
        self.duration_seconds = duration_seconds
        self.on_animation_end = on_animation_end

    def _get_control_name(self):
        return "flet_confetti"

    # emission_frequency
    @property
    def emission_frequency(self) -> OptionalNumber:
        return self._get_attr("emission_frequency")

    @emission_frequency.setter
    def emission_frequency(self, value: OptionalNumber):
        self._set_attr("emission_frequency", value)

    # number_of_particles
    @property
    def number_of_particles(self) -> Optional[int]:
        return self._get_attr("number_of_particles")

    @number_of_particles.setter
    def number_of_particles(self, value: Optional[int]):
        self._set_attr("number_of_particles", value)

    # max_blast_force
    @property
    def max_blast_force(self) -> OptionalNumber:
        return self._get_attr("max_blast_force")

    @max_blast_force.setter
    def max_blast_force(self, value: OptionalNumber):
        self._set_attr("max_blast_force", value)

    # min_blast_force
    @property
    def min_blast_force(self) -> OptionalNumber:
        return self._get_attr("min_blast_force")

    @min_blast_force.setter
    def min_blast_force(self, value: OptionalNumber):
        self._set_attr("min_blast_force", value)

    # blast_directionality
    @property
    def blast_directionality(self) -> Optional[BlastDirectionality]:
        return self.__blast_directionality

    @blast_directionality.setter
    def blast_directionality(self, value: Optional[BlastDirectionality]):
        self.__blast_directionality = value
        self._set_enum_attr("blast_directionality", value, BlastDirectionality)

    # blast_direction
    @property
    def blast_direction(self) -> OptionalNumber:
        return self._get_attr("blast_direction")

    @blast_direction.setter
    def blast_direction(self, value: OptionalNumber):
        self._set_attr("blast_direction", value)

    # gravity
    @property
    def gravity(self) -> OptionalNumber:
        return self._get_attr("gravity")

    @gravity.setter
    def gravity(self, value: OptionalNumber):
        self._set_attr("gravity", value)

    # should_loop
    @property
    def should_loop(self) -> Optional[bool]:
        return self._get_attr("should_loop")

    @should_loop.setter
    def should_loop(self, value: Optional[bool]):
        self._set_attr("should_loop", value)

    # display_target
    @property
    def display_target(self) -> Optional[bool]:
        return self._get_attr("display_target")

    @display_target.setter
    def display_target(self, value: Optional[bool]):
        self._set_attr("display_target", value)

    # colors
    @property
    def colors(self) -> Optional[List[ColorValue]]:
        return self._get_attr("colors")

    @colors.setter
    def colors(self, value: Optional[List[ColorValue]]):
        self._set_attr_json("colors", value)

    # theme
    @property
    def theme(self) -> Optional[ConfettiTheme]:
        return self.__theme if hasattr(self, "_FletConfetti__theme") else None

    @theme.setter
    def theme(self, value: Optional[ConfettiTheme]):
        self.__theme = value
        self._set_attr("theme", value.value if value else None)

    # stroke_color
    @property
    def stroke_color(self) -> Optional[ColorValue]:
        return self._get_attr("stroke_color")

    @stroke_color.setter
    def stroke_color(self, value: Optional[ColorValue]):
        self._set_attr("stroke_color", value)

    # stroke_width
    @property
    def stroke_width(self) -> OptionalNumber:
        return self._get_attr("stroke_width")

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        self._set_attr("stroke_width", value)

    # minimum_size_width
    @property
    def minimum_size_width(self) -> OptionalNumber:
        return self._get_attr("minimum_size_width")

    @minimum_size_width.setter
    def minimum_size_width(self, value: OptionalNumber):
        self._set_attr("minimum_size_width", value)

    # minimum_size_height
    @property
    def minimum_size_height(self) -> OptionalNumber:
        return self._get_attr("minimum_size_height")

    @minimum_size_height.setter
    def minimum_size_height(self, value: OptionalNumber):
        self._set_attr("minimum_size_height", value)

    # maximum_size_width
    @property
    def maximum_size_width(self) -> OptionalNumber:
        return self._get_attr("maximum_size_width")

    @maximum_size_width.setter
    def maximum_size_width(self, value: OptionalNumber):
        self._set_attr("maximum_size_width", value)

    # maximum_size_height
    @property
    def maximum_size_height(self) -> OptionalNumber:
        return self._get_attr("maximum_size_height")

    @maximum_size_height.setter
    def maximum_size_height(self, value: OptionalNumber):
        self._set_attr("maximum_size_height", value)

    # particle_drag
    @property
    def particle_drag(self) -> OptionalNumber:
        return self._get_attr("particle_drag")

    @particle_drag.setter
    def particle_drag(self, value: OptionalNumber):
        self._set_attr("particle_drag", value)

    # canvas_width
    @property
    def canvas_width(self) -> OptionalNumber:
        return self._get_attr("canvas_width")

    @canvas_width.setter
    def canvas_width(self, value: OptionalNumber):
        self._set_attr("canvas_width", value)

    # canvas_height
    @property
    def canvas_height(self) -> OptionalNumber:
        return self._get_attr("canvas_height")

    @canvas_height.setter
    def canvas_height(self, value: OptionalNumber):
        self._set_attr("canvas_height", value)

    # pause_emission_on_low_frame_rate
    @property
    def pause_emission_on_low_frame_rate(self) -> Optional[bool]:
        return self._get_attr("pause_emission_on_low_frame_rate")

    @pause_emission_on_low_frame_rate.setter
    def pause_emission_on_low_frame_rate(self, value: Optional[bool]):
        self._set_attr("pause_emission_on_low_frame_rate", value)

    # create_particle_path (deprecated)
    @property
    def create_particle_path(self) -> Optional[str]:
        return self._get_attr("create_particle_path")

    @create_particle_path.setter
    def create_particle_path(self, value: Optional[str]):
        self._set_attr("create_particle_path", value)

    # particle_shape
    @property
    def particle_shape(self) -> Optional[ParticleShape]:
        return self.__particle_shape

    @particle_shape.setter
    def particle_shape(self, value: Optional[ParticleShape]):
        self.__particle_shape = value
        self._set_enum_attr("particle_shape", value, ParticleShape)

    # duration_seconds
    @property
    def duration_seconds(self) -> Optional[int]:
        return self._get_attr("duration_seconds")

    @duration_seconds.setter
    def duration_seconds(self, value: Optional[int]):
        self._set_attr("duration_seconds", value)

    # on_animation_end
    @property
    def on_animation_end(self) -> OptionalControlEventCallable:
        return self._get_event_handler("on_animation_end")

    @on_animation_end.setter
    def on_animation_end(self, handler: OptionalControlEventCallable):
        self._add_event_handler("on_animation_end", handler)

    # Control methods
    def play(self):
        """Start the confetti animation."""
        return self.invoke_method("play", wait_for_result=True)

    def stop(self, clear_all_particles: bool = False):
        """
        Stop the confetti animation.

        Args:
            clear_all_particles (bool): If True, immediately clears all particles from the screen.
                                      If False, particles will continue to fall until they naturally disappear.
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
