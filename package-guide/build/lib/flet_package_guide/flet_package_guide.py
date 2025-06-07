# from enum import Enum
from typing import Any, Optional, List

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.control import Control
import json

from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
    WebRenderer,
)
import uuid
import concurrent.futures

class FletPackageGuide(ConstrainedControl):
    """
    FletPackageGuide Control description.

    This control demonstrates various patterns of communication between Python and Dart.
    It includes basic property mappings, event handling, and more advanced scenarios such as:
    - Asynchronous operations with callbacks.
    - Python calls to Dart with timeout handling.
    - Dart-initiated periodic events.
    - Tasks with multiple progress updates from Dart to Python.

    For detailed explanations and example usage of these advanced patterns,
    please refer to the "Advanced Communication Examples" section in the project's README.md file.
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
        self._async_callbacks = {}
        self._progress_handlers = {}
        self._completion_handlers = {} # Corrected initialization
        self._add_event_handler("async_callback", self._on_async_callback)
        self._add_event_handler("task_update", self._on_task_update)
        self._add_event_handler("shared_value_changed_from_dart", self._on_shared_value_changed_from_dart)

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
        return self.invoke_method("play", args, wait_for_result=True)
    def stop(self, love:str="you"):
        args = {"love": love}
        return self.invoke_method("stop", args, wait_for_result=True)

    def async_operation_with_callback(self, message: str, python_callback: callable):
        """
        Starts an asynchronous operation on the Dart side and calls the
        provided Python callback upon completion.

        :param message: A message to send to the Dart side.
        :param python_callback: A Python function to call when the async operation completes.
                                This function should accept one argument (the result from Dart).
        """
        callback_id = str(uuid.uuid4())
        self._async_callbacks[callback_id] = python_callback
        self.invoke_method(
            "start_async_task", {"message": message, "callback_id": callback_id}
        )

    def _on_async_callback(self, e):
        """
        Handles the 'async_callback' event triggered by Dart.
        Retrieves the Python callback associated with the callback_id
        and executes it with the data from Dart.
        """
        # print(f"Python _on_async_callback received: {e.data}")
        event_data = json.loads(e.data)
        callback_id = event_data.get("callback_id")
        data = event_data.get("data")
        # print(f"Callback ID: {callback_id}, Data: {data}")

        if callback_id in self._async_callbacks:
            callback = self._async_callbacks.pop(callback_id)
            # print(f"Executing callback: {callback} with data: {data}")
            callback(data)
        else:
            # print(f"Error: Callback ID {callback_id} not found.")
            pass

    def call_dart_with_timeout(self, data_to_send: str, python_timeout_sec: float, dart_task_duration_ms: int):
        """
        Calls a Dart method that simulates a long-running task and handles potential timeouts.

        :param data_to_send: Data to send to the Dart method.
        :param python_timeout_sec: Time in seconds for Python to wait for the Dart method to respond.
        :param dart_task_duration_ms: Time in milliseconds for Dart to simulate work.
        :return: The result from Dart if successful, or a timeout message if it times out.
        """
        try:
            # Flet docs say: "If timeout is specified and the call takes longer than timeout seconds,
            # then a concurrent.futures.TimeoutError exception will be raised."
            result = self.invoke_method(
                "long_running_task",
                {
                    "data": data_to_send,
                    "duration_ms": dart_task_duration_ms  # Dart will use this to simulate work
                },
                wait_for_result=True,
                timeout=python_timeout_sec  # Python-side timeout for the call
            )

            if result is None:
                # This case might occur if Flet's timeout behavior changes or for other non-exception interruptions.
                # Based on Flet docs, TimeoutError should be raised, so this is a fallback.
                return f"Timeout or no result: Dart method for '{data_to_send}' did not respond as expected within {python_timeout_sec}s."
            return result
        except concurrent.futures.TimeoutError:
            return f"Timeout: Dart method for '{data_to_send}' did not respond in {python_timeout_sec}s (Dart task was set to run for {dart_task_duration_ms}ms)."
        except Exception as e:
            # Catch any other unexpected errors during the call
            return f"Error calling Dart method for '{data_to_send}': {e}"

    # enable_periodic_events
    @property
    def enable_periodic_events(self) -> Optional[bool]:
        """
        Controls whether Dart should initiate periodic events.
        """
        return self._get_attr("enablePeriodicEvents", data_type="bool", def_value=False)

    @enable_periodic_events.setter
    def enable_periodic_events(self, value: Optional[bool]):
        self._set_attr("enablePeriodicEvents", value)
        # If events are enabled, we might need to inform Dart.
        # This example assumes Dart checks this attribute on its initState or via a method call if made dynamic.
        # For simplicity, if this is set after initial load, Dart might not react unless it's built to poll or receive an update call.
        # The current Dart implementation in _updatePeriodicTimer checks this attr when it's called (e.g. from initState).
        # If we want to dynamically start/stop, we'd need an invoke_method call here to tell Dart to re-check.
        # For now, this setter primarily makes the attribute available for Dart to read at startup.
        if self.page: # Ensure the control is on a page to send updates
            self.update()


    # on_dart_periodic_event
    @property
    def on_dart_periodic_event(self) -> OptionalControlEventCallable:
        """
        Event handler for Dart-initiated periodic events.
        """
        return self._get_event_handler("dart_periodic_event")

    @on_dart_periodic_event.setter
    def on_dart_periodic_event(self, handler: OptionalControlEventCallable):
        self._add_event_handler("dart_periodic_event", handler)
        if handler is not None and not self.enable_periodic_events:
            # Automatically enable periodic events in Dart if a Python handler is attached
            # and events are not already marked as enabled.
            self.enable_periodic_events = True
        elif handler is None and self.enable_periodic_events:
            # Optional: Disable periodic events if handler is removed
            # self.enable_periodic_events = False
            pass # Current behavior: keep enabled, Dart will send events but Python won't handle.

    def start_task_with_progress_updates(self, total_steps: int, progress_handler: callable, completion_handler: callable):
        """
        Starts a task on the Dart side that will provide periodic progress updates
        and a final completion update.

        :param total_steps: The total number of steps for the task.
        :param progress_handler: A Python callable that will be invoked for each progress update.
                                 It should accept one argument: a dictionary of event data.
        :param completion_handler: A Python callable that will be invoked when the task is complete.
                                   It should accept one argument: a dictionary of event data.
        """
        if not isinstance(total_steps, int) or total_steps <= 0:
            raise ValueError("total_steps must be a positive integer.")
        if not callable(progress_handler):
            raise ValueError("progress_handler must be a callable function.")
        if not callable(completion_handler):
            raise ValueError("completion_handler must be a callable function.")

        task_id = str(uuid.uuid4())
        self._progress_handlers[task_id] = progress_handler
        self._completion_handlers[task_id] = completion_handler

        # We need to ensure total_steps is passed in a way Dart's _onMethodCall can parse.
        # If args are Map<String, String>, then it must be a string.
        # If Flet's invoke_method handles type conversion for basic types, int might be fine.
        # The Dart side currently uses `int.tryParse(args["total_steps"] ?? "0") ?? 0;`
        # which implies it expects a string but can handle it.
        self.invoke_method(
            "start_task_with_progress",
            {"task_id": task_id, "total_steps": str(total_steps)},
        )
        return task_id # Return task_id so UI can track if needed, though example doesn't use it directly for now

    def _on_task_update(self, e):
        """
        Handles 'task_update' events from Dart, routing them to the appropriate
        progress or completion handlers based on the task_id and status.
        """
        try:
            event_data = json.loads(e.data)
        except json.JSONDecodeError:
            # print(f"Error decoding JSON in _on_task_update: {e.data}")
            return

        task_id = event_data.get("task_id")
        status = event_data.get("status")

        if not task_id:
            # print(f"Task ID missing in task_update event: {event_data}")
            return

        if status == "progress":
            handler = self._progress_handlers.get(task_id)
            if handler:
                handler(event_data)
        elif status == "complete":
            handler = self._completion_handlers.get(task_id)
            if handler:
                handler(event_data)
            # Clean up handlers for this task_id after completion or error
            self._progress_handlers.pop(task_id, None)
            self._completion_handlers.pop(task_id, None)
        elif status == "error":
            # Optional: Handle error status if Dart sends it
            # print(f"Task error for {task_id}: {event_data.get('message')}")
            # Clean up handlers for this task_id
            self._progress_handlers.pop(task_id, None)
            self._completion_handlers.pop(task_id, None)
        else:
            # print(f"Unknown status in task_update event: {status} for task {task_id}")
            pass

    def call_dart_that_might_fail(self, should_fail: bool):
        """
        Calls a Dart method that might succeed or return an error.
        Demonstrates handling errors returned by Dart.
        """
        try:
            # Convert boolean to string for Dart method call, as args are Map<String, String>
            result = self.invoke_method(
                "potentially_failing_task",
                {"should_fail": str(should_fail).lower()},
                wait_for_result=True,
                timeout=5.0 # Example timeout
            )
            # Dart is expected to return a dictionary (JSON serialized by Flet)
            if isinstance(result, dict):
                if result.get("success"):
                    return f"Dart task succeeded: {result.get('data')}"
                else:
                    return f"Dart task reported failure: {result.get('error', 'No error message provided.')}"
            elif result is None:
                return "Dart task returned None. This might indicate an issue or an unexpected successful non-response from a method not designed to return structured data."
            else:
                # Fallback for simple string responses, though structured dict is preferred for this pattern
                return f"Dart task returned unexpected type or simple response: {result}"

        except concurrent.futures.TimeoutError:
            return "Timeout: Dart method 'potentially_failing_task' did not respond in time."
        except Exception as e:
            return f"Error calling Dart 'potentially_failing_task': {e}"

    # shared_value
    @property
    def shared_value(self) -> Optional[str]:
        return self._get_attr("shared_value", def_value="Initial Python Value")

    @shared_value.setter
    def shared_value(self, value: Optional[str]):
        self._set_attr("shared_value", value)

    def increment_shared_value_from_python(self):
        current_val_str = self.shared_value
        try:
            parts = current_val_str.split(": ")
            num_part = int(parts[-1]) if len(parts) > 0 and parts[-1].isdigit() else 0
            num_part += 1
            self.shared_value = f"Python Value: {num_part}"
        except ValueError:
            self.shared_value = "Python Value: 1"

    def _on_shared_value_changed_from_dart(self, e):
        new_value_from_dart = e.data
        self.shared_value = new_value_from_dart # Update Python's source of truth for the attribute
        # If there's a specific Python-side public event handler for this, call it
        if self.on_shared_value_changed:
             self.on_shared_value_changed(ft.ControlEvent(target=self.uid, name="shared_value_changed", data=new_value_from_dart, control=self, page=self.page))

    @property
    def on_shared_value_changed(self) -> OptionalControlEventCallable:
        return self._get_event_handler("on_shared_value_changed_by_control")

    @on_shared_value_changed.setter
    def on_shared_value_changed(self, handler: OptionalControlEventCallable):
        self._add_event_handler("on_shared_value_changed_by_control", handler)
        # self._set_attr("has_on_shared_value_changed_handler", True if handler else False) # Inform Dart if needed
