import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart'; // Import the package
import 'dart:convert';

class UrlLauncherControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const UrlLauncherControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<UrlLauncherControl> createState() => _UrlLauncherControlState();
}

class _UrlLauncherControlState extends State<UrlLauncherControl> {
  String _status = "Awaiting URL to launch...";

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

  Future<String?> _onMethodCall(
      String methodName, Map<String, String> args) async {
    switch (methodName) {
      case "launch_url":
        final String? url = args["url"];
        if (url == null || url.isEmpty) {
          setState(() {
            _status = "Error: URL is null or empty.";
          });
          return "Error: URL is null or empty."; // Return error message to Python
        }
        try {
          // launchUrlString returns a bool. We need to convert it to string for Python.
          // Flet's invoke_method in Python expects a string result or throws error.
          bool success = await launchUrlString(url);
          if (success) {
             setState(() {
               _status = "Successfully launched $url";
             });
             return "true"; // Return "true" for success
          } else {
             setState(() {
               _status = "Failed to launch $url (launchUrlString returned false)";
             });
             return "false"; // Return "false" for known failure
          }
        } catch (e) {
          setState(() {
            _status = "Error launching $url: ${e.toString()}";
          });
          return "Error launching $url: ${e.toString()}"; // Return detailed error
        }
      default:
        return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    // This control is primarily functional, UI is minimal.
    // It could display the status if desired.
    return Container(
      padding: const EdgeInsets.all(8.0),
      child: Text(_status, style: const TextStyle(color: Colors.black)),
    );
    // We don't need to use constrainedControl if it's a simple non-visual helper
    // or if its visual representation is very basic like this Text.
    // For more complex UI, use constrainedControl.
  }
}
