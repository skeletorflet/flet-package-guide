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

  @override
  void initState() {
    super.initState();
    widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
    final String? complexDataJson =
        widget.control.attrString("complex_data", null);
    if (complexDataJson != null) {
      try {
        complexData = json.decode(complexDataJson);
      } catch (e) {
        complexData = {"error": "Invalid JSON"};
      }
    }
  }

  @override
  void dispose() {
    widget.backend.unsubscribeMethods(widget.control.id);
    super.dispose();
  }

  Future<String?> _onMethodCall(
      String methodName, Map<String, String> args) async {
    switch (methodName) {
      case "play":
        return "you call play" + args["some"]!;
      case "stop":
        return "you call stop" + args["love"]!;
      default:
        return null;
    }
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
      ],
    );

    return constrainedControl(
        context, myControl, widget.parent, widget.control);
  }
}
