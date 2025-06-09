import 'dart:convert';
import 'dart:math';
import 'package:confetti/confetti.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'utils/shapes.dart';

// SVG Path Parser for Custom Particle Shapes
class SVGPathParser {
  static final Map<String, Path> _pathCache = {};

  static Path? parsePathString(String? pathString) {
    if (pathString == null || pathString.isEmpty) return null;

    // Check cache first for performance
    if (_pathCache.containsKey(pathString)) {
      return _pathCache[pathString]!;
    }

    try {
      final path = _parseSVGPath(pathString);
      _pathCache[pathString] = path;
      return path;
    } catch (e) {
      debugPrint("Error parsing SVG path '$pathString': $e");
      return null;
    }
  }

  static Path _parseSVGPath(String pathString) {
    final path = Path();
    final commands = _tokenizePath(pathString);

    double currentX = 0, currentY = 0;
    double startX = 0, startY = 0;

    for (int i = 0; i < commands.length; i++) {
      final command = commands[i];

      switch (command.toUpperCase()) {
        case 'M': // Move to
          if (i + 2 < commands.length) {
            currentX = double.parse(commands[i + 1]);
            currentY = double.parse(commands[i + 2]);
            startX = currentX;
            startY = currentY;
            path.moveTo(currentX, currentY);
            i += 2;
          }
          break;

        case 'L': // Line to
          if (i + 2 < commands.length) {
            currentX = double.parse(commands[i + 1]);
            currentY = double.parse(commands[i + 2]);
            path.lineTo(currentX, currentY);
            i += 2;
          }
          break;

        case 'H': // Horizontal line
          if (i + 1 < commands.length) {
            currentX = double.parse(commands[i + 1]);
            path.lineTo(currentX, currentY);
            i += 1;
          }
          break;

        case 'V': // Vertical line
          if (i + 1 < commands.length) {
            currentY = double.parse(commands[i + 1]);
            path.lineTo(currentX, currentY);
            i += 1;
          }
          break;

        case 'Q': // Quadratic curve
          if (i + 4 < commands.length) {
            final x1 = double.parse(commands[i + 1]);
            final y1 = double.parse(commands[i + 2]);
            currentX = double.parse(commands[i + 3]);
            currentY = double.parse(commands[i + 4]);
            path.quadraticBezierTo(x1, y1, currentX, currentY);
            i += 4;
          }
          break;

        case 'C': // Cubic curve
          if (i + 6 < commands.length) {
            final x1 = double.parse(commands[i + 1]);
            final y1 = double.parse(commands[i + 2]);
            final x2 = double.parse(commands[i + 3]);
            final y2 = double.parse(commands[i + 4]);
            currentX = double.parse(commands[i + 5]);
            currentY = double.parse(commands[i + 6]);
            path.cubicTo(x1, y1, x2, y2, currentX, currentY);
            i += 6;
          }
          break;

        case 'Z': // Close path
          path.close();
          currentX = startX;
          currentY = startY;
          break;
      }
    }

    return path;
  }

  static List<String> _tokenizePath(String pathString) {
    // Simple tokenizer for SVG path commands
    final tokens = <String>[];
    final buffer = StringBuffer();

    for (int i = 0; i < pathString.length; i++) {
      final char = pathString[i];

      if ('MLHVQCZmlhvqcz'.contains(char)) {
        // Command character
        if (buffer.isNotEmpty) {
          tokens.add(buffer.toString().trim());
          buffer.clear();
        }
        tokens.add(char);
      } else if (char == ',' || char == ' ') {
        // Separator
        if (buffer.isNotEmpty) {
          tokens.add(buffer.toString().trim());
          buffer.clear();
        }
      } else {
        // Number or decimal point
        buffer.write(char);
      }
    }

    if (buffer.isNotEmpty) {
      tokens.add(buffer.toString().trim());
    }

    return tokens.where((token) => token.isNotEmpty).toList();
  }

  static void clearCache() {
    _pathCache.clear();
  }
}

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
    final double emissionFrequency =
        widget.control.attrDouble("emission_frequency", 0.02)!;
    final int numberOfParticles =
        widget.control.attrInt("number_of_particles", 10)!;
    final double maxBlastForce =
        widget.control.attrDouble("max_blast_force", 20.0)!;
    final double minBlastForce =
        widget.control.attrDouble("min_blast_force", 5.0)!;
    final String blastDirectionalityStr =
        widget.control.attrString("blast_directionality", "directional")!;
    final double blastDirection =
        widget.control.attrDouble("blast_direction", pi)!;
    final double gravity = widget.control.attrDouble("gravity", 0.2)!;
    final bool shouldLoop = widget.control.attrBool("should_loop", false)!;
    final bool displayTarget =
        widget.control.attrBool("display_target", false)!;
    final String? strokeColorStr =
        widget.control.attrString("stroke_color", "black");
    final double strokeWidth = widget.control.attrDouble("stroke_width", 0.0)!;

    // Parse Size objects directly from JSON - simplified approach
    Size minimumSize = const Size(20.0, 10.0); // default
    final String? minSizeJson = widget.control.attrString("minimum_size", null);
    if (minSizeJson != null && minSizeJson != "null") {
      try {
        final Map<String, dynamic> parsed = json.decode(minSizeJson);
        minimumSize = Size(
          parsed['width']?.toDouble() ?? 20.0,
          parsed['height']?.toDouble() ?? 10.0,
        );
        debugPrint(
            "FletConfetti: Parsed minimum_size: ${minimumSize.width}x${minimumSize.height}");
      } catch (e) {
        debugPrint("Error parsing minimum_size: $e");
      }
    }

    Size maximumSize = const Size(30.0, 15.0); // default
    final String? maxSizeJson = widget.control.attrString("maximum_size", null);
    if (maxSizeJson != null && maxSizeJson != "null") {
      try {
        final Map<String, dynamic> parsed = json.decode(maxSizeJson);
        maximumSize = Size(
          parsed['width']?.toDouble() ?? 30.0,
          parsed['height']?.toDouble() ?? 15.0,
        );
        debugPrint(
            "FletConfetti: Parsed maximum_size: ${maximumSize.width}x${maximumSize.height}");
      } catch (e) {
        debugPrint("Error parsing maximum_size: $e");
      }
    }

    // Validate size constraints and provide helpful debug info
    if (minimumSize.width > maximumSize.width ||
        minimumSize.height > maximumSize.height) {
      debugPrint(
          "FletConfetti: WARNING - minimumSize (${minimumSize.width}x${minimumSize.height}) is larger than maximumSize (${maximumSize.width}x${maximumSize.height}). This may cause unexpected behavior.");
    }

    if (minimumSize == maximumSize) {
      debugPrint(
          "FletConfetti: INFO - minimumSize and maximumSize are identical (${minimumSize.width}x${minimumSize.height}). All particles will be the same size with no variation.");
    }

    debugPrint(
        "FletConfetti: Final size range: ${minimumSize.width}x${minimumSize.height} to ${maximumSize.width}x${maximumSize.height}");

    Size? canvasSize;
    final String? canvasSizeJson =
        widget.control.attrString("canvas_size", null);
    if (canvasSizeJson != null && canvasSizeJson != "null") {
      try {
        final Map<String, dynamic> parsed = json.decode(canvasSizeJson);
        canvasSize = Size(
          parsed['width']?.toDouble() ?? 400.0,
          parsed['height']?.toDouble() ?? 300.0,
        );
      } catch (e) {
        debugPrint("Error parsing canvas_size: $e");
      }
    }

    final double particleDrag =
        widget.control.attrDouble("particle_drag", 0.05)!;
    final bool pauseEmissionOnLowFrameRate =
        widget.control.attrBool("pause_emission_on_low_frame_rate", true)!;
    final String? createParticlePathStr =
        widget.control.attrString("create_particle_path", null);
    final String? particleShapeStr =
        widget.control.attrString("particle_shape", null);
    final String? customParticlePathStr =
        widget.control.attrString("custom_particle_path", null);

    // Parse colors - themes are converted to colors in Python
    final String? colorListJs = widget.control.attrString("colors", null);

    // Enhanced debugging
    debugPrint("=== CONFETTI SIZE DEBUG ===");
    debugPrint("Raw minimum_size JSON: $minSizeJson");
    debugPrint("Raw maximum_size JSON: $maxSizeJson");
    debugPrint("Raw canvas_size JSON: $canvasSizeJson");
    debugPrint("Final minimumSize: $minimumSize");
    debugPrint("Final maximumSize: $maximumSize");
    debugPrint("Final canvasSize: $canvasSize");
    debugPrint("=== CONFETTI COLOR DEBUG ===");
    debugPrint("colorListJs: $colorListJs");

    List<Color> colors = [
      Colors.red,
      Colors.blue,
      Colors.green,
      Colors.orange,
      Colors.purple
    ];

    if (colorListJs != null &&
        colorListJs.isNotEmpty &&
        colorListJs != "null") {
      // Parse colors (includes both explicit colors and theme colors from Python)
      try {
        final List<dynamic> colorStrings = json.decode(colorListJs);
        colors = parseColors(Theme.of(context), colorStrings);
        debugPrint(
            "✅ Using colors: ${colorStrings.length} colors - $colorStrings");
      } catch (e) {
        debugPrint("❌ Error parsing colors: $e");
        debugPrint("Raw colorListJs: '$colorListJs'");
      }
    } else {
      debugPrint("ℹ️ No colors specified, using default colors");
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
      strokeColor =
          parseColor(Theme.of(context), strokeColorStr) ?? Colors.black;
    }

    // Create particle path function using new shape system
    Path Function(Size)? createParticlePath;

    // Priority: custom_particle_path > particle_shape > create_particle_path (deprecated)
    if (customParticlePathStr != null && customParticlePathStr.isNotEmpty) {
      // Use custom SVG path
      final customPath = SVGPathParser.parsePathString(customParticlePathStr);
      if (customPath != null) {
        createParticlePath = (Size size) {
          // Scale the custom path to fit the particle size
          final pathBounds = customPath.getBounds();
          final scaleX = size.width / pathBounds.width;
          final scaleY = size.height / pathBounds.height;

          final scaledPath = customPath
              .transform(Matrix4.diagonal3Values(scaleX, scaleY, 1.0).storage);

          // Center the path
          final offsetX = (size.width - pathBounds.width * scaleX) / 2;
          final offsetY = (size.height - pathBounds.height * scaleY) / 2;
          final centeredPath = scaledPath.shift(Offset(offsetX, offsetY));

          return centeredPath;
        };
        debugPrint(
            "Using custom SVG path: ${customParticlePathStr.substring(0, min(50, customParticlePathStr.length))}...");
      } else {
        debugPrint(
            "Failed to parse custom SVG path, falling back to predefined shapes");
      }
    }

    // If no custom path or parsing failed, use predefined shapes
    if (createParticlePath == null) {
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
    }

    // Use parsed canvas size directly
    Size? canvas = canvasSize;

    // Debug: Verify sizes being passed to ConfettiWidget
    debugPrint(
        "FletConfetti: Creating ConfettiWidget with minimumSize: ${minimumSize.width}x${minimumSize.height}, maximumSize: ${maximumSize.width}x${maximumSize.height}");

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
      minimumSize: minimumSize,
      maximumSize: maximumSize,
      particleDrag: particleDrag,
      canvas: canvas,
      pauseEmissionOnLowFrameRate: pauseEmissionOnLowFrameRate,
      createParticlePath: createParticlePath,
    );

    return constrainedControl(
        context, confettiWidget, widget.parent, widget.control);
  }
}
