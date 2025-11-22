# Premium Typography System

<!--## 🎨 Design Philosophy
Luxurious, minimal, and futuristic typography perfect for a dark neon AI assistant mobile interface.

## 📝 Font Families

### Primary: **Manrope SemiBold**
- **Usage**: All primary headings, buttons, and emphasis text
- **Character**: Modern, elegant, and futuristic
- **Weight**: 600 (SemiBold)

### Secondary: **Inter Regular**
- **Usage**: Subtitles, body text, captions, and secondary content
- **Character**: Premium, clean, and highly readable
- **Weight**: 400 (Regular)

---

## 📐 Typography Scales

### Headings (Manrope SemiBold)

#### Primary Heading
- **Size**: 32sp
- **Line Height**: 1.15 (tight)
- **Letter Spacing**: -0.6 (negative, elegant)
- **Color**: White (#FFFFFF)
- **Use Case**: Main app title, hero sections

#### Heading 1
- **Size**: 28sp
- **Line Height**: 1.15
- **Letter Spacing**: -0.5
- **Color**: White (#FFFFFF)
- **Use Case**: Page titles, major sections

#### Heading 2
- **Size**: 26sp
- **Line Height**: 1.15
- **Letter Spacing**: -0.4
- **Color**: White (#FFFFFF)
- **Use Case**: Sub-sections, card titles

#### Heading 3
- **Size**: 24sp
- **Line Height**: 1.2
- **Letter Spacing**: -0.3
- **Color**: White (#FFFFFF)
- **Use Case**: Smaller headings, emphasis

---

### Body Text (Inter Regular)

#### Subtitle
- **Size**: 17sp
- **Line Height**: 1.5 (relaxed, readable)
- **Letter Spacing**: 0
- **Color**: Soft Gray (#C9C9C9)
- **Use Case**: Primary descriptions, subtitles

#### Subtitle 2
- **Size**: 15sp
- **Line Height**: 1.55
- **Letter Spacing**: 0
- **Color**: Soft Gray (#C9C9C9)
- **Use Case**: Secondary descriptions

#### Body
- **Size**: 16sp
- **Line Height**: 1.5
- **Letter Spacing**: 0
- **Color**: Light Gray (#E0E0E0)
- **Use Case**: Main content, paragraphs

#### Body Small
- **Size**: 14sp
- **Line Height**: 1.45
- **Letter Spacing**: 0
- **Color**: Soft Gray (#C9C9C9)
- **Use Case**: Cards, smaller content

---

### Buttons (Manrope Medium)

#### Button
- **Size**: 16sp
- **Weight**: 500 (Medium)
- **Line Height**: 1.2
- **Letter Spacing**: 0.5
- **Color**: White (#FFFFFF)
- **Use Case**: Primary buttons, CTAs

#### Button Small
- **Size**: 14sp
- **Weight**: 500
- **Line Height**: 1.2
- **Letter Spacing**: 0.3
- **Color**: White (#FFFFFF)
- **Use Case**: Secondary buttons, small CTAs

---

### Captions & Labels (Inter Regular)

#### Caption
- **Size**: 13sp
- **Line Height**: 1.4
- **Letter Spacing**: 0
- **Color**: Medium Gray (#9E9E9E)
- **Use Case**: Meta information, timestamps

#### Label
- **Size**: 12sp
- **Weight**: 500
- **Line Height**: 1.3
- **Letter Spacing**: 0.5
- **Color**: Light Gray (#B0B0B0)
- **Use Case**: Form labels, tags

---

## 🌟 Special Styles

### Neon Accent (Manrope SemiBold)
- **Size**: 20sp
- **Weight**: 600
- **Line Height**: 1.2
- **Letter Spacing**: -0.3
- **Color**: Neon Purple (#A463F2)
- **Use Case**: Highlighted text, special callouts

### Chat Message (Inter Regular)
- **Size**: 15sp
- **Line Height**: 1.5
- **Letter Spacing**: 0
- **Color**: Near White (#E8E8E8)
- **Use Case**: Chat interface, conversational text

---

## 💡 Usage Guidelines

### ✅ DO:
- Use Manrope for all headings and buttons
- Use Inter for all body text and descriptions
- Apply negative letter spacing (-0.3 to -0.6) for headings
- Use tight line height (1.15) for headings
- Use relaxed line height (1.45-1.55) for body text
- Keep soft gray (#C9C9C9) for secondary text

### ❌ DON'T:
- Mix multiple font families unnecessarily
- Use positive letter spacing on headings
- Exceed 32sp for headings (keeps it minimal)
- Use pure white for body text (too harsh)
- Use line height below 1.4 for body text

---

## 🚀 Implementation

Import the typography system in your screens:

```dart
import '../theme/app_text_styles.dart';
```

### Example Usage:

```dart
// Primary Heading
Text(
  'Hello! I\'m Your AI Assistant',
  style: AppTextStyles.heading1,
)

// Subtitle
Text(
  'What would you like to do today?',
  style: AppTextStyles.subtitle,
)

// Button
Text(
  'Analyze Resume',
  style: AppTextStyles.button,
)

// Body Text
Text(
  'Get instant ATS score & personalized feedback',
  style: AppTextStyles.bodySmall,
)
```

---

## 🎭 Color Palette

- **White**: #FFFFFF (Headings, buttons)
- **Near White**: #E8E8E8 (Chat messages)
- **Light Gray**: #E0E0E0 (Body text)
- **Soft Gray**: #C9C9C9 (Subtitles, secondary)
- **Medium Gray**: #9E9E9E (Captions)
- **Light Gray 2**: #B0B0B0 (Labels)
- **Neon Purple**: #A463F2 (Accent)

---

## 📱 Platform Integration

Using Google Fonts package for seamless font delivery:
- Automatic font downloading
- Caching for performance
- Cross-platform consistency
- No manual font file management

All fonts are loaded via `google_fonts` package which handles downloading, caching, and platform-specific rendering automatically.

---

**Created for**: Resume ATS Mobile App  
**Design System**: Futuristic Neon AI Assistant  
**Theme**: Dark Mode Premium
