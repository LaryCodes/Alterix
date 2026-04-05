# Alterix UI Consistency Guide

## Overview
This guide ensures complete design consistency across the entire Alterix application.

## Reusable Components

### 1. Layout Components

#### DashboardLayout (`/components/layout/DashboardLayout.tsx`)
- Wraps all dashboard pages
- Includes DashboardHeader automatically
- Provides consistent background and container

**Usage:**
```tsx
import DashboardLayout from '@/components/layout/DashboardLayout'

export default function MyPage() {
  return (
    <DashboardLayout>
      {/* Your content */}
    </DashboardLayout>
  )
}
```

#### DashboardHeader (`/components/layout/DashboardHeader.tsx`)
- Consistent glassmorphic header
- Active state highlighting
- Responsive navigation
- Automatic user display
- Logout functionality

### 2. UI Components

#### Button (`/components/ui/Button.tsx`)
**Variants:**
- `primary`: Pink-to-brown gradient
- `secondary`: Glass effect with border
- `ghost`: Transparent with hover

**Sizes:**
- `sm`: Small (px-4 py-2)
- `md`: Medium (px-6 py-3)
- `lg`: Large (px-10 py-5)

**Usage:**
```tsx
<Button variant="primary" size="lg" onClick={handleClick}>
  Click Me
</Button>
```

#### GlassCard (`/components/ui/GlassCard.tsx`)
**Props:**
- `gradient`: Use glass-card with gradient
- `hover`: Enable hover effects
- `onClick`: Make clickable

**Usage:**
```tsx
<GlassCard className="p-6" gradient hover>
  Card content
</GlassCard>
```

#### StatCard (`/components/ui/StatCard.tsx`)
**Props:**
- `icon`: Emoji icon
- `value`: Stat value
- `label`: Stat label
- `gradient`: Gradient accent color
- `delay`: Animation delay

**Usage:**
```tsx
<StatCard
  icon="🎯"
  value="42"
  label="Skills"
  gradient="from-pink-400 to-pink-600"
  delay={0.1}
/>
```

#### LoadingSpinner (`/components/ui/LoadingSpinner.tsx`)
**Props:**
- `size`: 'sm' | 'md' | 'lg'
- `fullScreen`: Show full-screen loader

**Usage:**
```tsx
<LoadingSpinner fullScreen />
```

#### EmptyState (`/components/ui/EmptyState.tsx`)
**Props:**
- `icon`: Large emoji
- `title`: Main message
- `description`: Supporting text
- `action`: Optional action button

**Usage:**
```tsx
<EmptyState
  icon="📚"
  title="No items yet"
  description="Get started by adding your first item"
  action={<Button>Add Item</Button>}
/>
```

## Design Tokens

### Colors
```tsx
// Primary Actions
from-pink-500 to-brown-500

// Text
text-brown-900  // Headings
text-brown-800  // Body
text-brown-600  // Secondary

// Backgrounds
bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100
```

### Glassmorphism
```tsx
// Standard
glass

// Strong (headers, cards)
glass-strong

// With gradient
glass-card
```

### Spacing
```tsx
// Padding
p-6   // Cards
p-8   // Sections
p-10  // Forms

// Margins
mb-6  // Between elements
mb-8  // Between sections

// Gaps
gap-4  // Small
gap-6  // Medium
gap-8  // Large
```

### Border Radius
```tsx
rounded-2xl   // Standard (16px)
rounded-3xl   // Large (24px)
rounded-full  // Pills/Circles
```

## Page Structure

### Dashboard Pages
```tsx
import DashboardLayout from '@/components/layout/DashboardLayout'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

export default function Page() {
  const [loading, setLoading] = useState(true)
  
  if (loading) {
    return <LoadingSpinner fullScreen />
  }
  
  return (
    <DashboardLayout>
      {/* Page content */}
    </DashboardLayout>
  )
}
```

### Auth Pages
```tsx
// Consistent structure:
- Animated background blobs
- Glass-strong card
- Gradient decorative border
- Form with glass inputs
- Button component
- Link to other auth page
- Decorative elements
```

## Animation Patterns

### Hover Effects
```tsx
whileHover={{ scale: 1.05, y: -2 }}
whileTap={{ scale: 0.95 }}
```

### Page Entry
```tsx
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ delay: 0.1 }}
```

### Icon Animations
```tsx
animate={{ rotate: [0, 10, -10, 0] }}
transition={{ duration: 3, repeat: Infinity }}
```

## Consistency Checklist

### Every Dashboard Page Must Have:
- [ ] DashboardLayout wrapper
- [ ] LoadingSpinner for loading states
- [ ] EmptyState for empty data
- [ ] Button components (not raw buttons)
- [ ] GlassCard for content sections
- [ ] Consistent spacing (gap-6, mb-8)
- [ ] Gradient text for headings

### Every Form Must Have:
- [ ] Glass inputs with consistent styling
- [ ] Button component for submit
- [ ] Error display with glass card
- [ ] Loading state with spinner
- [ ] Consistent padding (px-5 py-3/4)

### Every Card Must Have:
- [ ] GlassCard component or glass-card class
- [ ] Rounded-3xl corners
- [ ] Hover effects (whileHover)
- [ ] Shimmer effect on hover (optional)
- [ ] Consistent padding (p-6 or p-8)

## Common Patterns

### Section Header
```tsx
<div className="mb-8">
  <h2 className="text-3xl font-bold gradient-text mb-2">Title</h2>
  <p className="text-brown-600">Description</p>
</div>
```

### Action Bar
```tsx
<div className="flex items-center justify-between mb-8">
  <div>
    <h2 className="text-3xl font-bold gradient-text mb-2">Title</h2>
    <p className="text-brown-600">Description</p>
  </div>
  <Button variant="primary" size="lg">Action</Button>
</div>
```

### Grid Layout
```tsx
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map((item) => (
    <GlassCard key={item.id} gradient>
      {/* Content */}
    </GlassCard>
  ))}
</div>
```

### List Layout
```tsx
<div className="space-y-6">
  {items.map((item) => (
    <GlassCard key={item.id}>
      {/* Content */}
    </GlassCard>
  ))}
</div>
```

## File Organization

```
frontend/
├── components/
│   ├── layout/
│   │   ├── DashboardLayout.tsx
│   │   └── DashboardHeader.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── GlassCard.tsx
│   │   ├── StatCard.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── EmptyState.tsx
│   └── three/
│       └── ThreeBackground.tsx
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── skills/page.tsx
│   │   ├── matches/page.tsx
│   │   └── exchanges/page.tsx
│   ├── globals.css
│   └── layout.tsx
└── lib/
    ├── auth.ts
    └── api.ts
```

## Best Practices

1. **Always use components** - Never create raw buttons or cards
2. **Consistent spacing** - Use gap-6 for grids, mb-8 for sections
3. **Loading states** - Always show LoadingSpinner
4. **Empty states** - Always show EmptyState when no data
5. **Animations** - Use Framer Motion for all interactions
6. **Glassmorphism** - Use glass classes, not custom styles
7. **Colors** - Use design tokens, not arbitrary colors
8. **Typography** - Use gradient-text for headings
9. **Responsive** - Always use md: and lg: breakpoints
10. **Accessibility** - Proper labels, ARIA attributes, keyboard navigation

## Migration Guide

### Converting Old Pages

1. Replace layout wrapper with DashboardLayout
2. Replace loading div with LoadingSpinner
3. Replace empty div with EmptyState
4. Replace buttons with Button component
5. Replace cards with GlassCard
6. Update colors to design tokens
7. Add consistent spacing
8. Add animations

### Example:
```tsx
// Before
<div className="bg-white/60 p-4 rounded-xl">
  <button className="px-4 py-2 bg-blue-500">Click</button>
</div>

// After
<GlassCard className="p-6">
  <Button variant="primary" size="md">Click</Button>
</GlassCard>
```

## Testing Consistency

Run through this checklist for each page:
1. Does it use DashboardLayout?
2. Are all buttons using Button component?
3. Are all cards using GlassCard?
4. Is the header consistent?
5. Are colors from design tokens?
6. Is spacing consistent?
7. Are animations smooth?
8. Does it look premium?
9. Is it responsive?
10. Is glassmorphism applied correctly?
