# Frontend Development Rules (Next.js)

## Path: frontend/**/*.{ts,tsx}

## CRITICAL: Design System Compliance

**YOU MUST follow GiGi design system:**

**Colors**:
- Primary BG: `#f5f5eb` (cream)
- Accent: `#c4ff0e` (lime green)
- Text: `#000000` (black)
- Secondary text: `#555555`

**Buttons**:
- Primary: Lime green fill, black text, `border-radius: 9999px`
- Secondary: Transparent, 2px black border, pill-shaped
- Padding: `16px 32px`

**Cards**:
- Background: `#ffffff`
- Border: `1px solid #e0e0d8`
- Radius: `16px`
- Padding: `48px`

**IMPORTANT**: No generic Tailwind designs. Follow GiGi aesthetic.

## Component Structure

**YOU MUST**:
- One component per file
- Props interface above component
- Destructure props in parameters
- Function components only (no classes)

**Example**:
```tsx
interface ProductCardProps {
  product: Product;
  onEdit: (id: number) => void;
}

export function ProductCard({ product, onEdit }: ProductCardProps) {
  return (
    <div className="bg-white rounded-2xl p-12 border border-warm-gray">
      {/* Component content */}
    </div>
  );
}
```

## State Management

**YOU MUST use Zustand for global state:**

```tsx
// stores/authStore.ts
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));

// Component usage with selector
const userName = useAuthStore((s) => s.user?.name);
```

**NEVER**: Use Redux or Context API for complex state.

## API Client Pattern

**IMPORTANT**: All API calls through centralized client:

```tsx
// lib/api.ts
export const api = {
  posts: {
    list: () => fetch(`${API_URL}/api/posts`).then(r => r.json()),
    get: (id: number) => fetch(`${API_URL}/api/posts/${id}`).then(r => r.json()),
  },
};

// Component usage
const { data } = useQuery({ queryKey: ['posts'], queryFn: api.posts.list });
```

## Error Handling

**YOU MUST handle ALL async errors:**

```tsx
try {
  await api.posts.create(data);
  toast.success("Post created!");
} catch (error) {
  toast.error(error.message || "Failed to create post");
  console.error("Create post error:", error);
}
```

**NEVER**: Leave unhandled promise rejections.

## Routing (Next.js App Router)

**Structure**:
```
app/
├── page.tsx              # Home
├── dashboard/
│   └── page.tsx          # Dashboard
├── posts/
│   └── [id]/
│       └── page.tsx      # Post detail
└── auth/
    └── callback/
        └── page.tsx      # OAuth callback
```

**IMPORTANT**: Use dynamic routes `[id]` for detail pages.

## Performance

**YOU MUST**:
- Lazy load routes: `const Dashboard = lazy(() => import('./Dashboard'))`
- Optimize images: Use Next.js `<Image>` component
- Virtualize long lists: Use `react-window` for >100 items

**NEVER**: Load all data at once. Use pagination.

## TypeScript Strictness

**YOU MUST**:
- Enable `strict: true` in tsconfig
- No `any` types (use `unknown` with type guards)
- Export types used by other files
- Type all function return values

**NEVER**: Use `// @ts-ignore` without explanation comment.

## Accessibility

**YOU MUST**:
- Minimum 44px touch targets
- 2px lime green focus outline
- ARIA labels for icon buttons
- Keyboard navigation support

**Test**: Tab through entire page to verify navigation.
