import 'dart:math';
import 'package:flutter/material.dart';

/// Utility class for creating particle shapes for confetti animations.
/// Each method returns a Path that defines the shape of a particle.
class ParticleShapes {
  /// Helper method to convert degrees to radians
  static double degToRad(double deg) => deg * (pi / 180.0);

  /// Parse a shape name string and return the corresponding Path function
  static Path Function(Size)? getShapeFunction(String? shapeName) {
    if (shapeName == null) return null;

    switch (shapeName.toLowerCase()) {
      // Basic shapes
      case "rectangle":
        return drawRectangle;
      case "circle":
        return drawCircle;
      case "square":
        return drawSquare;

      // Geometric shapes
      case "triangle":
        return drawTriangle;
      case "diamond":
        return drawDiamond;
      case "hexagon":
        return drawHexagon;
      case "pentagon":
        return drawPentagon;
      case "octagon":
        return drawOctagon;

      // Star variations
      case "star":
        return drawStar;
      case "star_4":
        return drawStar4;
      case "star_6":
        return drawStar6;
      case "star_8":
        return drawStar8;

      // Fun shapes
      case "heart":
        return drawHeart;
      case "flower":
        return drawFlower;
      case "leaf":
        return drawLeaf;
      case "butterfly":
        return drawButterfly;

      // Symbols
      case "cross":
        return drawCross;
      case "plus":
        return drawPlus;
      case "arrow":
        return drawArrow;
      case "lightning":
        return drawLightning;

      // Special shapes (placeholders for complex paths you'll add)
      case "skull":
        return drawSkull;
      case "crown":
        return drawCrown;
      case "sword":
        return drawSword;
      case "music_note":
        return drawMusicNote;

      default:
        return null;
    }
  }

  // ============================================================================
  // BASIC SHAPES
  // ============================================================================

  /// Default rectangle (same as confetti package default)
  static Path drawRectangle(Size size) {
    final path = Path();
    path.addRect(Rect.fromLTWH(0, 0, size.width, size.height));
    return path;
  }

  /// Perfect circle
  static Path drawCircle(Size size) {
    final path = Path();
    final radius = size.width / 2;
    path.addOval(Rect.fromCircle(
      center: Offset(radius, radius),
      radius: radius,
    ));
    return path;
  }

  /// Perfect square
  static Path drawSquare(Size size) {
    final path = Path();
    final sideLength = size.width < size.height ? size.width : size.height;
    path.addRect(Rect.fromLTWH(0, 0, sideLength, sideLength));
    return path;
  }

  // ============================================================================
  // GEOMETRIC SHAPES
  // ============================================================================

  /// Equilateral triangle
  static Path drawTriangle(Size size) {
    final path = Path();
    final halfWidth = size.width / 2;

    path.moveTo(halfWidth, 0); // Top point
    path.lineTo(0, size.height); // Bottom left
    path.lineTo(size.width, size.height); // Bottom right
    path.close();

    return path;
  }

  /// Diamond shape
  static Path drawDiamond(Size size) {
    final path = Path();
    final halfWidth = size.width / 2;
    final halfHeight = size.height / 2;

    path.moveTo(halfWidth, 0); // Top
    path.lineTo(size.width, halfHeight); // Right
    path.lineTo(halfWidth, size.height); // Bottom
    path.lineTo(0, halfHeight); // Left
    path.close();

    return path;
  }

  /// Regular hexagon
  static Path drawHexagon(Size size) {
    return _drawRegularPolygon(size, 6);
  }

  /// Regular pentagon
  static Path drawPentagon(Size size) {
    return _drawRegularPolygon(size, 5);
  }

  /// Regular octagon
  static Path drawOctagon(Size size) {
    return _drawRegularPolygon(size, 8);
  }

  /// Helper method to draw regular polygons
  static Path _drawRegularPolygon(Size size, int sides) {
    final path = Path();
    final centerX = size.width / 2;
    final centerY = size.height / 2;
    final radius = centerX < centerY ? centerX : centerY;
    final angleStep = 2 * pi / sides;

    for (int i = 0; i < sides; i++) {
      final angle = i * angleStep - pi / 2; // Start from top
      final x = centerX + radius * cos(angle);
      final y = centerY + radius * sin(angle);

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    path.close();

    return path;
  }

  // ============================================================================
  // STAR VARIATIONS
  // ============================================================================

  /// 5-pointed star (original implementation)
  static Path drawStar(Size size) {
    return _drawStar(size, 5);
  }

  /// 4-pointed star
  static Path drawStar4(Size size) {
    return _drawStar(size, 4);
  }

  /// 6-pointed star
  static Path drawStar6(Size size) {
    return _drawStar(size, 6);
  }

  /// 8-pointed star
  static Path drawStar8(Size size) {
    return _drawStar(size, 8);
  }

  /// Helper method to draw stars with different point counts
  static Path _drawStar(Size size, int numberOfPoints) {
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

  // ============================================================================
  // FUN SHAPES
  // ============================================================================

  /// Heart shape
  static Path drawHeart(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Heart shape using cubic bezier curves
    path.moveTo(width / 2, height * 0.3);

    // Left curve
    path.cubicTo(width * 0.2, height * 0.1, -width * 0.25, height * 0.6,
        width / 2, height);

    // Right curve
    path.cubicTo(width * 1.25, height * 0.6, width * 0.8, height * 0.1,
        width / 2, height * 0.3);

    return path;
  }

  /// Flower shape using proper SVG path parsing
  static Path drawFlower(Size size) {
    const svgPathString =
        "M30 30A1 1 0 0040 30 1 1 0 0030 30ZM41 30Q53 30 47 20 38 12 37 24 41 26 41 30ZM36 24Q33 12 25 19 21 25 29 29 30 24 36 24ZM29 30Q18 28 21 37 25 45 31 34 29 32 29 30ZM32 35Q26 46 37 45 44 44 38 35 35 37 32 35ZM39 34Q42 46 50 39 54 28 41 31 41 33 39 34";

    return _parseSvgPath(svgPathString, size);
  }

  /// Parse an SVG path string and return a scaled Path object
  static Path _parseSvgPath(String svgPath, Size size) {
    final path = Path();

    // Calculate bounding box of the original SVG path
    final bounds = _calculateSvgBounds(svgPath);

    // Calculate scale to fit the provided size
    final scaleX = size.width / bounds.width;
    final scaleY = size.height / bounds.height;
    final scale = scaleX < scaleY ? scaleX : scaleY;

    // Calculate offset to center the shape
    final offsetX =
        (size.width - bounds.width * scale) / 2 - bounds.left * scale;
    final offsetY =
        (size.height - bounds.height * scale) / 2 - bounds.top * scale;

    // Parse the SVG path commands
    final commands = _tokenizeSvgPath(svgPath);
    double currentX = 0, currentY = 0;
    double startX = 0, startY = 0;

    for (int i = 0; i < commands.length; i++) {
      final command = commands[i];

      switch (command.toUpperCase()) {
        case 'M': // Move to
          final x = double.parse(commands[++i]) * scale + offsetX;
          final y = double.parse(commands[++i]) * scale + offsetY;
          path.moveTo(x, y);
          currentX = x;
          currentY = y;
          startX = x;
          startY = y;
          break;

        case 'L': // Line to
          final x = double.parse(commands[++i]) * scale + offsetX;
          final y = double.parse(commands[++i]) * scale + offsetY;
          path.lineTo(x, y);
          currentX = x;
          currentY = y;
          break;

        case 'Q': // Quadratic Bezier curve
          final cpX = double.parse(commands[++i]) * scale + offsetX;
          final cpY = double.parse(commands[++i]) * scale + offsetY;
          final x = double.parse(commands[++i]) * scale + offsetX;
          final y = double.parse(commands[++i]) * scale + offsetY;
          path.quadraticBezierTo(cpX, cpY, x, y);
          currentX = x;
          currentY = y;
          break;

        case 'A': // Arc
          final rx = double.parse(commands[++i]) * scale;
          final ry = double.parse(commands[++i]) * scale;
          final xAxisRotation = double.parse(commands[++i]);
          final largeArcFlag = int.parse(commands[++i]);
          final sweepFlag = int.parse(commands[++i]);
          final x = double.parse(commands[++i]) * scale + offsetX;
          final y = double.parse(commands[++i]) * scale + offsetY;

          // Convert SVG arc to Flutter path arc
          _addArcToPath(path, currentX, currentY, x, y, rx, ry, xAxisRotation,
              largeArcFlag == 1, sweepFlag == 1);
          currentX = x;
          currentY = y;
          break;

        case 'Z': // Close path
          path.lineTo(startX, startY);
          path.close();
          break;
      }
    }

    return path;
  }

  /// Tokenize SVG path string into individual commands and coordinates
  static List<String> _tokenizeSvgPath(String svgPath) {
    final tokens = <String>[];
    final buffer = StringBuffer();

    for (int i = 0; i < svgPath.length; i++) {
      final char = svgPath[i];

      if ('MLQAZmlqaz'.contains(char)) {
        if (buffer.isNotEmpty) {
          tokens.add(buffer.toString().trim());
          buffer.clear();
        }
        tokens.add(char);
      } else if (char == ' ' || char == ',') {
        if (buffer.isNotEmpty) {
          tokens.add(buffer.toString().trim());
          buffer.clear();
        }
      } else {
        buffer.write(char);
      }
    }

    if (buffer.isNotEmpty) {
      tokens.add(buffer.toString().trim());
    }

    return tokens.where((token) => token.isNotEmpty).toList();
  }

  /// Calculate the bounding box of an SVG path
  static Rect _calculateSvgBounds(String svgPath) {
    final commands = _tokenizeSvgPath(svgPath);
    double minX = double.infinity;
    double minY = double.infinity;
    double maxX = double.negativeInfinity;
    double maxY = double.negativeInfinity;

    for (int i = 0; i < commands.length; i++) {
      final command = commands[i];

      switch (command.toUpperCase()) {
        case 'M': // Move to
        case 'L': // Line to
          final x = double.parse(commands[++i]);
          final y = double.parse(commands[++i]);
          minX = minX < x ? minX : x;
          minY = minY < y ? minY : y;
          maxX = maxX > x ? maxX : x;
          maxY = maxY > y ? maxY : y;
          break;

        case 'Q': // Quadratic Bezier curve
          final cpX = double.parse(commands[++i]);
          final cpY = double.parse(commands[++i]);
          final x = double.parse(commands[++i]);
          final y = double.parse(commands[++i]);

          // Update bounds for control point and end point
          minX = minX < cpX ? minX : cpX;
          minY = minY < cpY ? minY : cpY;
          maxX = maxX > cpX ? maxX : cpX;
          maxY = maxY > cpY ? maxY : cpY;

          minX = minX < x ? minX : x;
          minY = minY < y ? minY : y;
          maxX = maxX > x ? maxX : x;
          maxY = maxY > y ? maxY : y;
          break;

        case 'A': // Arc
          i += 5; // Skip rx, ry, rotation, large-arc-flag, sweep-flag
          final x = double.parse(commands[++i]);
          final y = double.parse(commands[++i]);

          minX = minX < x ? minX : x;
          minY = minY < y ? minY : y;
          maxX = maxX > x ? maxX : x;
          maxY = maxY > y ? maxY : y;
          break;
      }
    }

    return Rect.fromLTRB(minX, minY, maxX, maxY);
  }

  /// Add an SVG arc to a Flutter Path
  static void _addArcToPath(
      Path path,
      double x1,
      double y1,
      double x2,
      double y2,
      double rx,
      double ry,
      double rotation,
      bool largeArcFlag,
      bool sweepFlag) {
    // For simplicity, we'll approximate the arc with a quadratic curve
    // This is not a perfect conversion but works for most cases

    if (x1 == x2 && y1 == y2) {
      return; // No arc needed
    }

    // Calculate the center point and angles (simplified approximation)
    final midX = (x1 + x2) / 2;
    final midY = (y1 + y2) / 2;

    // For small arcs like in the flower (rx=1, ry=1), we can approximate with a line
    if (rx <= 1 && ry <= 1) {
      path.lineTo(x2, y2);
      return;
    }

    // For larger arcs, use a quadratic approximation
    final controlX = midX + (sweepFlag ? rx : -rx);
    final controlY = midY + (sweepFlag ? ry : -ry);

    path.quadraticBezierTo(controlX, controlY, x2, y2);
  }

  /// Leaf shape
  static Path drawLeaf(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    path.moveTo(width / 2, 0); // Top point

    // Right curve
    path.quadraticBezierTo(width, height / 3, width / 2, height);

    // Left curve
    path.quadraticBezierTo(0, height / 3, width / 2, 0);

    return path;
  }

  /// Butterfly shape
  static Path drawButterfly(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 62x44)
    final scaleX = width / 62.0;
    final scaleY = height / 44.0;

    // Body path: M28 30Q28 40 31 40Q34 40 34 30Q34 29 33 28Q34 28 34 21Q34 20 33 19Q34 15 31 15Q28 15 29 19Q28 20 28 21Q28 28 29 28Q28 29 28 30
    path.moveTo(28 * scaleX, 30 * scaleY);
    path.quadraticBezierTo(28 * scaleX, 40 * scaleY, 31 * scaleX, 40 * scaleY);
    path.quadraticBezierTo(34 * scaleX, 40 * scaleY, 34 * scaleX, 30 * scaleY);
    path.quadraticBezierTo(34 * scaleX, 29 * scaleY, 33 * scaleX, 28 * scaleY);
    path.quadraticBezierTo(34 * scaleX, 28 * scaleY, 34 * scaleX, 21 * scaleY);
    path.quadraticBezierTo(34 * scaleX, 20 * scaleY, 33 * scaleX, 19 * scaleY);
    path.quadraticBezierTo(34 * scaleX, 15 * scaleY, 31 * scaleX, 15 * scaleY);
    path.quadraticBezierTo(28 * scaleX, 15 * scaleY, 29 * scaleX, 19 * scaleY);
    path.quadraticBezierTo(28 * scaleX, 20 * scaleY, 28 * scaleX, 21 * scaleY);
    path.quadraticBezierTo(28 * scaleX, 28 * scaleY, 29 * scaleX, 28 * scaleY);
    path.quadraticBezierTo(28 * scaleX, 29 * scaleY, 28 * scaleX, 30 * scaleY);

    // Right antenna: M33 15Q37 8 41 7Q38 8 33 15Z
    path.moveTo(33 * scaleX, 15 * scaleY);
    path.quadraticBezierTo(37 * scaleX, 8 * scaleY, 41 * scaleX, 7 * scaleY);
    path.quadraticBezierTo(38 * scaleX, 8 * scaleY, 33 * scaleX, 15 * scaleY);
    path.close();

    // Left antenna: M29 15Q25 8 21 7Q26 8 29 15Z
    path.moveTo(29 * scaleX, 15 * scaleY);
    path.quadraticBezierTo(25 * scaleX, 8 * scaleY, 21 * scaleX, 7 * scaleY);
    path.quadraticBezierTo(26 * scaleX, 8 * scaleY, 29 * scaleX, 15 * scaleY);
    path.close();

    // Left wing: M28 19Q18 2 5 6Q0 8 5 18Q7 22 19 27Q9 32 13 39Q16 44 27 34Q26 29 28 28Q26 22 28 19Z
    path.moveTo(28 * scaleX, 19 * scaleY);
    path.quadraticBezierTo(18 * scaleX, 2 * scaleY, 5 * scaleX, 6 * scaleY);
    path.quadraticBezierTo(0 * scaleX, 8 * scaleY, 5 * scaleX, 18 * scaleY);
    path.quadraticBezierTo(7 * scaleX, 22 * scaleY, 19 * scaleX, 27 * scaleY);
    path.quadraticBezierTo(9 * scaleX, 32 * scaleY, 13 * scaleX, 39 * scaleY);
    path.quadraticBezierTo(16 * scaleX, 44 * scaleY, 27 * scaleX, 34 * scaleY);
    path.quadraticBezierTo(26 * scaleX, 29 * scaleY, 28 * scaleX, 28 * scaleY);
    path.quadraticBezierTo(26 * scaleX, 22 * scaleY, 28 * scaleX, 19 * scaleY);
    path.close();

    // Right wing: M34 19Q44 2 57 6Q62 8 57 18Q55 22 43 27Q53 32 49 38Q44 44 35 34Q36 29 34 28Q36 22 34 19Z
    path.moveTo(34 * scaleX, 19 * scaleY);
    path.quadraticBezierTo(44 * scaleX, 2 * scaleY, 57 * scaleX, 6 * scaleY);
    path.quadraticBezierTo(62 * scaleX, 8 * scaleY, 57 * scaleX, 18 * scaleY);
    path.quadraticBezierTo(55 * scaleX, 22 * scaleY, 43 * scaleX, 27 * scaleY);
    path.quadraticBezierTo(53 * scaleX, 32 * scaleY, 49 * scaleX, 38 * scaleY);
    path.quadraticBezierTo(44 * scaleX, 44 * scaleY, 35 * scaleX, 34 * scaleY);
    path.quadraticBezierTo(36 * scaleX, 29 * scaleY, 34 * scaleX, 28 * scaleY);
    path.quadraticBezierTo(36 * scaleX, 22 * scaleY, 34 * scaleX, 19 * scaleY);
    path.close();

    return path;
  }
  // ============================================================================
  // SYMBOLS
  // ============================================================================

  /// Cross shape (religious cross)
  static Path drawCross(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 27x27)
    final scaleX = width / 27.0;
    final scaleY = height / 27.0;

    // Apply your SVG path: M10 0 10 10 0 10 0 17 10 17 10 27 17 27 17 17 27 17 27 10 17 10 17 0Z
    path.moveTo(10 * scaleX, 0 * scaleY);
    path.lineTo(10 * scaleX, 10 * scaleY);
    path.lineTo(0 * scaleX, 10 * scaleY);
    path.lineTo(0 * scaleX, 17 * scaleY);
    path.lineTo(10 * scaleX, 17 * scaleY);
    path.lineTo(10 * scaleX, 27 * scaleY);
    path.lineTo(17 * scaleX, 27 * scaleY);
    path.lineTo(17 * scaleX, 17 * scaleY);
    path.lineTo(27 * scaleX, 17 * scaleY);
    path.lineTo(27 * scaleX, 10 * scaleY);
    path.lineTo(17 * scaleX, 10 * scaleY);
    path.lineTo(17 * scaleX, 0 * scaleY);
    path.close();

    return path;
  }

  /// Plus sign
  static Path drawPlus(Size size) {
    return drawCross(size); // Same as cross
  }

  /// Arrow pointing up
  static Path drawArrow(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Arrow head
    path.moveTo(width / 2, 0); // Top point
    path.lineTo(width / 4, height / 3); // Left point
    path.lineTo(width * 3 / 8, height / 3); // Left inner
    path.lineTo(width * 3 / 8, height); // Left bottom
    path.lineTo(width * 5 / 8, height); // Right bottom
    path.lineTo(width * 5 / 8, height / 3); // Right inner
    path.lineTo(width * 3 / 4, height / 3); // Right point
    path.close();

    return path;
  }

  /// Lightning bolt
  static Path drawLightning(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 20x23)
    final scaleX = width / 20.0;
    final scaleY = height / 23.0;

    // Apply your SVG path: M0 23 16 13 11 9 20 0 4 9 9 13Z
    path.moveTo(0 * scaleX, 23 * scaleY);
    path.lineTo(16 * scaleX, 13 * scaleY);
    path.lineTo(11 * scaleX, 9 * scaleY);
    path.lineTo(20 * scaleX, 0 * scaleY);
    path.lineTo(4 * scaleX, 9 * scaleY);
    path.lineTo(9 * scaleX, 13 * scaleY);
    path.close();

    return path;
  }

  // ============================================================================
  // SPECIAL SHAPES (Placeholders for complex paths you'll add)
  // ============================================================================

  /// Skull shape
  static Path drawSkull(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 16x20)
    final scaleX = width / 16.0;
    final scaleY = height / 20.0;

    // First subpath: Main skull shape
    // M0 5Q0 0 8 0Q16 0 16 5Q16 12 12 11Q12 14 11 14Q10 14 10 12Q10 14 9 14Q8 14 8 12Q8 14 7 14Q6 14 6 12Q6 14 5 14Q4 14 4 11Q0 12 0 5Z
    path.moveTo(0 * scaleX, 5 * scaleY);
    path.quadraticBezierTo(0 * scaleX, 0 * scaleY, 8 * scaleX, 0 * scaleY);
    path.quadraticBezierTo(16 * scaleX, 0 * scaleY, 16 * scaleX, 5 * scaleY);
    path.quadraticBezierTo(16 * scaleX, 12 * scaleY, 12 * scaleX, 11 * scaleY);
    path.quadraticBezierTo(12 * scaleX, 14 * scaleY, 11 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(10 * scaleX, 14 * scaleY, 10 * scaleX, 12 * scaleY);
    path.quadraticBezierTo(10 * scaleX, 14 * scaleY, 9 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(8 * scaleX, 14 * scaleY, 8 * scaleX, 12 * scaleY);
    path.quadraticBezierTo(8 * scaleX, 14 * scaleY, 7 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(6 * scaleX, 14 * scaleY, 6 * scaleX, 12 * scaleY);
    path.quadraticBezierTo(6 * scaleX, 14 * scaleY, 5 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(4 * scaleX, 14 * scaleY, 4 * scaleX, 11 * scaleY);
    path.quadraticBezierTo(0 * scaleX, 12 * scaleY, 0 * scaleX, 5 * scaleY);
    path.close();

    // Second subpath: Jaw/mouth area
    // M5 17Q8 19 11 17Q11 14 10 14Q9 14 9 16Q9 14 8 14Q7 14 7 16Q7 14 6 14Q5 14 5 17Z
    path.moveTo(5 * scaleX, 17 * scaleY);
    path.quadraticBezierTo(8 * scaleX, 19 * scaleY, 11 * scaleX, 17 * scaleY);
    path.quadraticBezierTo(11 * scaleX, 14 * scaleY, 10 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(9 * scaleX, 14 * scaleY, 9 * scaleX, 16 * scaleY);
    path.quadraticBezierTo(9 * scaleX, 14 * scaleY, 8 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(7 * scaleX, 14 * scaleY, 7 * scaleX, 16 * scaleY);
    path.quadraticBezierTo(7 * scaleX, 14 * scaleY, 6 * scaleX, 14 * scaleY);
    path.quadraticBezierTo(5 * scaleX, 14 * scaleY, 5 * scaleX, 17 * scaleY);
    path.close();

    // Third subpath: Right eye
    // M13 6Q13 4 11 4Q10 4 10 6Q10 8 12 8Q13 8 13 6Z
    path.moveTo(13 * scaleX, 6 * scaleY);
    path.quadraticBezierTo(13 * scaleX, 4 * scaleY, 11 * scaleX, 4 * scaleY);
    path.quadraticBezierTo(10 * scaleX, 4 * scaleY, 10 * scaleX, 6 * scaleY);
    path.quadraticBezierTo(10 * scaleX, 8 * scaleY, 12 * scaleX, 8 * scaleY);
    path.quadraticBezierTo(13 * scaleX, 8 * scaleY, 13 * scaleX, 6 * scaleY);
    path.close();

    // Fourth subpath: Left eye
    // M3 6Q3 8 4 8Q6 8 6 6Q6 4 5 4Q3 4 3 6Z
    path.moveTo(3 * scaleX, 6 * scaleY);
    path.quadraticBezierTo(3 * scaleX, 8 * scaleY, 4 * scaleX, 8 * scaleY);
    path.quadraticBezierTo(6 * scaleX, 8 * scaleY, 6 * scaleX, 6 * scaleY);
    path.quadraticBezierTo(6 * scaleX, 4 * scaleY, 5 * scaleX, 4 * scaleY);
    path.quadraticBezierTo(3 * scaleX, 4 * scaleY, 3 * scaleX, 6 * scaleY);
    path.close();

    return path;
  }

  /// Crown shape
  static Path drawCrown(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 100x100)
    final scaleX = width / 100.0;
    final scaleY = height / 100.0;

    // Apply your SVG path: M0 0 30 50 33 50 50 10 67 50 70 50 100 0 100 100 0 100Z
    path.moveTo(0 * scaleX, 0 * scaleY);
    path.lineTo(30 * scaleX, 50 * scaleY);
    path.lineTo(33 * scaleX, 50 * scaleY);
    path.lineTo(50 * scaleX, 10 * scaleY);
    path.lineTo(67 * scaleX, 50 * scaleY);
    path.lineTo(70 * scaleX, 50 * scaleY);
    path.lineTo(100 * scaleX, 0 * scaleY);
    path.lineTo(100 * scaleX, 100 * scaleY);
    path.lineTo(0 * scaleX, 100 * scaleY);
    path.close();

    return path;
  }

  /// Sword
  /// M9 16 11 16 11 9Q17 9 19 5 15 7 11 7 14-18 6-18 9-8 9 7 4 7 1 5 2 9 9 9Z
  static Path drawSword(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 64x54)
    final scaleX = width / 64.0;
    final scaleY = height / 54.0;

    // Apply your SVG path: M9 16 11 16 11 9Q17 9 19 5 15 7 11 7 14-18 6-18 9-8 9 7 4 7 1 5 2 9 9 9Z
    path.moveTo(9 * scaleX, 16 * scaleY);
    path.lineTo(11 * scaleX, 16 * scaleY);
    path.lineTo(11 * scaleX, 9 * scaleY);
    path.quadraticBezierTo(17 * scaleX, 9 * scaleY, 19 * scaleX, 5 * scaleY);
    path.quadraticBezierTo(15 * scaleX, 7 * scaleY, 11 * scaleX, 7 * scaleY);
    path.quadraticBezierTo(14 * scaleX, -18 * scaleY, 6 * scaleX, -18 * scaleY);
    path.quadraticBezierTo(9 * scaleX, -8 * scaleY, 9 * scaleX, 7 * scaleY);
    path.lineTo(7 * scaleX, 4 * scaleY);
    path.lineTo(7 * scaleX, 1 * scaleY);
    path.lineTo(5 * scaleX, 2 * scaleY);
    path.lineTo(9 * scaleX, 9 * scaleY);
    path.lineTo(9 * scaleX, 9 * scaleY);
    path.close();

    return path;
  }

  /// Music note shape
  static Path drawMusicNote(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Scale factors to fit the SVG path (original viewBox appears to be around 64x54)
    final scaleX = width / 64.0;
    final scaleY = height / 54.0;

    // Apply your SVG path: M48 4v36.7c-1.5-.5-3.1-.7-4.8-.7-6.1 0-11 3.1-11 7s4.9 7 11 7 11-3.1 11-7V11h9.8V4H48
    path.moveTo(48 * scaleX, 4 * scaleY);
    path.relativeLineTo(0, 36.7 * scaleY);
    path.relativeCubicTo(-1.5 * scaleX, -0.5 * scaleY, -3.1 * scaleX,
        -0.7 * scaleY, -4.8 * scaleX, -0.7 * scaleY);

    // Note: The SVG path contains arc commands (s) which need to be converted to cubic curves
    // Approximating the elliptical arcs with cubic Bezier curves
    path.relativeCubicTo(
        -6.1 * scaleX, 0, -11 * scaleX, 3.1 * scaleY, -11 * scaleX, 7 * scaleY);
    path.relativeCubicTo(
        0, 3.9 * scaleY, 4.9 * scaleX, 7 * scaleY, 11 * scaleX, 7 * scaleY);
    path.relativeCubicTo(
        6.1 * scaleX, 0, 11 * scaleX, -3.1 * scaleY, 11 * scaleX, -7 * scaleY);
    path.lineTo(54 * scaleX, 11 * scaleY);
    path.lineTo(63.8 * scaleX, 11 * scaleY);
    path.lineTo(63.8 * scaleX, 4 * scaleY);
    path.lineTo(48 * scaleX, 4 * scaleY);
    path.close();

    return path;
  }
}
