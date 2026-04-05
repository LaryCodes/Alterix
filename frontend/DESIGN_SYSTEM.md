# Alterix Design System

## Color Palette

### Primary Colors
- **Soft Pink**: `#fbcfe8` to `#ec4899` - Main brand color, used for primary actions and highlights
- **Warm Brown**: `#bfa094` to `#977669` - Contrasting color, provides warmth and sophistication
- **Cream**: `#fef9f5` to `#f5caa5` - Background and subtle accents

### Color Usage
- **Pink shades**: Primary buttons, active states, important highlights
- **Brown shades**: Secondary elements, text, borders
- **Cream shades**: Backgrounds, cards, subtle fills

## Glassmorphism

### Glass Classes
- `.glass` - Standard glass effect (50% opacity, 20px blur)
- `.glass-strong` - Stronger glass effect (70% opacity, 30px blur)
- `.glass-card` - Glass card with gradient and inner shadow

### Properties
- Background: `rgba(255, 255, 255, 0.5)` to `rgba(255, 255, 255, 0.7)`
- Backdrop Filter: `blur(20px)` to `blur(30px)`
- Border: `1px solid rgba(255, 255, 255, 0.3)`
- Box Shadow: Custom glass shadows with pink tints

## Gradients

### Background Gradients
```css
bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100
```

### Button Gradients
```css
bg-gradient-to-r from-pink-500 via-pink-600 to-brown-500
```

### Text Gradients
```css
.gradient-text {
  background: linear-gradient(135deg, #be185d 0%, #a18072 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## Typography

### Font Family
- Primary: Inter (Google Fonts)
- Weights: 300, 400, 500, 600, 700, 800, 900

### Text Styles
- Headings: Bold (700-900), gradient-text class
- Body: Regular (400-500), brown-800 color
- Secondary: Light (300-400), brown-600 color

## Components

### Buttons

#### Primary Button
```tsx
<button className="px-10 py-5 bg-gradient-to-r from-pink-500 via-pink-600 to-brown-500 text-white rounded-2xl font-bold shadow-glass-xl hover:shadow-glass-xl transition-all">
  Button Text
</button>
```

#### Secondary Button
```tsx
<button className="px-10 py-5 glass-strong text-brown-800 rounded-2xl font-bold border-2 border-white/40 hover:border-pink-300/60 transition-all">
  Button Text
</button>
```

### Cards

#### Glass Card
```tsx
<div className="glass-card p-8 rounded-3xl">
  Card Content
</div>
```

#### Hover Effects
- Transform: `translateY(-8px)` and `scale(1.02)`
- Shadow: Increase from `shadow-glass` to `shadow-glass-lg`
- Shimmer effect on hover

### Header

#### Glassmorphic Header
```tsx
<header className="glass-strong border-b border-white/30 sticky top-0 z-50">
  Header Content
</header>
```

## Animations

### Framer Motion Variants

#### Float Animation
```tsx
animate={{ 
  y: [0, -20, 0],
  rotate: [0, 5, -5, 0]
}}
transition={{ 
  duration: 6, 
  repeat: Infinity 
}}
```

#### Scale Hover
```tsx
whileHover={{ scale: 1.05, y: -2 }}
whileTap={{ scale: 0.95 }}
```

### CSS Animations
- `animate-float`: Floating effect (6s)
- `animate-gradient`: Gradient animation (8s)
- `animate-shimmer`: Shimmer effect (2s)
- `animate-spin-slow`: Slow rotation (20s)

## 3D Elements

### Three.js Background
- Multiple geometric shapes (torus, octahedron, icosahedron, etc.)
- Particle field with 100 particles
- Multiple light sources (ambient, point, spot)
- Continuous floating and rotation animations
- Metallic materials with transparency

### Shape Properties
- Roughness: 0.1
- Metalness: 0.9
- Opacity: 0.7
- Emissive intensity: 0.2

## Spacing

### Padding
- Small: `p-4` to `p-6`
- Medium: `p-8` to `p-10`
- Large: `p-12` to `p-16`

### Margins
- Small: `mb-4` to `mb-6`
- Medium: `mb-8` to `mb-10`
- Large: `mb-12` to `mb-16`

### Gaps
- Grid/Flex: `gap-4` to `gap-8`

## Border Radius

### Rounded Corners
- Small: `rounded-2xl` (16px)
- Medium: `rounded-3xl` (24px)
- Full: `rounded-full`

## Shadows

### Glass Shadows
- `shadow-glass`: Light glass shadow
- `shadow-glass-lg`: Medium glass shadow
- `shadow-glass-xl`: Strong glass shadow

## Responsive Design

### Breakpoints
- Mobile: Default
- Tablet: `md:` (768px)
- Desktop: `lg:` (1024px)

### Grid Layouts
```tsx
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
```

## Best Practices

1. Always use glassmorphism for cards and overlays
2. Apply gradient-text to important headings
3. Use motion components for interactive elements
4. Maintain consistent spacing throughout
5. Use pink for primary actions, brown for secondary
6. Apply shimmer effect on hover for premium feel
7. Include 3D background elements for depth
8. Use rounded-3xl for modern, soft appearance
9. Apply proper z-index for layering (background: -10, content: 10, header: 50)
10. Ensure all interactive elements have hover and tap animations
