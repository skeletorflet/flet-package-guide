import 'dart:async'; // Import for Timer
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'dart:convert';

class FletPackageGuideControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const FletPackageGuideControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<FletPackageGuideControl> createState() =>
      _FletPackageGuideControlState();
}

class _FletPackageGuideControlState extends State<FletPackageGuideControl> {
  Map<String, dynamic>? complexData;
  Timer? _periodicTimer;
  int _periodicCounter = 0;

  @override
  void initState() {
    super.initState();
    widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
    // Initialize complexData as before
    final String? complexDataJson =
        widget.control.attrString("complex_data", null);
    if (complexDataJson != null) {
      try {
        complexData = json.decode(complexDataJson);
      } catch (e) {
        complexData = {"error": "Invalid JSON"};
      }
    }
    // Start periodic timer if enabled
    _updatePeriodicTimer();
  }

  @override
  void dispose() {
    widget.backend.unsubscribeMethods(widget.control.id);
    _periodicTimer?.cancel(); // Cancel the timer on dispose
    super.dispose();
  }

  void _updatePeriodicTimer() {
    _periodicTimer?.cancel(); // Cancel any existing timer
    if (widget.control.attrBool("enablePeriodicEvents", false) ?? false) {
      debugPrint("Starting Dart periodic timer.");
      _periodicTimer =
          Timer.periodic(const Duration(seconds: 1), (Timer timer) {
        _periodicCounter++;
        // debugPrint("Dart periodic event: Counter = $_periodicCounter");
        widget.backend.triggerControlEvent(
          widget.control.id,
          "dart_periodic_event", // Event name for Python handler
          json.encode({"counter": _periodicCounter}),
        );
      });
    } else {
      debugPrint("Dart periodic timer is disabled or not explicitly enabled.");
    }
  }

  // This method could be called if we were to implement live updates of the `enablePeriodicEvents` attribute
  // For now, it's called from initState.
  // @override
  // void didUpdateWidget(covariant FletPackageGuideControl oldWidget) {
  //   super.didUpdateWidget(oldWidget);
  //   if (widget.control.attrBool("enablePeriodicEvents") !=
  //       oldWidget.control.attrBool("enablePeriodicEvents")) {
  //     _updatePeriodicTimer();
  //   }
  // }

  Future<String?> _onMethodCall(
      String methodName, Map<String, String> args) async {
    switch (methodName) {
      case "play":
        return "you call play" + args["some"]!;
      case "stop":
        return "you call stop" + args["love"]!;
      case "start_async_task":
        // Extract message and callbackId from args
        final String message = args["message"] ?? "No message";
        final String callbackId = args["callback_id"] ?? "";

        if (callbackId.isEmpty) {
          debugPrint("Error: callback_id is missing in start_async_task");
          return "Error: callback_id is missing";
        }
        // Call the async task method
        start_async_task(message, callbackId);
        return null; // Indicate that the method was handled
      case "long_running_task":
        final String data = args["data"] ?? "No data";
        // Default to 0ms if not provided or if parsing fails
        final int durationMs = int.tryParse(args["duration_ms"] ?? "0") ?? 0;
        return long_running_task(data, durationMs);
      case "start_task_with_progress":
        final String taskId = args["task_id"] ?? "";
        final int totalSteps = int.tryParse(args["total_steps"] ?? "0") ?? 0;
        if (taskId.isEmpty || totalSteps <= 0) {
          debugPrint(
              "Error: task_id is missing or total_steps is invalid in start_task_with_progress");
          // Optionally send an error event back
          widget.backend.triggerControlEvent(
              widget.control.id,
              "task_update",
              json.encode({
                "task_id": taskId,
                "status": "error",
                "message": "Invalid parameters for task creation."
              }));
          return null;
        }
        start_task_with_progress(taskId, totalSteps);
        return null; // Indicate method was handled, no direct string result
      case "potentially_failing_task":
        // args from Python are Map<String, String>
        final bool shouldFail = (args["should_fail"] ?? "false") == "true";
        return await potentially_failing_task(shouldFail);
        // Flet will JSON encode the returned Map<String, dynamic>
      default:
        return null;
    }
  }

  void start_async_task(String message, String callbackId) {
    debugPrint(
        "Dart start_async_task called with message: '$message', callbackId: '$callbackId'");
    // Simulate an async operation
    Future.delayed(const Duration(seconds: 2), () {
      String result = "Async task for '$message' completed";
      debugPrint("Dart async task completed. Result: '$result'");
      // Send an event back to Python
      widget.backend.triggerControlEvent(
        widget.control.id,
        "async_callback", // Event name must match Python's event handler
        json.encode({"callback_id": callbackId, "data": result}),
      );
    });
  }

  Future<String?> long_running_task(String data, int durationMs) async {
    debugPrint(
        "Dart long_running_task called with data: '$data', duration_ms: $durationMs");
    // Simulate work using Future.delayed
    await Future.delayed(Duration(milliseconds: durationMs));
    String result = "Task completed for: '$data' after $durationMs ms";
    debugPrint("Dart long_running_task completed. Result: '$result'");
    return result;
  }

  Future<void> start_task_with_progress(String taskId, int totalSteps) async {
    debugPrint(
        "Dart start_task_with_progress called for task ID: $taskId with $totalSteps steps.");

    for (int i = 1; i <= totalSteps; i++) {
      await Future.delayed(
          const Duration(seconds: 1)); // Simulate one second of work per step
      // Send progress update
      // debugPrint("Sending progress for task $taskId, step $i/$totalSteps");
      widget.backend.triggerControlEvent(
          widget.control.id,
          "task_update", // Event name for Python handler
          json.encode({
            "task_id": taskId,
            "status": "progress",
            "current_step": i,
            "total_steps": totalSteps
          }));
    }

    // Send completion event
    // debugPrint("Sending completion for task $taskId");
    widget.backend.triggerControlEvent(
        widget.control.id,
        "task_update", // Event name for Python handler
        json.encode({
          "task_id": taskId,
          "status": "complete",
          "message":
              "Task $taskId finished successfully after $totalSteps steps."
        }));
  }

  Future<Map<String, dynamic>> potentially_failing_task(bool shouldFail) async {
    debugPrint("Dart potentially_failing_task called with shouldFail: $shouldFail");
    await Future.delayed(const Duration(seconds: 1)); // Simulate some work
    if (shouldFail) {
      debugPrint("Dart task is simulating a failure.");
      return {"success": false, "error": "Simulated error from Dart."};
    } else {
      debugPrint("Dart task is simulating success.");
      return {"success": true, "data": "Successfully processed in Dart."};
    }
  }

  void _incrementSharedValueFromDart() {
    String currentValue = widget.control.attrString("shared_value", "Initial Dart Value")!;
    int newValueNum;
    try {
      // Attempt to parse "Python Value: X" or "Dart Value: X"
      List<String> parts = currentValue.split(": ");
      newValueNum = (parts.isNotEmpty && int.tryParse(parts.last) != null) ? int.parse(parts.last) + 1 : 1;
    } catch (e) {
      newValueNum = 1; // Start fresh if parsing fails
    }
    String newSharedValue = "Dart Value: $newValueNum";

    debugPrint("Dart incrementing shared_value to: $newSharedValue");
    widget.backend.triggerControlEvent(
      widget.control.id,
      "shared_value_changed_from_dart", // Event name Python listens to
      newSharedValue // Data for the event
    );
  }

  void handleSomething(dynamic value) {
    String newValue = value.toString();
    debugPrint("Handler triggered: $newValue");
    var props = {"value": newValue};
    widget.backend.updateControlState(widget.control.id, props);
    widget.backend
        .triggerControlEvent(widget.control.id, "on_something", newValue);
  }

  @override
  Widget build(BuildContext context) {
    final String? colorListJs = widget.control.attrString("colors", null);
    List<Color> colors = [Colors.red, Colors.blue, Colors.green];
    if (colorListJs != null) {
      try {
        final List<dynamic> colorStrings = json.decode(colorListJs);
        colors = parseColors(Theme.of(context), colorStrings);
      } catch (e) {}
    }

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Widget? childWidget;
    if (contentCtrls.isNotEmpty) {
      childWidget = createControl(
          widget.control, contentCtrls.first.id, disabled,
          parentAdaptive: adaptive);
    }

    Widget debugText = Text(
      complexData != null ? json.encode(complexData) : "No complex data",
      style: const TextStyle(fontSize: 12, color: Colors.black),
    );

    Widget myControl = Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        debugText,
        ...colors.map((color) => GestureDetector(
              onTap: () => handleSomething(
                  "handled,#${color.toARGB32().toRadixString(16).substring(2).toUpperCase()}"),
              child: Container(
                width: 50,
                height: 50,
                color: color,
                child: childWidget,
              ),
            )),
        const SizedBox(height: 10), // Spacer
        Text("Shared Value: ${widget.control.attrString('shared_value', 'N/A')}"),
        ElevatedButton(
          onPressed: _incrementSharedValueFromDart,
          child: const Text("Increment from Dart"),
        ),
      ],
    );

    return constrainedControl(
        context, myControl, widget.parent, widget.control);
  }
}
