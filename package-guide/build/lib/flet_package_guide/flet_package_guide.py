# from enum import Enum
from typing import Any, Optional, List

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.control import Control
import json

from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
)


class FletPackageGuide(ConstrainedControl):
    """
    FletPackageGuide Control description.
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
        # FletPackageGuide specific
        #
        colors: Optional[List[ColorValue]] = None,
        content: Optional[Control] = None,
        on_something: OptionalControlEventCallable = None,
        complex_data: Optional[Any] = None,
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

        self.colors = colors
        self.content = content
        self.on_something = on_something
        self.complex_data = complex_data

    # controls name reference
    # OK
    def _get_control_name(self):
        return "flet_package_guide"

    # ENDOK

    # colors
    # OK. Passing list of colors
    # FLET PYTHON SIDE
    @property
    def colors(self):
        """
        colors property description.
        """
        return self._get_attr("colors")

    @colors.setter
    def colors(self, colors: Optional[List[ColorValue]]):
        self._set_attr_json("colors", colors)

    # FLUTTER DART SIDE
    # final String? colorListJs = control.attrString("colors", null);
    # List<Color> colors = [Colors.red, Colors.blue, Colors.green]; // default
    # if (colorListJs != null) {
    #   try {
    #     final List<dynamic> colorStrings = json.decode(colorListJs);
    #     colors = parseColors(Theme.of(context), colorStrings);
    #   } catch (e) {}
    # }
    # ENDOK. Done passing list of colors

    # content
    # OK. Passing control to dart as widget
    # FLET PYTHON SIDE
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # FLUTTER DART SIDE
    # var contentCtrls =
    #     children.where((c) => c.name == "thumb_icon" && c.isVisible);
    # bool? adaptive =
    #     control.attrBool("adaptive") ?? parentAdaptive;
    # bool disabled = control.isDisabled || parentDisabled;
    # Widget? widget = null;
    # if (contentCtrls.isNotEmpty) {
    #   widget = createControl(control, contentCtrls.first.id, disabled,
    #       parentAdaptive: adaptive);
    # }
    # ENDOK. Passing control to dart as widget

    # on_something
    # OK. Passing Event Callable
    # FLET PYTHON SIDE
    @property
    def on_something(self) -> OptionalControlEventCallable:
        self._set_attr_json
        return self._get_event_handler("on_something")

    @on_something.setter
    def on_something(self, handler: OptionalControlEventCallable):
        self._add_event_handler("on_something", handler)

    # FLUTTER DART SIDE
    #   void handleSomething(dynamic value) {
    #     String newValue = value.toString();
    #     debugPrint("Handler triggered: $newValue");
    #     var props = {"value": newValue};
    #     // OK - We update the Control State and Triggering Control Event
    #     backend.updateControlState(control.id, props);
    #     backend.triggerControlEvent(control.id, "on_something", newValue);
    #     // ENDOK - We update the Control State and Triggering Control Event
    #   }
    # ENDOK. Passing Event Callable

    # complex_data
    # OK. Passing complex Data (JSON)
    # FLET PYTHON SIDE
    @property
    def complex_data(self) -> Optional[Any]:
        raw = self._get_attr("complex_data", None)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None

    @complex_data.setter
    def complex_data(self, value: Optional[Any]):
        self._set_attr_json("complex_data", value=value)

    # FLUTTER DART SIDE
    # final String? complexDataJson = control.attrString("complex_data", null);
    # Map<String, dynamic>? complexData;
    # if (complexDataJson != null) {
    #     try {
    #     complexData = json.decode(complexDataJson);
    #     } catch (e) {
    #     complexData = {"error": "Invalid JSON"};
    #     }
    # }
    # Widget debugText = Text(
    #     complexData != null ? json.encode(complexData) : "No complex data",
    #     style: TextStyle(fontSize: 12, color: Colors.black),
    # );
    # ENDOK. Passing complex Data (JSON)


    def play(self, some:str="thing"):
        args = {"some": some}
        return self.invoke_method("play", args)
    def stop(self, love:str="you"):
        args = {"love": love}
        return self.invoke_method("stop", args)