import 'package:flutter/material.dart';

/// Utility class for handling confetti color themes
class ConfettiThemes {
  /// Get colors for a given theme name
  static List<Color> getThemeColors(String themeName) {
    switch (themeName.toLowerCase()) {
      // Festive themes
      case 'christmas':
        return [
          const Color(0xFFFF0000), // Red
          const Color(0xFF00FF00), // Green
          const Color(0xFFFFD700), // Gold
          const Color(0xFFFFFFFF), // White
          const Color(0xFF8B0000), // Dark Red
          const Color(0xFF006400), // Dark Green
        ];
      
      case 'halloween':
        return [
          const Color(0xFFFF8C00), // Orange
          const Color(0xFF000000), // Black
          const Color(0xFF800080), // Purple
          const Color(0xFF228B22), // Forest Green
          const Color(0xFFFF4500), // Orange Red
        ];
      
      case 'valentine':
        return [
          const Color(0xFFFF69B4), // Hot Pink
          const Color(0xFFFF0000), // Red
          const Color(0xFFFFFFFF), // White
          const Color(0xFFFFB6C1), // Light Pink
          const Color(0xFFDC143C), // Crimson
        ];
      
      case 'easter':
        return [
          const Color(0xFFFFB6C1), // Light Pink
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFF90EE90), // Light Green
          const Color(0xFF87CEEB), // Sky Blue
          const Color(0xFFDDA0DD), // Plum
        ];
      
      case 'new_year':
        return [
          const Color(0xFFFFD700), // Gold
          const Color(0xFFC0C0C0), // Silver
          const Color(0xFF000000), // Black
          const Color(0xFFFFFFFF), // White
          const Color(0xFFFFA500), // Orange
        ];
      
      // Seasonal themes
      case 'spring':
        return [
          const Color(0xFF90EE90), // Light Green
          const Color(0xFF87CEEB), // Sky Blue
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFFFB6C1), // Light Pink
          const Color(0xFF98FB98), // Pale Green
        ];
      
      case 'summer':
        return [
          const Color(0xFF00BFFF), // Deep Sky Blue
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFFF8C00), // Orange
          const Color(0xFFFF0000), // Red
          const Color(0xFF32CD32), // Lime Green
        ];
      
      case 'autumn':
        return [
          const Color(0xFFFF8C00), // Orange
          const Color(0xFFFF0000), // Red
          const Color(0xFF8B4513), // Saddle Brown
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFDAA520), // Goldenrod
        ];
      
      case 'winter':
        return [
          const Color(0xFF87CEEB), // Sky Blue
          const Color(0xFFFFFFFF), // White
          const Color(0xFFC0C0C0), // Silver
          const Color(0xFF4682B4), // Steel Blue
          const Color(0xFFB0E0E6), // Powder Blue
        ];
      
      // Nature themes
      case 'forest':
        return [
          const Color(0xFF228B22), // Forest Green
          const Color(0xFF006400), // Dark Green
          const Color(0xFF32CD32), // Lime Green
          const Color(0xFF8FBC8F), // Dark Sea Green
          const Color(0xFF556B2F), // Dark Olive Green
        ];
      
      case 'ocean':
        return [
          const Color(0xFF0000FF), // Blue
          const Color(0xFF008B8B), // Dark Cyan
          const Color(0xFF00CED1), // Dark Turquoise
          const Color(0xFFFFFFFF), // White
          const Color(0xFF4682B4), // Steel Blue
        ];
      
      case 'sunset':
        return [
          const Color(0xFFFF8C00), // Orange
          const Color(0xFFFF69B4), // Hot Pink
          const Color(0xFF800080), // Purple
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFFF4500), // Orange Red
        ];
      
      case 'rainbow':
        return [
          const Color(0xFFFF0000), // Red
          const Color(0xFFFF8C00), // Orange
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFF00FF00), // Green
          const Color(0xFF0000FF), // Blue
          const Color(0xFF800080), // Purple
        ];
      
      // Party themes
      case 'birthday':
        return [
          const Color(0xFFFF0000), // Red
          const Color(0xFF00FF00), // Green
          const Color(0xFF0000FF), // Blue
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFFF00FF), // Magenta
          const Color(0xFF00FFFF), // Cyan
        ];
      
      case 'wedding':
        return [
          const Color(0xFFFFFFFF), // White
          const Color(0xFFF5F5DC), // Beige
          const Color(0xFFFFB6C1), // Light Pink
          const Color(0xFFFFD700), // Gold
          const Color(0xFFFFFACD), // Lemon Chiffon
        ];
      
      case 'graduation':
        return [
          const Color(0xFF0000FF), // Blue
          const Color(0xFFFFD700), // Gold
          const Color(0xFFFFFFFF), // White
          const Color(0xFF000080), // Navy
          const Color(0xFFC0C0C0), // Silver
        ];
      
      // Style themes
      case 'neon':
        return [
          const Color(0xFFFF073A), // Neon Red
          const Color(0xFF39FF14), // Neon Green
          const Color(0xFF00FFFF), // Cyan
          const Color(0xFFFF00FF), // Magenta
          const Color(0xFFFFFF00), // Yellow
        ];
      
      case 'pastel':
        return [
          const Color(0xFFFFB6C1), // Light Pink
          const Color(0xFF87CEEB), // Sky Blue
          const Color(0xFF98FB98), // Pale Green
          const Color(0xFFF0E68C), // Khaki
          const Color(0xFFDDA0DD), // Plum
        ];
      
      case 'gold':
        return [
          const Color(0xFFFFD700), // Gold
          const Color(0xFFFFA500), // Orange
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFDAA520), // Goldenrod
          const Color(0xFFB8860B), // Dark Goldenrod
        ];
      
      case 'silver':
        return [
          const Color(0xFFC0C0C0), // Silver
          const Color(0xFF808080), // Gray
          const Color(0xFFDCDCDC), // Gainsboro
          const Color(0xFFA9A9A9), // Dark Gray
          const Color(0xFFD3D3D3), // Light Gray
        ];
      
      case 'monochrome':
        return [
          const Color(0xFF000000), // Black
          const Color(0xFFFFFFFF), // White
          const Color(0xFF808080), // Gray
          const Color(0xFFC0C0C0), // Silver
          const Color(0xFF696969), // Dim Gray
        ];
      
      // Default fallback
      default:
        return [
          const Color(0xFFFF0000), // Red
          const Color(0xFF00FF00), // Green
          const Color(0xFF0000FF), // Blue
          const Color(0xFFFFFF00), // Yellow
          const Color(0xFFFF00FF), // Magenta
        ];
    }
  }
  
  /// Check if a theme name is valid
  static bool isValidTheme(String themeName) {
    const validThemes = [
      'christmas', 'halloween', 'valentine', 'easter', 'new_year',
      'spring', 'summer', 'autumn', 'winter',
      'forest', 'ocean', 'sunset', 'rainbow',
      'birthday', 'wedding', 'graduation',
      'neon', 'pastel', 'gold', 'silver', 'monochrome'
    ];
    return validThemes.contains(themeName.toLowerCase());
  }
}
