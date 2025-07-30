# Flet Extension Development Guide

This guide covers the basic setup for developing Flet extensions with Flutter packages.

## Initial Setup

### 1. Create Virtual Environment
```bash
uv venv
.venv\Scripts\activate
uv pip install "flet[all]" --upgrade
```

### 2. Generate Extension Template
```bash
uv run flet create --template extension --project-name flet-extension
```

## Configuration

### 3. Fix Path Dependencies
In `examples\flet_extension_example\pyproject.toml`, replace all single backslashes `\` with double backslashes `\\`:

```toml
[tool.poetry.dependencies]
flet-extension = { path = "..\\..\\", editable = true }

[tool.poetry.group.dev.dependencies]
flet = {extras = ["all"], version = "0.28.3"}
flet-extension = {path = "..\\..\\", develop = true}
```

**Important**: This path fix is required for successful builds.

## Adding Flutter Packages

### 4. Install Flutter Dependencies
Navigate to the Flutter extension directory and add packages:

```bash
cd src\flutter\flet_extension
flutter pub add pro_image_editor  # or any package from pub.dev
```

## Development Workflow

### 5. Main Development Files
- **Dart**: `src\flutter\flet_extension\lib\src\flet_extension.dart`
- **Python**: `src\flet_extension\flet_extension.py`

### 6. Testing Changes
- **Dart changes**: Require `flet build` to see effects
- **Python changes**: Use `uv pip install .` (sufficient for testing)

## Building and Running

### 7. Build Process
From the example directory:
```bash
cd examples\flet_extension_example
uv run --active flet build windows -v
```

**Note**: `--active` prevents creating unnecessary `.venv` in the example folder.

### 8. Running the Extension
```bash
uv run --active flet run
```
Run from the example directory where `pyproject.toml` is located.

## Troubleshooting

### 9. Build Issues
If builds fail without apparent errors in Python or Dart code:
1. Delete all `build` folders
2. Delete all `.egg` folders  
3. Rebuild the extension

**Note**: Built extensions only work on the target platform they were built for.

## Environment Notes
- Always use the base `.venv` environment
- The extension template provides a working foundation for Flutter package integration
- Path corrections are critical for Windows development

# Flutter to Flet Extension Development Guide

This guide explains how to create custom Flet extensions that integrate Flutter packages, covering data parsing, control types, parameters, and implementation patterns.

## Table of Contents

1. [Control Types](#control-types)
2. [Data Parsing and Communication](#data-parsing-and-communication)
3. [Property Implementation Patterns](#property-implementation-patterns)
4. [Event Handling](#event-handling)
5. [Method Invocation](#method-invocation)
6. [Advanced Communication Patterns](#advanced-communication-patterns)
7. [Implementation Examples](#implementation-examples)

## Control Types

### Visual Controls (ConstrainedControl)

For controls that render visual widgets, inherit from `ConstrainedControl`:

```python
from flet.core.constrained_control import ConstrainedControl

class MyVisualControl(ConstrainedControl):
    def __init__(self, 
                 # ConstrainedControl properties
                 left: OptionalNumber = None,
                 top: OptionalNumber = None,
                 right: OptionalNumber = None,
                 bottom: OptionalNumber = None,
                 # Custom properties
                 my_property: Optional[str] = None):
        ConstrainedControl.__init__(self, left=left, top=top, right=right, bottom=bottom)
        self.my_property = my_property
    
    def _get_control_name(self):
        return "my_visual_control"  # Must match Dart implementation
```

**Dart Side:**
```dart
// Use constrainedControl() wrapper
return constrainedControl(context, myWidget, widget.parent, widget.control);
```

### Non-Visual Controls (Control)

For controls that don't render widgets (services, data providers):

```python
from flet.core.control import Control

class MyServiceControl(Control):
    def __init__(self, service_config: Optional[str] = None):
        Control.__init__(self)
        self.service_config = service_config
    
    def _get_control_name(self):
        return "my_service_control"
```

**Dart Side:**
```dart
// Use baseControl() wrapper
return baseControl(context, widget.parent, widget.control);
```

## Data Parsing and Communication

### Basic Data Types

#### Strings
```python
# Python
@property
def my_string(self) -> Optional[str]:
    return self._get_attr("my_string")

@my_string.setter
def my_string(self, value: Optional[str]):
    self._set_attr("my_string", value)
```

```dart
// Dart
final String? myString = widget.control.attrString("my_string", null);
```

#### Numbers
```python
# Python
@property
def my_number(self) -> OptionalNumber:
    return self._get_attr("my_number", data_type="float")

@my_number.setter
def my_number(self, value: OptionalNumber):
    self._set_attr("my_number", value)
```

```dart
// Dart
final double? myNumber = widget.control.attrDouble("my_number", null);
```

#### Booleans
```python
# Python
@property
def my_bool(self) -> Optional[bool]:
    return self._get_attr("my_bool", data_type="bool", def_value=False)

@my_bool.setter
def my_bool(self, value: Optional[bool]):
    self._set_attr("my_bool", value)
```

```dart
// Dart
final bool myBool = widget.control.attrBool("my_bool", false) ?? false;
```

#### Individual Colors with Enums
```python
# Python - Single color properties
@property
def base_color(self) -> Optional[ColorValue]:
    """Get the base color for the effect."""
    return self.__base_color

@base_color.setter
def base_color(self, value: Optional[ColorValue]):
    self.__base_color = value
    self._set_enum_attr("base_color", value, ColorEnums)

@property
def highlight_color(self) -> Optional[ColorValue]:
    """Get the highlight color for the effect."""
    return self.__highlight_color

@highlight_color.setter
def highlight_color(self, value: Optional[ColorValue]):
    self.__highlight_color = value
    self._set_enum_attr("highlight_color", value, ColorEnums)
```

```dart
// Dart - Parse individual colors
Color baseColor = widget.control.attrColor("base_color", context) ?? Colors.grey.shade300;
Color highlightColor = widget.control.attrColor("highlight_color", context) ?? Colors.grey.shade100;
```

#### Duration Objects
```python
# Python - Duration property with validation
@property
def period(self) -> Optional[Duration]:
    """Get or set the animation period."""
    return self.__period

@period.setter
def period(self, value: Optional[Duration]):
    if value is not None:
        # Calculate total microseconds to check minimum duration
        total_microseconds = (
            value.microseconds
            + value.milliseconds * 1000
            + value.seconds * 1000000
            + value.minutes * 60 * 1000000
            + value.hours * 60 * 60 * 1000000
            + value.days * 24 * 60 * 60 * 1000000
        )
        
        if total_microseconds < 1:
            raise ValueError("Period duration must be at least 1 microsecond")
        
        self.__period = value
        self._set_attr_json(
            "duration",
            {
                "microseconds": value.microseconds,
                "milliseconds": value.milliseconds,
                "seconds": value.seconds,
                "minutes": value.minutes,
                "hours": value.hours,
                "days": value.days,
            },
        )
    else:
        self.__period = None
        self._set_attr_json("duration", None)
```

```dart
// Dart - Parse duration from JSON using built-in function
final Duration duration = parseDuration(widget.control, "duration") ?? Duration(milliseconds: 1500);
```

### Complex Data Types

#### Lists and JSON Data
```python
# Python - Colors List
@property
def colors(self) -> Optional[List[ColorValue]]:
    return self._get_attr("colors")

@colors.setter
def colors(self, value: Optional[List[ColorValue]]):
    self._set_attr_json("colors", value)  # Use _set_attr_json for complex data
```

```dart
// Dart - Parse JSON list using built-in function
List<Color> colors = parseColors(Theme.of(context), widget.control, "colors") ?? 
    [Colors.red, Colors.blue, Colors.green]; // default
```

#### Complex JSON Objects
```python
# Python
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
```

```dart
// Dart
final String? complexDataJson = widget.control.attrString("complex_data", null);
Map<String, dynamic>? complexData;
if (complexDataJson != null) {
  try {
    complexData = json.decode(complexDataJson);
  } catch (e) {
    complexData = {"error": "Invalid JSON"};
  }
}
```

## Property Implementation Patterns

### Child Controls
```python
# Python - Single child control
@property
def content(self) -> Optional[Control]:
    return self.__content

@content.setter
def content(self, value: Optional[Control]):
    self.__content = value

def _get_children(self):
    children = []
    if self.__content is not None:
        self.__content._set_attr_internal("n", "content")  # Set name identifier
        children.append(self.__content)
    return children
```

```dart
// Dart - Find and create child widget
var contentCtrls = widget.children.where((c) => c.name == "content" && c.isVisible);
bool? adaptive = widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
bool disabled = widget.control.isDisabled || widget.parentDisabled;

Widget? childWidget;
if (contentCtrls.isNotEmpty) {
  childWidget = createControl(
    widget.control, 
    contentCtrls.first.id, 
    disabled,
    parentAdaptive: adaptive
  );
}
```

## Event Handling

### Basic Events
```python
# Python
@property
def on_something(self) -> OptionalControlEventCallable:
    return self._get_event_handler("on_something")

@on_something.setter
def on_something(self, handler: OptionalControlEventCallable):
    self._add_event_handler("on_something", handler)
```

```dart
// Dart - Trigger event
void handleSomething(dynamic value) {
  String newValue = value.toString();
  var props = {"value": newValue};
  
  // Update control state
  widget.backend.updateControlState(widget.control.id, props);
  
  // Trigger Python event handler
  widget.backend.triggerControlEvent(widget.control.id, "on_something", newValue);
}
```

### Advanced Event Patterns
```python
# Python - Event with JSON data
def _on_task_update(self, e):
    try:
        event_data = json.loads(e.data)
        task_id = event_data.get("task_id")
        status = event_data.get("status")
        
        if status == "progress":
            handler = self._progress_handlers.get(task_id)
            if handler:
                handler(event_data)
    except json.JSONDecodeError:
        pass
```

```dart
// Dart - Send structured event data
widget.backend.triggerControlEvent(
  widget.control.id,
  "task_update",
  json.encode({
    "task_id": taskId,
    "status": "progress",
    "current_step": i,
    "total_steps": totalSteps
  })
);
```

## Method Invocation

### Python to Dart Method Calls
```python
# Python - Simple method call
def play(self, some: str = "thing"):
    args = {"some": some}
    return self.invoke_method("play", args, wait_for_result=True)

# Python - Async method call
def async_operation_with_callback(self, message: str, python_callback: callable):
    callback_id = str(uuid.uuid4())
    self._async_callbacks[callback_id] = python_callback
    self.invoke_method(
        "start_async_task", 
        {"message": message, "callback_id": callback_id}
    )
```

```dart
// Dart - Method handler
Future<String?> _onMethodCall(String methodName, Map<String, String> args) async {
  switch (methodName) {
    case "play":
      return "you call play" + args["some"]!;
    
    case "start_async_task":
      final String message = args["message"] ?? "No message";
      final String callbackId = args["callback_id"] ?? "";
      start_async_task(message, callbackId);
      return null; // Async operation, no immediate result
    
    default:
      return null;
  }
}
```

### Method Registration
```dart
// Dart - Register method handler in initState
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
```

## Advanced Communication Patterns

### Timeout Handling
```python
# Python - Method call with timeout
def call_dart_with_timeout(self, data: str, timeout_sec: float, duration_ms: int):
    try:
        result = self.invoke_method(
            "long_running_task",
            {"data": data, "duration_ms": duration_ms},
            wait_for_result=True
        )
        return result
    except concurrent.futures.TimeoutError:
        return f"Timeout: Method did not respond in {timeout_sec}s"
    except Exception as e:
        return f"Error: {e}"
```

### Periodic Events from Dart
```python
# Python - Enable periodic events
@property
def enable_periodic_events(self) -> Optional[bool]:
    return self._get_attr("enablePeriodicEvents", data_type="bool", def_value=False)

@enable_periodic_events.setter
def enable_periodic_events(self, value: Optional[bool]):
    self._set_attr("enablePeriodicEvents", value)
    if self.page:
        self.update()
```

```dart
// Dart - Periodic timer
void _updatePeriodicTimer() {
  _periodicTimer?.cancel();
  if (widget.control.attrBool("enablePeriodicEvents", false) ?? false) {
    _periodicTimer = Timer.periodic(const Duration(seconds: 1), (Timer timer) {
      _periodicCounter++;
      widget.backend.triggerControlEvent(
        widget.control.id,
        "dart_periodic_event",
        json.encode({"counter": _periodicCounter})
      );
    });
  }
}
```

## Implementation Examples

### Complete Control Example

**Python (flet_package_guide.py):**
```python
class FletPackageGuide(ConstrainedControl):
    def __init__(self,
                 colors: Optional[List[ColorValue]] = None,
                 content: Optional[Control] = None,
                 on_something: OptionalControlEventCallable = None,
                 complex_data: Optional[Any] = None):
        ConstrainedControl.__init__(self)
        self.colors = colors
        self.content = content
        self.on_something = on_something
        self.complex_data = complex_data
    
    def _get_control_name(self):
        return "flet_package_guide"
```

**Dart (flet_package_guide.dart):**
```dart
class FletPackageGuideControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  @override
  Widget build(BuildContext context) {
    // Parse properties
    final String? colorListJs = widget.control.attrString("colors", null);
    List<Color> colors = [Colors.red, Colors.blue, Colors.green];
    colors = parseColors(Theme.of(context), widget.control, "colors") ?? colors;
    }
    
    // Build widget
    Widget myControl = Column(
      children: colors.map((color) => Container(
        width: 50,
        height: 50,
        color: color,
      )).toList(),
    );
    
    return constrainedControl(context, myControl, widget.parent, widget.control);
  }
}
```

**Usage (main.py):**
```python
import flet as ft
from flet_package_guide import FletPackageGuide

def main(page: ft.Page):
    package = FletPackageGuide(
        colors=[ft.Colors.RED, ft.Colors.BLUE, ft.Colors.PRIMARY],
        content=ft.Icon(ft.Icons.ABC),
        on_something=lambda e: print(e.data),
        complex_data={"hello": "world", "count": 42}
    )
    
    page.add(package)

ft.app(main)
```

## Key Takeaways

1. **Control Name Matching**: The `_get_control_name()` in Python must match the Dart implementation
2. **Data Serialization**: Use `_set_attr_json()` for complex data, `_set_attr()` for simple types
3. **Event Handling**: Register events with `_add_event_handler()` in Python, trigger with `triggerControlEvent()` in Dart
4. **Method Calls**: Use `invoke_method()` for Python-to-Dart calls, implement `_onMethodCall()` in Dart
5. **Child Controls**: Use `_get_children()` and `createControl()` for nested widgets
6. **State Management**: Use StatefulWidget in Dart for controls that need internal state
7. **Error Handling**: Always include try-catch blocks for JSON parsing and method calls

This guide provides the foundation for creating robust Flutter-to-Flet extensions with proper data flow and communication patterns.
