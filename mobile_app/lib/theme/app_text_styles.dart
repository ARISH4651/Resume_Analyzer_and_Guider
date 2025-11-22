import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Premium typography system for futuristic AI assistant interface
class AppTextStyles {
  // Primary Headings - Manrope SemiBold
  static TextStyle get primaryHeading => GoogleFonts.manrope(
        fontSize: 32,
        fontWeight: FontWeight.w600,
        height: 1.15,
        letterSpacing: -0.6,
        color: Colors.white,
      );

  static TextStyle get heading1 => GoogleFonts.manrope(
        fontSize: 28,
        fontWeight: FontWeight.w600,
        height: 1.15,
        letterSpacing: -0.5,
        color: Colors.white,
      );

  static TextStyle get heading2 => GoogleFonts.manrope(
        fontSize: 26,
        fontWeight: FontWeight.w600,
        height: 1.15,
        letterSpacing: -0.4,
        color: Colors.white,
      );

  static TextStyle get heading3 => GoogleFonts.manrope(
        fontSize: 24,
        fontWeight: FontWeight.w600,
        height: 1.2,
        letterSpacing: -0.3,
        color: Colors.white,
      );

  // Secondary Text - Inter Regular
  static TextStyle get subtitle => GoogleFonts.inter(
        fontSize: 17,
        fontWeight: FontWeight.w400,
        height: 1.5,
        letterSpacing: 0,
        color: const Color(0xFFC9C9C9),
      );

  static TextStyle get subtitle2 => GoogleFonts.inter(
        fontSize: 15,
        fontWeight: FontWeight.w400,
        height: 1.55,
        letterSpacing: 0,
        color: const Color(0xFFC9C9C9),
      );

  static TextStyle get body => GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w400,
        height: 1.5,
        letterSpacing: 0,
        color: const Color(0xFFE0E0E0),
      );

  static TextStyle get bodySmall => GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        height: 1.45,
        letterSpacing: 0,
        color: const Color(0xFFC9C9C9),
      );

  // Button Text - Manrope Medium
  static TextStyle get button => GoogleFonts.manrope(
        fontSize: 16,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: 0.5,
        color: Colors.white,
      );

  static TextStyle get buttonSmall => GoogleFonts.manrope(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: 0.3,
        color: Colors.white,
      );

  // Caption & Labels - Inter Regular
  static TextStyle get caption => GoogleFonts.inter(
        fontSize: 13,
        fontWeight: FontWeight.w400,
        height: 1.4,
        letterSpacing: 0,
        color: const Color(0xFF9E9E9E),
      );

  static TextStyle get label => GoogleFonts.inter(
        fontSize: 12,
        fontWeight: FontWeight.w500,
        height: 1.3,
        letterSpacing: 0.5,
        color: const Color(0xFFB0B0B0),
      );

  // Special Styles
  static TextStyle get neonAccent => GoogleFonts.manrope(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        height: 1.2,
        letterSpacing: -0.3,
        color: const Color(0xFFA463F2),
      );

  static TextStyle get chatMessage => GoogleFonts.inter(
        fontSize: 15,
        fontWeight: FontWeight.w400,
        height: 1.5,
        letterSpacing: 0,
        color: const Color(0xFFE8E8E8),
      );
}
