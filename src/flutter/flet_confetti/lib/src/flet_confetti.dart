import 'dart:convert';
import 'dart:math';
import 'package:confetti/confetti.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

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

  @override
  void initState() {
    super.initState();
    _confettiController = ConfettiController(
      duration: const Duration(seconds: 10),
    );
    
    // Listen for animation end
    _confettiController.addListener(() {
      if (!_confettiController.state.isPlaying) {
        widget.backend.triggerControlEvent(
          widget.control.id, 
          "on_animation_end", 
          "ended"
        );
      }
    });
  }

  @override
  void dispose() {
    _confettiController.dispose();
    super.dispose();
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
    
    // Parse colors
    final String? colorListJs = widget.control.attrString("colors", null);
    List<Color> colors = [Colors.red, Colors.blue, Colors.green, Colors.orange, Colors.purple];
    if (colorListJs != null) {
      try {
        final List<dynamic> colorStrings = json.decode(colorListJs);
        colors = parseColors(Theme.of(context), colorStrings);
      } catch (e) {
        debugPrint("Error parsing colors: $e");
      }
    }
    
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
    
    // Create particle path function
    Path Function(Size)? createParticlePath;
    if (createParticlePathStr == "star") {
      createParticlePath = drawStar;
    }
    
    // Create canvas size
    Size? canvas;
    if (canvasWidth != null && canvasHeight != null) {
      canvas = Size(canvasWidth, canvasHeight);
    }
    
    // Register method call handler
    widget.control.onMethodCall = (String method, Map<String, dynamic> args) {
      switch (method) {
        case "play":
          _confettiController.play();
          break;
        case "stop":
          _confettiController.stop();
          break;
      }
    };
    
    Widget confettiWidget = ConfettiWidget(
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
