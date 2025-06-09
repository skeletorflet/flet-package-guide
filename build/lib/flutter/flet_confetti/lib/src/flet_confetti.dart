import 'dart:convert';
import 'dart:math';
import 'package:confetti/confetti.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'utils/shapes.dart';
import 'utils/themes.dart';

class FletConfettiControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const FletConfettiControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<FletConfettiControl> createState() => _FletConfettiControlState();
}

class _FletConfettiControlState extends State<FletConfettiControl> {
  late ConfettiController _confettiController;
  int _controllerVersion = 0; // Track controller recreations

  @override
  void initState() {
    super.initState();
    _initializeConfettiController();
    widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
  }

  @override
  void didUpdateWidget(covariant FletConfettiControl oldWidget) {
    super.didUpdateWidget(oldWidget);

    // Check if critical parameters have changed that require controller reconstruction
    final bool needsReconstruction = _needsControllerReconstruction(oldWidget);

    if (needsReconstruction) {
      debugPrint(
          "Critical confetti parameters changed, reconstructing controller...");
      _confettiController.dispose();
      _initializeConfettiController();
    } else {
      debugPrint(
          "Confetti widget updated but controller reconstruction not needed");
    }
  }

  bool _needsControllerReconstruction(FletConfettiControl oldWidget) {
    // Check if duration changed
    final oldDuration = oldWidget.control.attrInt("duration_seconds", 10);
    final newDuration = widget.control.attrInt("duration_seconds", 10);

    if (oldDuration != newDuration) {
      debugPrint("Duration changed from $oldDuration to $newDuration");
      return true;
    }

    // Check if should_loop changed (affects controller behavior)
    final oldShouldLoop = oldWidget.control.attrBool("should_loop", false);
    final newShouldLoop = widget.control.attrBool("should_loop", false);

    if (oldShouldLoop != newShouldLoop) {
      debugPrint("Should loop changed from $oldShouldLoop to $newShouldLoop");
      return true;
    }

    // For other parameters, we don't need to reconstruct the controller
    // as they are applied in the build method to the ConfettiWidget
    return false;
  }

  @override
  void dispose() {
    widget.backend.unsubscribeMethods(widget.control.id);
    _confettiController.dispose();
    super.dispose();
  }

  void _initializeConfettiController() {
    try {
      // Get duration from control attributes or use default
      final int durationSeconds =
          widget.control.attrInt("duration_seconds", 10)!;

      _confettiController = ConfettiController(
        duration: Duration(seconds: durationSeconds),
      );

      // Increment version to track recreations
      _controllerVersion++;

      debugPrint(
          "ConfettiController initialized with duration: ${durationSeconds}s (version: $_controllerVersion)");

      // Listen for animation end
      _confettiController.addListener(() {
        if (mounted &&
            _confettiController.state == ConfettiControllerState.stopped) {
          debugPrint("Confetti animation ended, triggering event");
          widget.backend.triggerControlEvent(
              widget.control.id, "on_animation_end", "ended");
        }
      });
    } catch (e) {
      debugPrint("Error initializing ConfettiController: $e");
      // Fallback initialization
      _confettiController = ConfettiController(
        duration: const Duration(seconds: 10),
      );
      _controllerVersion++;
    }
  }

  Future<String?> _onMethodCall(String method, Map<String, String> args) async {
    try {
      debugPrint("ConfettiController _onMethodCall: $method with args: $args");

      switch (method) {
        case "play":
          // Ensure controller is in a good state before playing
          if (_confettiController.state == ConfettiControllerState.disposed) {
            debugPrint("Controller was disposed, reinitializing...");
            _initializeConfettiController();
            // Force widget rebuild to use the new controller
            if (mounted) {
              setState(() {
                // This will trigger a rebuild with the new controller
              });
            }
          }
          _confettiController.play();
          debugPrint("Confetti play() called successfully");
          return "play_started";

        case "stop":
          // Parse clearAllParticles parameter (default: false)
          final bool clearAllParticles =
              args["clear_all_particles"]?.toLowerCase() == "true";
          _confettiController.stop(clearAllParticles: clearAllParticles);
          debugPrint(
              "Confetti stop() called with clearAllParticles: $clearAllParticles");
          return "stop_called";

        case "reload":
        case "reset":
          // Completely reinitialize the controller and rebuild widget
          debugPrint("Reloading confetti controller...");
          _confettiController.dispose();
          _initializeConfettiController();
          // Force immediate rebuild - the ValueKey will ensure ConfettiWidget is recreated
          if (mounted) {
            setState(() {
              debugPrint(
                  "Widget rebuilt after reload - controller version: $_controllerVersion");
            });
          }
          return "controller_reloaded";

        case "get_state":
          // Return current controller state for debugging
          final state = _confettiController.state.toString();
          debugPrint("Current controller state: $state");
          return state;

        default:
          debugPrint("Unknown method: $method");
          return null;
      }
    } catch (e) {
      debugPrint("Error in _onMethodCall: $e");
      // Try to recover by reinitializing the controller
      try {
        _confettiController.dispose();
        _initializeConfettiController();
        // Force widget rebuild after recovery
        if (mounted) {
          setState(() {
            // This will trigger a rebuild with the new controller
          });
        }
        return "error_recovered";
      } catch (recoveryError) {
        debugPrint("Failed to recover: $recoveryError");
        return "error_failed_to_recover";
      }
    }
  }

  /// Custom Path to paint stars (from confetti.md example)
  Path drawStar(Size size) {
    double degToRad(double deg) => deg * (pi / 180.0);

    const numberOfPoints = 5;
    final halfWidth = size.width / 2;
    final externalRadius = halfWidth;
    final internalRadius = halfWidth / 2.5;
    final degreesPerStep = degToRad(360 / numberOfPoints);
    final halfDegreesPerStep = degreesPerStep / 2;
    final path = Path();
    final fullAngle = degToRad(360);
    path.moveTo(size.width, halfWidth);

    for (double step = 0; step < fullAngle; step += degreesPerStep) {
      path.lineTo(halfWidth + externalRadius * cos(step),
          halfWidth + externalRadius * sin(step));
      path.lineTo(halfWidth + internalRadius * cos(step + halfDegreesPerStep),
          halfWidth + internalRadius * sin(step + halfDegreesPerStep));
    }
    path.close();
    return path;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FletConfettiControl build: ${widget.control.id}");

    // Ensure controller is in a valid state before building
    if (_confettiController.state == ConfettiControllerState.disposed) {
      debugPrint("Controller is disposed during build, reinitializing...");
      _initializeConfettiController();
    }

    // Get all parameters from control attributes
    final double emissionFrequency = widget.control.attrDouble("emission_frequency", 0.02)!;
    final int numberOfParticles = widget.control.attrInt("number_of_particles", 10)!;
    final double maxBlastForce = widget.control.attrDouble("max_blast_force", 20.0)!;
    final double minBlastForce = widget.control.attrDouble("min_blast_force", 5.0)!;
    final String blastDirectionalityStr = widget.control.attrString("blast_directionality", "directional")!;
    final double blastDirection = widget.control.attrDouble("blast_direction", pi)!;
    final double gravity = widget.control.attrDouble("gravity", 0.2)!;
    final bool shouldLoop = widget.control.attrBool("should_loop", false)!;
    final bool displayTarget = widget.control.attrBool("display_target", false)!;
    final String? strokeColorStr = widget.control.attrString("stroke_color", "black");
    final double strokeWidth = widget.control.attrDouble("stroke_width", 0.0)!;
    final double minimumSizeWidth = widget.control.attrDouble("minimum_size_width", 20.0)!;
    final double minimumSizeHeight = widget.control.attrDouble("minimum_size_height", 10.0)!;
    final double maximumSizeWidth = widget.control.attrDouble("maximum_size_width", 30.0)!;
    final double maximumSizeHeight = widget.control.attrDouble("maximum_size_height", 15.0)!;
    final double particleDrag = widget.control.attrDouble("particle_drag", 0.05)!;
    final double? canvasWidth = widget.control.attrDouble("canvas_width", null);
    final double? canvasHeight = widget.control.attrDouble("canvas_height", null);
    final bool pauseEmissionOnLowFrameRate = widget.control.attrBool("pause_emission_on_low_frame_rate", true)!;
    final String? createParticlePathStr = widget.control.attrString("create_particle_path", null);
    final String? particleShapeStr =
        widget.control.attrString("particle_shape", null);

    // Parse colors - check for explicit colors first, then theme
    final String? colorListJs = widget.control.attrString("colors", null);
    final String? themeStr = widget.control.attrString("theme", null);

    // Enhanced debugging
    debugPrint("=== CONFETTI COLOR DEBUG ===");
    debugPrint("colorListJs: $colorListJs");
    debugPrint("themeStr: $themeStr");

    List<Color> colors = [Colors.red, Colors.blue, Colors.green, Colors.orange, Colors.purple];

    if (colorListJs != null &&
        colorListJs.isNotEmpty &&
        colorListJs != "null") {
      // Explicit colors have priority
      try {
        final List<dynamic> colorStrings = json.decode(colorListJs);
        colors = parseColors(Theme.of(context), colorStrings);
        debugPrint(
            "✅ Using explicit colors: ${colorStrings.length} colors - $colorStrings");
      } catch (e) {
        debugPrint("❌ Error parsing colors: $e");
        debugPrint("Raw colorListJs: '$colorListJs'");
      }
    } else if (themeStr != null && themeStr.isNotEmpty && themeStr != "null") {
      // Use theme colors if no explicit colors
      if (ConfettiThemes.isValidTheme(themeStr)) {
        colors = ConfettiThemes.getThemeColors(themeStr);
        debugPrint("✅ Using theme '$themeStr': ${colors.length} colors");
      } else {
        debugPrint("❌ Unknown theme '$themeStr', using default colors");
      }
    } else {
      debugPrint("ℹ️ No colors or theme specified, using default colors");
    }

    debugPrint("Final colors count: ${colors.length}");
    debugPrint("=== END COLOR DEBUG ===");
    
    // Parse blast directionality
    BlastDirectionality blastDirectionality = BlastDirectionality.directional;
    if (blastDirectionalityStr == "explosive") {
      blastDirectionality = BlastDirectionality.explosive;
    }
    
    // Parse stroke color
    Color strokeColor = Colors.black;
    if (strokeColorStr != null) {
      strokeColor = parseColor(Theme.of(context), strokeColorStr) ?? Colors.black;
    }
    
    // Create particle path function using new shape system
    Path Function(Size)? createParticlePath;

    // Priority: particle_shape (new) > create_particle_path (deprecated)
    String? shapeToUse = particleShapeStr ?? createParticlePathStr;

    if (shapeToUse != null) {
      createParticlePath = ParticleShapes.getShapeFunction(shapeToUse);
      debugPrint("Using particle shape: $shapeToUse");
    }

    // Fallback to original star implementation if shape not found
    if (createParticlePath == null && createParticlePathStr == "star") {
      createParticlePath = drawStar;
      debugPrint("Using fallback star implementation");
    }
    
    // Create canvas size
    Size? canvas;
    if (canvasWidth != null && canvasHeight != null) {
      canvas = Size(canvasWidth, canvasHeight);
    }
    

    
    Widget confettiWidget = ConfettiWidget(
      key: ValueKey(
          "confetti_$_controllerVersion"), // Force rebuild when controller changes
      confettiController: _confettiController,
      emissionFrequency: emissionFrequency,
      numberOfParticles: numberOfParticles,
      maxBlastForce: maxBlastForce,
      minBlastForce: minBlastForce,
      blastDirectionality: blastDirectionality,
      blastDirection: blastDirection,
      gravity: gravity,
      shouldLoop: shouldLoop,
      displayTarget: displayTarget,
      colors: colors,
      strokeColor: strokeColor,
      strokeWidth: strokeWidth,
      minimumSize: Size(minimumSizeWidth, minimumSizeHeight),
      maximumSize: Size(maximumSizeWidth, maximumSizeHeight),
      particleDrag: particleDrag,
      canvas: canvas,
      pauseEmissionOnLowFrameRate: pauseEmissionOnLowFrameRate,
      createParticlePath: createParticlePath,
    );

    return constrainedControl(context, confettiWidget, widget.parent, widget.control);
  }
}
