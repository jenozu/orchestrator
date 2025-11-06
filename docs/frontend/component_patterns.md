# Frontend Component Patterns

## React Component Structure

```tsx
import React from 'react';

interface ComponentProps {
  // Props interface
}

export const Component: React.FC<ComponentProps> = ({ props }) => {
  // Component logic
  return (
    <div>
      {/* JSX */}
    </div>
  );
};
```

## Component Best Practices

- Keep components focused and single-purpose
- Use TypeScript for type safety
- Extract reusable logic into custom hooks
- Compose complex components from simple ones
- Use proper prop validation

## State Management

- Use React hooks (useState, useEffect) for local state
- Use Context API for shared state
- Consider Zustand or Redux for complex state
- Avoid prop drilling

## Styling

- Use Tailwind CSS utility classes
- Create reusable component styles
- Maintain consistent design system
- Ensure responsive design

## Accessibility

- Use semantic HTML
- Include ARIA labels where needed
- Ensure keyboard navigation
- Test with screen readers

