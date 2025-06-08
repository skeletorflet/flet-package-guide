from enum import Enum
from typing import Any, Optional, List

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

class FletConfetti(ConstrainedControl):
    """
    FletConfetti Control - A confetti animation widget for Flet.
    
    Provides customizable confetti animations with various parameters for
    emission frequency, particle count, blast direction, colors, and more.
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
        blast_directionality: Optional[BlastDirectionality] = BlastDirectionality.DIRECTIONAL,
        blast_direction: OptionalNumber = math.pi,
        gravity: OptionalNumber = 0.2,
        should_loop: Optional[bool] = False,
        display_target: Optional[bool] = False,
        colors: Optional[List[ColorValue]] = None,
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
        create_particle_path: Optional[str] = None,
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

    # create_particle_path
    @property
    def create_particle_path(self) -> Optional[str]:
        return self._get_attr("create_particle_path")

    @create_particle_path.setter
    def create_particle_path(self, value: Optional[str]):
        self._set_attr("create_particle_path", value)

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
        self.invoke_method("play")

    def stop(self):
        """Stop the confetti animation."""
        self.invoke_method("stop")
