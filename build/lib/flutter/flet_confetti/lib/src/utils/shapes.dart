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
      case "snowflake":
        return drawSnowflake;
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
    path.cubicTo(
      width * 0.2, height * 0.1,
      -width * 0.25, height * 0.6,
      width / 2, height
    );
    
    // Right curve
    path.cubicTo(
      width * 1.25, height * 0.6,
      width * 0.8, height * 0.1,
      width / 2, height * 0.3
    );
    
    return path;
  }

  /// Simple flower shape
  static Path drawFlower(Size size) {
    final path = Path();
    final centerX = size.width / 2;
    final centerY = size.height / 2;
    final petalRadius = size.width / 4;
    
    // Draw 6 petals
    for (int i = 0; i < 6; i++) {
      final angle = i * pi / 3;
      final petalX = centerX + petalRadius * cos(angle);
      final petalY = centerY + petalRadius * sin(angle);
      
      path.addOval(Rect.fromCircle(
        center: Offset(petalX, petalY),
        radius: petalRadius / 2,
      ));
    }
    
    // Center circle
    path.addOval(Rect.fromCircle(
      center: Offset(centerX, centerY),
      radius: petalRadius / 3,
    ));
    
    return path;
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

  /// Simple butterfly shape
  static Path drawButterfly(Size size) {
    final path = Path();
    final centerX = size.width / 2;
    final centerY = size.height / 2;
    final wingWidth = size.width / 4;
    final wingHeight = size.height / 3;
    
    // Top wings
    path.addOval(Rect.fromCenter(
      center: Offset(centerX - wingWidth / 2, centerY - wingHeight / 2),
      width: wingWidth,
      height: wingHeight,
    ));
    path.addOval(Rect.fromCenter(
      center: Offset(centerX + wingWidth / 2, centerY - wingHeight / 2),
      width: wingWidth,
      height: wingHeight,
    ));
    
    // Bottom wings
    path.addOval(Rect.fromCenter(
      center: Offset(centerX - wingWidth / 2, centerY + wingHeight / 2),
      width: wingWidth * 0.8,
      height: wingHeight * 0.8,
    ));
    path.addOval(Rect.fromCenter(
      center: Offset(centerX + wingWidth / 2, centerY + wingHeight / 2),
      width: wingWidth * 0.8,
      height: wingHeight * 0.8,
    ));
    
    // Body
    path.addRect(Rect.fromCenter(
      center: Offset(centerX, centerY),
      width: size.width / 20,
      height: size.height,
    ));
    
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
    final thickness = width / 5;

    // Vertical bar
    path.addRect(Rect.fromLTWH(
      (width - thickness) / 2, 0,
      thickness, height,
    ));

    // Horizontal bar
    path.addRect(Rect.fromLTWH(
      0, (height - thickness) / 2,
      width, thickness,
    ));

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

    path.moveTo(width * 0.3, 0);
    path.lineTo(width * 0.7, 0);
    path.lineTo(width * 0.4, height * 0.6);
    path.lineTo(width * 0.8, height * 0.6);
    path.lineTo(width * 0.2, height);
    path.lineTo(width * 0.5, height * 0.4);
    path.lineTo(width * 0.1, height * 0.4);
    path.close();

    return path;
  }

  // ============================================================================
  // SPECIAL SHAPES (Placeholders for complex paths you'll add)
  // ============================================================================

  /// Skull shape (placeholder - you can replace with detailed path)
  static Path drawSkull(Size size) {
    final path = Path();
    final centerX = size.width / 2;
    final centerY = size.height / 2;

    // Simple skull outline (you can make this more detailed)
    path.addOval(Rect.fromCenter(
      center: Offset(centerX, centerY * 0.7),
      width: size.width * 0.8,
      height: size.height * 0.6,
    ));

    // Eye sockets
    path.addOval(Rect.fromCenter(
      center: Offset(centerX - size.width * 0.15, centerY * 0.6),
      width: size.width * 0.15,
      height: size.height * 0.15,
    ));
    path.addOval(Rect.fromCenter(
      center: Offset(centerX + size.width * 0.15, centerY * 0.6),
      width: size.width * 0.15,
      height: size.height * 0.15,
    ));

    return path;
  }

  /// Crown shape (placeholder)
  static Path drawCrown(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Simple crown outline
    path.moveTo(0, height * 0.7);
    path.lineTo(width * 0.2, height * 0.3);
    path.lineTo(width * 0.4, height * 0.5);
    path.lineTo(width * 0.6, height * 0.1);
    path.lineTo(width * 0.8, height * 0.5);
    path.lineTo(width, height * 0.3);
    path.lineTo(width, height);
    path.lineTo(0, height);
    path.close();

    return path;
  }

  /// Snowflake shape (placeholder)
  static Path drawSnowflake(Size size) {
    final path = Path();
    final centerX = size.width / 2;
    final centerY = size.height / 2;
    final radius = size.width / 2;

    // Draw 6 spokes
    for (int i = 0; i < 6; i++) {
      final angle = i * pi / 3;
      final endX = centerX + radius * cos(angle);
      final endY = centerY + radius * sin(angle);

      path.moveTo(centerX, centerY);
      path.lineTo(endX, endY);

      // Add small branches
      final branchLength = radius * 0.3;
      final branchX1 = centerX + (radius * 0.7) * cos(angle) + branchLength * cos(angle + pi / 4);
      final branchY1 = centerY + (radius * 0.7) * sin(angle) + branchLength * sin(angle + pi / 4);
      final branchX2 = centerX + (radius * 0.7) * cos(angle) + branchLength * cos(angle - pi / 4);
      final branchY2 = centerY + (radius * 0.7) * sin(angle) + branchLength * sin(angle - pi / 4);

      path.moveTo(centerX + (radius * 0.7) * cos(angle), centerY + (radius * 0.7) * sin(angle));
      path.lineTo(branchX1, branchY1);
      path.moveTo(centerX + (radius * 0.7) * cos(angle), centerY + (radius * 0.7) * sin(angle));
      path.lineTo(branchX2, branchY2);
    }

    return path;
  }

  /// Music note shape (placeholder)
  static Path drawMusicNote(Size size) {
    final path = Path();
    final width = size.width;
    final height = size.height;

    // Note head (oval)
    path.addOval(Rect.fromLTWH(
      0, height * 0.6,
      width * 0.4, height * 0.4,
    ));

    // Note stem
    path.addRect(Rect.fromLTWH(
      width * 0.35, 0,
      width * 0.1, height * 0.8,
    ));

    // Flag
    path.moveTo(width * 0.45, 0);
    path.quadraticBezierTo(width, height * 0.1, width * 0.7, height * 0.3);
    path.quadraticBezierTo(width * 0.6, height * 0.2, width * 0.45, height * 0.15);
    path.close();

    return path;
  }
}
