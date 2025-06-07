# Comprehensive Guide to Integrating Flutter Packages with Flet

This guide provides a comprehensive overview of how to create Flet custom controls by wrapping existing Flutter packages or by building custom Flutter widgets. It covers everything from basic setup and core communication principles to advanced interaction patterns and real-world examples.

Whether you want to bring the power of a specific Flutter package into your Python Flet application or develop unique UI components, this guide aims to equip you with the necessary knowledge.

## Core Concepts for Flet Custom Controls

Understanding these fundamental concepts is key to successfully bridging Python Flet and Flutter.

### 1. Architecture Overview
Flet custom controls allow you to extend Flet's capabilities with Flutter widgets. This involves two main parts:
- **Python side:** A Python class that inherits from `flet.Control` (or a more specialized Flet control class). This class defines the properties and methods your Flet app will interact with.
- **Dart (Flutter) side:** A Flutter widget that implements the actual UI and logic. Flet handles the communication channel between your Python code and the Dart widget.

Communication typically involves:
- Python sending property updates to Dart.
- Python invoking methods on the Dart control.
- Dart sending events back to Python.

### 2. Development Environment Setup
To create custom Flet controls, you'll need:
- Python and Flet installed.
- Flutter SDK installed.
- An IDE like Visual Studio Code with extensions for Python and Flutter can be very helpful.
Refer to the official [Flet documentation](https://flet.dev/docs/guides/python/custom-controls/) and [Flutter documentation](https://flutter.dev/docs/get-started/install) for detailed setup instructions.

### 3. Project Structure
A typical Flet custom control project involves:
- **Python package:** Contains your Python control logic (e.g., `my_control.py`).
- **Flutter module:** A standard Flutter module within your Python package (often in a `src/flutter` or similar directory). This module contains:
    - `pubspec.yaml`: Defines Flutter package dependencies.
    - `lib/`: Contains your Dart code for the Flutter widget.
Your main Flet application's `pyproject.toml` will then depend on your Python package.

Add dependency to `pyproject.toml` of your Flet app:

* **Git dependency**

Link to git repository:

```
dependencies = [
  "flet-package-guide @ git+https://github.com/MyGithubAccount/flet-package-guide", # Or your custom control package
  "flet>=0.28.3",
]
```

* **PyPi dependency**  

If the package is published on pypi.org:

```
dependencies = [
  "flet-package-guide", # Or your custom control package
  "flet>=0.28.3",
]
```

Build your app (example):
```
flet build macos -v
```

### 4. Attributes: Defining and Accessing Properties
Attributes (properties) are how you configure your custom control from Python and how the Dart widget reads its configuration.

**Python side (e.g., in `your_control.py`):**
Use standard Python properties with setters that call `self._set_attr("attribute_name", value)` and getters that call `self._get_attr("attribute_name")`. Flet handles serializing these to Dart.

```python
from flet import Control

class MyCustomControl(Control):
    def __init__(self, text=None):
        super().__init__()
        self.text = text

    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value) # Automatically calls self.update() if value changes
```

**Dart side (e.g., in `your_control_widget.dart`):**
Access attributes from the `widget.control` object:
```dart
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class MyCustomControlWidget extends StatelessWidget {
  final Control control;

  const MyCustomControlWidget({Key? key, required this.control}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    String text = control.attrString("text", "Default Text")!; // Accessing the 'text' attribute
    return Text(text);
  }
}
```
Common attribute accessors in Dart include `attrString()`, `attrBool()`, `attrInt()`, `attrDouble()`.

### 5. Handling Data Types
- **Simple Types:** Basic types like strings, booleans, numbers are passed directly.
- **Complex Data (Lists, Dictionaries):** For complex data structures like lists or dictionaries, serialize them to a JSON string in Python before sending and deserialize in Dart.
    - Python: `self._set_attr_json("my_complex_data", {"key": "value", "items": [1, 2, 3]})`
    - Dart: `String? jsonData = control.attrString("my_complex_data"); if (jsonData != null) { var data = json.decode(jsonData); }`
    The `FletPackageGuide` control demonstrates this with its `complex_data` property.

### 6. Python Calling Dart Methods
You can define methods in your Dart widget that can be called from Python.

**Python side:**
Use `self.invoke_method("method_name", {"arg1": "value1"}, wait_for_result=False)` for fire-and-forget, or `wait_for_result=True` to get a synchronous result (blocks Python until Dart returns).
```python
# In your Python control class
def do_something_in_dart(self, message):
    self.invoke_method("doSomething", {"message": message})

def get_data_from_dart(self, param):
    return self.invoke_method("getData", {"param": param}, wait_for_result=True)
```

**Dart side:**
Subscribe to method calls in your widget's `State` class.
```dart
// In your Dart widget's State class
@override
void initState() {
  super.initState();
  widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
}

@override
void dispose() {
  widget.backend.unsubscribeMethods(widget.control.id);
  super.dispose();
}

Future<String?> _onMethodCall(String methodName, Map<String, String> args) async {
  switch (methodName) {
    case "doSomething":
      // Handle the method call, args["message"] contains the data
      debugPrint("Dart received doSomething: ${args['message']}");
      break;
    case "getData":
      String param = args["param"] ?? "";
      return "Data from Dart for $param"; // This string is returned to Python
  }
  return null; // Default response or for methods not returning a value
}
```

### 7. Dart Sending Events to Python
Dart can send events (with optional data) back to Python, for example, on user interaction.

**Dart side:**
Use `widget.backend.triggerControlEvent(widget.control.id, "event_name", "optional_data_string")`.
```dart
// Example: In a GestureDetector onTap callback in your Dart widget
onTap: () {
  widget.backend.triggerControlEvent(widget.control.id, "my_event", "Button clicked!");
}
```

**Python side:**
Register an event handler in your Python control's `__init__` method or via a property.
```python
# In your Python control class
def __init__(self, on_my_event=None):
    super().__init__()
    self.on_my_event = on_my_event # Using a property
    # Alternatively, using _add_event_handler directly:
    # self._add_event_handler("my_event", self._internal_event_handler)

@property
def on_my_event(self):
    return self._get_event_handler("my_event")

@on_my_event.setter
def on_my_event(self, handler):
    self._add_event_handler("my_event", handler)
    # Optional: self._set_attr("hasMyEventHandler", True if handler else False) to inform Dart

# If using a direct internal handler:
# def _internal_event_handler(self, e):
#     print(f"Internal handler received: {e.data}")
#     # If you also have a public property, you might call it:
#     # if self.on_my_event:
#     #     self.on_my_event(e)
```
When `on_my_event` is set in the Flet app, the provided callable will be invoked when Dart triggers the "my_event" event. The event object `e` will have an `e.data` attribute containing the string sent from Dart.

## Advanced Communication Examples

This section details several patterns for more complex interactions between Python and Dart within your Flet custom control. For full implementation details and context, please refer to:
- Example usage: `package-guide/examples/flet_package_guide_example/src/main.py`
- Python control logic: `package-guide/src/flet_package_guide/flet_package_guide.py`
- Dart control logic: `package-guide/src/flutter/flet_package_guide/lib/src/flet_package_guide.dart`

### 1. Asynchronous Operation with Callback

- **Purpose:** Demonstrates how Python can call a Dart function and receive a response asynchronously via a callback, without blocking the main Python thread.
- **Mechanism:**
    - Python (`FletPackageGuide`): `async_operation_with_callback(message, python_callback)` method initiates the call using `invoke_method` (where `wait_for_result` defaults to `False`). It passes a unique `callback_id` and the `message`. The `python_callback` is stored in a dictionary, keyed by this `callback_id`.
    - Dart (`_FletPackageGuideControlState`): `start_async_task(message, callbackId)` method (invoked by Python) simulates asynchronous work (e.g., using `Future.delayed`). Upon completion, it uses `triggerControlEvent` to send an event (e.g., `"async_callback"`) back to Python, including the original `callbackId` and the result data.
    - Python: An event handler (`_on_async_callback`) receives this event, uses the `callbackId` from the event data to look up the original `python_callback` from the dictionary, and then executes it with the data from Dart.
- **Pitfalls/Notes:**
    - Ensure the `callback_id` is unique for concurrent operations. `uuid.uuid4()` is a good choice.
    - Error handling for the Dart async operation itself should be implemented within the Dart code. The Python callback receives the result (success or error data) that Dart sends.
- **Example Snippet (from `main.py`):**
  ```python
  def my_async_handler(data_from_dart):
      print(f"Async result from Dart: {data_from_dart}")

  # In your Flet app setup:
  # my_package = FletPackageGuide(...) # Assuming 'my_package' is your control instance
  # my_package.async_operation_with_callback("Hello from Python!", my_async_handler)
  ```

### 2. Calling Dart with Timeout Handling

- **Purpose:** Shows how Python can call a Dart method and handle potential timeouts if Dart doesn't respond within a specified duration.
- **Mechanism:**
    - Python (`FletPackageGuide`): `call_dart_with_timeout(data_to_send, python_timeout_sec, dart_task_duration_ms)` method uses Flet's `invoke_method(..., wait_for_result=True, timeout=python_timeout_sec)`.
    - It passes `dart_task_duration_ms` to Dart to control the simulated work time.
    - If `invoke_method` raises `concurrent.futures.TimeoutError` (the specific exception for this scenario), it's caught, and a timeout message is returned. Otherwise, Dart's response is returned.
    - Dart (`_FletPackageGuideControlState`): `long_running_task(data, duration_ms)` simulates work for `duration_ms`.
- **Pitfalls/Notes:**
    - The `timeout` in `invoke_method` is a Python-side timeout. Dart code is not automatically interrupted. Design your Dart method to respect the expected duration or handle its own timeouts if it involves long native operations.
    - If the Dart method completes successfully but after the Python timeout, its result is lost to that specific `invoke_method` call.
- **Example Snippet (from `main.py`):**
  ```python
  # In your Flet app setup:
  # my_package = FletPackageGuide(...)
  # result = my_package.call_dart_with_timeout(
  #     data_to_send="Process me",
  #     python_timeout_sec=2.0,  # Python waits for 2s
  #     dart_task_duration_ms=1000 # Dart task takes 1s (should succeed)
  # )
  # print(f"Dart call result: {result}")

  # result_timeout = my_package.call_dart_with_timeout(
  #     data_to_send="Process me slowly",
  #     python_timeout_sec=1.0,  # Python waits for 1s
  #     dart_task_duration_ms=2000 # Dart task takes 2s (should timeout)
  # )
  # print(f"Dart call result (timeout expected): {result_timeout}")
  ```

### 3. Dart-Initiated Periodic Events

- **Purpose:** Illustrates how the Dart side of a control can autonomously send events to Python periodically (e.g., for live updates).
- **Mechanism:**
    - Python (`FletPackageGuide`): Has an `enable_periodic_events` boolean attribute (property) and an `on_dart_periodic_event` event handler property. Setting the event handler in Python typically also sets `enable_periodic_events` to true, signaling Dart to start.
    - Dart (`_FletPackageGuideControlState`): If the `enablePeriodicEvents` attribute is true (often checked in `initState` or `didUpdateWidget`), a `Timer.periodic` is started (commonly in `initState` or a dedicated setup method if the enabling can change). This timer uses `triggerControlEvent` to send an event (e.g., `"dart_periodic_event"`) with data (like a counter) to Python at regular intervals.
    - Crucially, the timer must be cancelled in Dart's `dispose` method to prevent errors and resource leaks when the widget is removed.
- **Pitfalls/Notes:**
    - If `enable_periodic_events` is set from Python after the Dart widget is initialized, Dart might not pick up the change unless it's explicitly coded to listen for attribute updates that re-evaluate the timer (e.g., in `didUpdateWidget` or by calling a specific method from Python to refresh the timer state). The current example primarily relies on `initState`.
    - Excessive frequency of periodic events can impact performance. Choose a sensible interval.
- **Example Snippet (from `main.py`):**
  ```python
  # periodic_update_text = ft.Text("Waiting...") # Defined in your UI

  # def handle_periodic_updates(e):
  #     # Assuming 'page' is your ft.Page instance and 'json' is imported
  #     data = json.loads(e.data)
  #     periodic_update_text.value = f"Dart says: {data['counter']}"
  #     page.update()

  # In your Flet app setup:
  # my_package = FletPackageGuide()
  # my_package.on_dart_periodic_event = handle_periodic_updates
  # page.add(periodic_update_text, my_package) # Add relevant controls to page
  ```

### 4. Task with Progress Updates

- **Purpose:** Demonstrates managing a longer task initiated by Python on the Dart side, where Dart provides multiple progress updates before completion.
- **Mechanism:**
    - Python (`FletPackageGuide`): `start_task_with_progress_updates(total_steps, progress_handler, completion_handler)` method generates a unique `task_id`, stores the `progress_handler` and `completion_handler` (typically in dictionaries keyed by `task_id`), and then calls a Dart method using `invoke_method` to start the task, passing the `task_id`.
    - Dart (`_FletPackageGuideControlState`): `start_task_with_progress(taskId, totalSteps)` simulates a multi-step task. For each progress step, it uses `triggerControlEvent` to send a `"task_update"` event with `status: "progress"`, the `taskId`, and current step details. Upon finalization (completion or error), it sends another `"task_update"` event with `status: "complete"` or `status: "error"`, including the `taskId`.
    - Python: A generic event handler (`_on_task_update`) receives these events. It uses the `taskId` from the event data to retrieve the correct `progress_handler` or `completion_handler` and executes it with the event data.
- **Pitfalls/Notes:**
    - Ensure proper cleanup of handlers (e.g., removing them from the dictionaries) in Python once a task is complete or errors out to prevent memory leaks.
    - Consider what happens if the user navigates away or the control is destroyed mid-task. Implement cancellation mechanisms if necessary (this example doesn't explicitly show task cancellation logic, which would typically involve Python sending another message to Dart, and Dart stopping the task and cleaning up).
- **Example Snippet (from `main.py`):**
  ```python
  # progress_display = ft.Text("Progress...") # Defined in your UI
  # status_display = ft.Text("Status: Idle")   # Defined in your UI

  # def show_progress(data):
  #     # Assuming 'page' is your ft.Page instance
  #     progress_display.value = f"Step {data['current_step']}/{data['total_steps']}"
  #     page.update()

  # def show_completion(data):
  #     # Assuming 'page' is your ft.Page instance
  #     status_display.value = f"Task {data['task_id'][:8]}: {data['message']}"
  #     progress_display.value = ""
  #     page.update()

  # In your Flet app setup:
  # my_package = FletPackageGuide(...)
  # To call from a button click or other action:
  # my_package.start_task_with_progress_updates(
  #     total_steps=10,
  #     progress_handler=show_progress,
  #     completion_handler=show_completion
  # )
  ```

### 5. Robust Error Handling from Dart

- **Purpose:** Demonstrates how Python can invoke a Dart method that might fail, and how Dart can return structured error information to Python. This is crucial for building robust controls.
- **Mechanism:**
    - Python (`FletPackageGuide`): A method like `call_dart_that_might_fail(should_fail: bool)` uses `invoke_method(..., wait_for_result=True)`.
    - The Python method includes `try...except` blocks to catch:
        - `concurrent.futures.TimeoutError` for timeouts.
        - General `Exception` for other communication issues or platform exceptions forwarded by Flet.
    - Dart (`_FletPackageGuideControlState`): The corresponding Dart method (e.g., `potentially_failing_task(shouldFail)`) returns a `Future<Map<String, dynamic>>`. This map indicates success or failure. Flet handles the JSON serialization of this map to a string when sending it to Python, and Flet on the Python side deserializes it back into a Python `dict`. For example:
        - Success: `{"success": true, "data": "some result"}`
        - Failure: `{"success": false, "error": "description of error"}`
    - Python then inspects this dictionary to determine the outcome.
- **Example Snippet (Python - in `FletPackageGuide`):**
  ```python
  def call_dart_that_might_fail(self, should_fail: bool):
      try:
          result = self.invoke_method(
              "potentially_failing_task",
              {"should_fail": str(should_fail).lower()}, # Pass bool as string
              wait_for_result=True,
              timeout=5.0
          )
          if isinstance(result, dict):
              if result.get("success"):
                  return f"Dart task succeeded: {result.get('data')}"
              else:
                  return f"Dart task reported failure: {result.get('error')}"
          return f"Unexpected result structure from Dart: {result}"
      except concurrent.futures.TimeoutError:
          return "Timeout: Dart method 'potentially_failing_task' did not respond."
      except Exception as e:
          return f"Error calling Dart 'potentially_failing_task': {e}"
  ```
- **Example Snippet (Dart - in `_FletPackageGuideControlState`):**
  ```dart
  // In _onMethodCall:
  // case "potentially_failing_task":
  //   final bool shouldFail = (args["should_fail"] ?? "false") == "true";
  //   return await potentially_failing_task(shouldFail); // Result is Map<String, dynamic>

  Future<Map<String, dynamic>> potentially_failing_task(bool shouldFail) async {
    await Future.delayed(const Duration(seconds: 1)); // Simulate work
    if (shouldFail) {
      return {"success": false, "error": "Simulated error from Dart."};
    } else {
      return {"success": true, "data": "Successfully processed in Dart."};
    }
  }
  ```
- **Example Snippet (from `main.py`):**
  ```python
  # error_handling_success_text = ft.Text(...)
  # error_handling_failure_text = ft.Text(...)
  # package = FletPackageGuide(...) # instance of your control
  # # page = ft.Page(...) # instance of the page, usually passed to main

  # def test_dart_success(e):
  #     result = package.call_dart_that_might_fail(should_fail=False)
  #     error_handling_success_text.value = str(result)
  #     error_handling_success_text.update() # or page.update()

  # def test_dart_failure(e):
  #     result = package.call_dart_that_might_fail(should_fail=True)
  #     error_handling_failure_text.value = str(result)
  #     error_handling_failure_text.update() # or page.update()

  # # In page.add(...):
  # #   ft.ElevatedButton("Call Dart (Expect Success)", on_click=test_dart_success),
  # #   error_handling_success_text,
  # #   ft.ElevatedButton("Call Dart (Expect Failure)", on_click=test_dart_failure),
  # #   error_handling_failure_text,
  ```
- **Pitfalls/Notes:**
    - "Always define a clear contract for the structure of the success/error response from Dart (e.g., always include a 'success' boolean field and 'data' or 'error' fields)."
    - "Ensure proper JSON serialization/deserialization if passing complex error objects. Flet handles Map<String, dynamic> from Dart to Python dict automatically when `wait_for_result=True`."
    - "Arguments from Python to Dart's `_onMethodCall` are `Map<String, String>`. Convert non-string types (like booleans) to strings in Python (e.g., `str(should_fail).lower()`) and parse them appropriately in Dart (e.g., `(args["should_fail"] ?? "false") == "true"`)."
    - "Consider logging raw responses on both sides during development to debug issues with data structures or serialization."

### 6. Bi-directional Update of Shared Data

- **Purpose:** Illustrates how a piece of data can be modified by either Python or Dart, with the other side reflecting the change. This is useful for state that needs to be synchronized and interactively modified from both ends.
- **Mechanism:**
    - **Python Side (`FletPackageGuide`):**
        - A property (e.g., `shared_value`) is defined using `_get_attr` and `_set_attr`. Setting this property automatically triggers an update to the Dart side.
        - A method (e.g., `increment_shared_value_from_python()`) allows Python logic to modify this property.
        - An internal event handler (e.g., `_on_shared_value_changed_from_dart`) is registered for an event like `"shared_value_changed_from_dart"`. When Dart sends this event, this handler updates the Python property `shared_value`.
        - Optionally, a public event handler property (e.g., `on_shared_value_changed`) can be exposed for the Flet app user to react to changes originating from Dart.
    - **Dart Side (`_FletPackageGuideControlState`):**
        - The Dart widget reads the `shared_value` using `widget.control.attrString('shared_value')` in its `build` method to display it.
        - A UI element in Dart (e.g., an `ElevatedButton`) allows the user to modify the value.
        - When this Dart UI element is interacted with, a Dart method (e.g., `_incrementSharedValueFromDart()`) calculates the new value and then uses `widget.backend.triggerControlEvent(widget.control.id, "shared_value_changed_from_dart", new_value_string)` to send the new value to Python.
    - **Flow:**
        1. Python changes `shared_value` -> `_set_attr` -> Dart UI updates on next `build` because `attrString` gets new value.
        2. Dart button clicked -> Dart method -> `triggerControlEvent` -> Python's `_on_shared_value_changed_from_dart` -> Python sets `shared_value` -> `_set_attr` -> Dart UI updates (if not already updated by Dart itself).
- **Example Snippet (Python - in `FletPackageGuide`):**
  ```python
  # Property
  @property
  def shared_value(self): return self._get_attr("shared_value", "Init Val")
  @shared_value.setter
  def shared_value(self, value): self._set_attr("shared_value", value)

  # Method to change from Python
  def increment_shared_value_from_python(self):
      try:
          parts = self.shared_value.split(": ")
          num_part = int(parts[-1]) if len(parts) > 0 and parts[-1].isdigit() else 0
          num_part += 1
          self.shared_value = f"Python Value: {num_part}"
      except ValueError:
          self.shared_value = "Python Value: 1" # Or handle error appropriately

  # Internal handler for Dart's event
  def _on_shared_value_changed_from_dart(self, e):
      self.shared_value = e.data # Update Python's source of truth
      # Optionally call a public event handler if defined:
      # if self.on_shared_value_changed: self.on_shared_value_changed(e)

  # In __init__:
  # self._add_event_handler("shared_value_changed_from_dart", self._on_shared_value_changed_from_dart)
  ```
- **Example Snippet (Dart - in `_FletPackageGuideControlState`):**
  ```dart
  // In build method:
  // Text("Shared Value: ${widget.control.attrString('shared_value', 'N/A')}"),
  // ElevatedButton(onPressed: _incrementSharedValueFromDart, child: const Text("Increment from Dart")),

  void _incrementSharedValueFromDart() {
    String currentValue = widget.control.attrString("shared_value", "Init Val")!;
    int newValueNum = (int.tryParse(currentValue.split(": ").last) ?? 0) + 1;
    String newSharedValue = "Dart Value: $newValueNum";
    widget.backend.triggerControlEvent(
      widget.control.id,
      "shared_value_changed_from_dart",
      newSharedValue
    );
  }
  ```
- **Example Snippet (from `main.py`):**
  ```python
  # shared_value_display_text = ft.Text(f"Shared Value: {package.shared_value}")
  # def increment_from_python_button_click(e):
  #     package.increment_shared_value_from_python()
  #     shared_value_display_text.value = f"Shared Value: {package.shared_value}"
  #     shared_value_display_text.update()

  # # Optional: if you have a public on_shared_value_changed handler on the control
  # # def handle_change_from_dart(e):
  # #     shared_value_display_text.value = f"Shared Value (event): {e.data}"
  # #     shared_value_display_text.update()
  # # package.on_shared_value_changed = handle_change_from_dart

  # # In page.add(...):
  # #   shared_value_display_text,
  # #   ft.ElevatedButton("Increment from Python", on_click=increment_from_python_button_click),
  ```
- **Pitfalls/Notes:**
    - "Careful state management is needed to avoid infinite loops. For instance, if Python's `_set_attr` for `shared_value` itself triggered an event that Dart listened to and reacted by sending *another* `shared_value_changed_from_dart` event." (The current example avoids this by Dart primarily reading attributes for display and only sending events on direct user interaction in Dart).
    - "Decide which side (Python or Dart) is the ultimate source of truth if there are conflicts, or implement a conflict resolution strategy."
    - "Parsing logic (like `split(': ')` and `int.tryParse`) should be robust to handle unexpected formats of the shared string."

## 7. Wrapping Existing Flutter Packages: A Conceptual Guide & Example

One of the most powerful features of Flet custom controls is the ability to wrap existing Flutter packages, bringing their native capabilities and rich UIs into your Python applications.

### Conceptual Steps:

1.  **Identify the Flutter Package:** Find a package on [pub.dev](https://pub.dev/) that you want to use. Understand its main widgets, APIs, and how it's typically used in a Flutter app.
2.  **Add Dependency:** Add the Flutter package to the `pubspec.yaml` file of your Flet custom control's Flutter module (e.g., `src/flutter/your_control_name/pubspec.yaml`). Run `flutter pub get` in that directory.
3.  **Design Python Interface:** Decide how you want to interact with this package from Python.
    *   What properties will your Flet control have? These will map to the Flutter widget's properties.
    *   What methods will your Flet control expose? These will call methods on the Flutter package's objects or your Dart wrapper logic.
4.  **Implement Dart Wrapper:**
    *   Create a new Dart file for your custom control's widget (e.g., `my_flutter_package_wrapper.dart`).
    *   Import the target Flutter package.
    *   In your `StatefulWidget`'s `State` class:
        *   Use `widget.control.attrString()`, `attrBool()`, etc., in the `build` method to get values from Python and configure the wrapped Flutter widget.
        *   If you need to call methods on the Flutter package, subscribe to method calls from Python using `widget.backend.subscribeMethods()` and implement `_onMethodCall` to delegate to the package's API.
        *   If the Flutter package has callbacks (e.g., `onPressed`, `onChanged`), implement these in Dart and use `widget.backend.triggerControlEvent()` to send results or notifications back to Python.
5.  **Implement Python Control:**
    *   Create the Python class for your Flet control.
    *   Define properties using `@property` and `_get_attr`/`_set_attr`.
    *   Define methods that use `self.invoke_method()` to call your Dart wrapper logic.
    *   Use `self._add_event_handler()` to handle events triggered from Dart.
6.  **Expose and Use:**
    *   Ensure your new Python control is exported from your package's `__init__.py`.
    *   In your Flet app, import and use your new custom control.

### Example: Wrapping `url_launcher`

Let's create a Flet control that uses the popular `url_launcher` package to open URLs.

**1. Add Dependency to `src/flutter/flet_package_guide/pubspec.yaml`:**
```yaml
dependencies:
  flutter:
    sdk: flutter
  flet: # ... existing flet dependency
  url_launcher: ^6.2.1 # Check for the latest version
```
*(Remember to run `flutter pub get` in that directory after editing.)*

**2. Python Control (`src/flet_package_guide/url_launcher_control.py`):**
```python
from typing import Optional
from flet import Control
import concurrent.futures

class UrlLauncherControl(Control):
    def __init__(self, data: any = None): # Simplified for README
        Control.__init__(self, data=data)
        self._last_result = None

    def _get_control_name(self):
        return "url_launcher_control"

    def launch_url(self, url: str) -> bool:
        if not url: self._last_result = "Error: URL cannot be empty."; return False
        try:
            result_str = self.invoke_method("launch_url", {"url": url}, wait_for_result=True, timeout=10.0)
            if result_str == "true": self._last_result = f"Launched {url}"; return True
            self._last_result = f"Failed: {result_str or 'Dart returned no specific error'}"; return False
        except Exception as e: self._last_result = f"Error: {e}"; return False

    @property
    def last_result(self) -> Optional[str]: # For display in example app
        return self._last_result
```

**3. Dart Wrapper (`src/flutter/flet_package_guide/lib/src/url_launcher_control.dart`):**
```dart
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class UrlLauncherControl extends StatefulWidget {
  final Control? parent; final Control control; final List<Control> children;
  final bool parentDisabled; final bool? parentAdaptive; final FletControlBackend backend;
  const UrlLauncherControl({super.key, this.parent, required this.control, required this.children, required this.parentDisabled, this.parentAdaptive, required this.backend});
  @override State<UrlLauncherControl> createState() => _UrlLauncherControlState();
}

class _UrlLauncherControlState extends State<UrlLauncherControl> {
  String _status = "URL Launcher Ready";
  @override void initState() { super.initState(); widget.backend.subscribeMethods(widget.control.id, _onMethodCall); }
  @override void dispose() { widget.backend.unsubscribeMethods(widget.control.id); super.dispose(); }

  Future<String?> _onMethodCall(String methodName, Map<String, String> args) async {
    if (methodName == "launch_url") {
      final String? url = args["url"];
      if (url == null || url.isEmpty) return "Error: URL is null or empty.";
      try {
        bool success = await launchUrlString(url);
        setState(() {_status = success ? "Launched $url" : "Failed to launch $url";});
        return success ? "true" : "false";
      } catch (e) { setState(() {_status = "Error: ${e.toString()}";}); return "Error: ${e.toString()}"; }
    }
    return null;
  }
  @override Widget build(BuildContext context) {
    // UI is optional, this control is mainly functional.
    return Container(padding: const EdgeInsets.all(8.0), child: Text(_status));
  }
}
```
*(Note: Ensure the Flutter project that uses this control (`flet_package_guide`) has the necessary platform configurations if `url_launcher` requires them, e.g., for iOS query schemes or Android manifest entries. This is beyond Flet's direct scope but important for Flutter plugin usage.)*

**4. Expose in `src/flet_package_guide/__init__.py`:**
```python
# ... (existing imports)
from .url_launcher_control import UrlLauncherControl
__all__ = [ /* ... existing names ... */ UrlLauncherControl.__name__ ]
```

**5. Usage in Flet App (`main.py`):**
```python
# import flet as ft
# from flet_package_guide import UrlLauncherControl # Assuming it's in your package

# def main(page: ft.Page):
#     # ...
#     url_input = ft.TextField(label="Enter URL", value="https://flet.dev")
#     url_launcher_status = ft.Text("URL Launcher status will appear here.")
#     launcher_control = UrlLauncherControl() # Create an instance

#     def do_launch_url(e):
#         if not url_input.value:
#             url_launcher_status.value = "Please enter a URL."
#             url_launcher_status.update()
#             return
#         launcher_control.launch_url(url_input.value)
#         # The control's internal _last_result is not directly bound to UI here.
#         # We rely on the UI in the Dart side or a separate status text.
#         # For a better UX, the launch_url method could update a Text control passed to it,
#         # or the UrlLauncherControl could have its own on_launch_result event.
#         # For this example, we'll add a button to fetch the last result manually.
#         url_launcher_status.value = launcher_control.last_result or "No result yet."
#         url_launcher_status.update()


#     def refresh_launcher_status(e):
#          url_launcher_status.value = launcher_control.last_result or "No result yet."
#          url_launcher_status.update()

#     page.add(
#         ft.Text("URL Launcher Example:"),
#         launcher_control, # Add the control itself to the page (displays Dart UI)
#         url_input,
#         ft.ElevatedButton("Launch URL", on_click=do_launch_url),
#         url_launcher_status,
#         ft.ElevatedButton("Refresh Last Launch Result", on_click=refresh_launcher_status)
#     )
#     # ...
```
This example provides a basic Flet control for `url_launcher`. More complex packages might require more elaborate attribute mapping, event handling, and Dart UI construction.

## Troubleshooting / Common Pitfalls

Here are some common issues and tips for debugging your Flet custom controls:

- **Verbose Build Logs:** When building your Flet app (`flet build -v ...`), the `-v` (verbose) flag provides detailed logs from both the Flet build process and the Flutter compilation. These logs are invaluable for diagnosing build errors, Flutter plugin issues, or Dart compilation problems.
- **Browser Developer Tools (for Flet Web):** If your Flet app runs in the browser, use the browser's developer tools (Console, Network tabs) to check for JavaScript errors, WebSocket communication issues, or failed asset loading.
- **Dart DevTools:** For more in-depth debugging of the Dart side of your control, you can connect Flutter DevTools. This is more advanced but useful for inspecting widget trees, performance, and logging within Dart. (Refer to Flutter documentation for DevTools usage).
- **Unique IDs for Callbacks/Tasks:** When managing multiple asynchronous operations or tasks, ensure that any IDs you generate (e.g., for `async_operation_with_callback` or `start_task_with_progress_updates`) are truly unique to avoid misdirecting callbacks or updates. `uuid.uuid4()` is recommended.
- **Python-Side Timeouts:** Remember that the `timeout` parameter in `invoke_method(..., wait_for_result=True, timeout=X)` is a Python-side timeout. The Dart code is not automatically interrupted. Design Dart methods accordingly.
- **Data Serialization:**
    - Python to Dart: Arguments in `invoke_method` (the `args` map in Dart's `_onMethodCall`) are `Map<String, String>`. Convert Python types like booleans or numbers to strings if not already, and parse them in Dart. For complex data, use `_set_attr_json` or manually `json.dumps` for event data, and `json.decode` in Dart.
    - Dart to Python: When Dart returns a result for `invoke_method(..., wait_for_result=True)`, Flet handles JSON serialization for basic Dart types and `Map<String, dynamic>` (to Python `dict`). For events via `triggerControlEvent`, the data payload is a string; use JSON for complex data.
- **Hot Reload Limitations:** While Flet's hot reload is powerful for Python UI code, changes to the Dart side of custom controls typically require a full rebuild of the Flet app (`flet build ...` or restarting `flet run`) to take effect.
- **Platform-Specific Configurations:** If your wrapped Flutter package requires platform-specific setup (e.g., `Info.plist` for iOS, `AndroidManifest.xml` for Android, web-specific configurations), these must be done within the Flutter module of your custom control (e.g., in `src/flutter/your_control_name/ios/Runner/Info.plist`).
- **Check Control Names:** Ensure the string returned by `_get_control_name()` in Python matches the name used when registering the control on the Dart side (typically the class name of the Dart widget).

## Contributing

Contributions to this guide and the example package are welcome! If you find any issues, have suggestions for improvements, or want to add more examples, please feel free to:

1.  Open an issue on the project's repository.
2.  Fork the repository and submit a pull request with your changes.

Clear explanations, working code examples, and adherence to the existing style are appreciated.
