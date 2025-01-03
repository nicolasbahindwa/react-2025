file structure:
styles/
    ├── themes/
    │   ├── _light.scss
    │   ├── _dark.scss
    │   ├── _common.scss
    │   └── _variables.scss
    ├── components/
    │   ├── _buttons.scss
    │   ├── _cards.scss
    │   └── _modals.scss
    └── main.scss
src/
  ├── assets/                          # Static files (images, fonts)
  │   ├── images/
  │   ├── styles/
  │   │   ├── global/                  # Global styles
  │   │   ├── themes/                  # Theme configurations (e.g., light/dark themes)
  │   │   └── constants/               # Global constants (e.g., color schemes, font sizes)
  │   └── fonts/
  ├── components/                      # Reusable UI components
  │   ├── shared/                      # Shared UI components across features
  │   │   ├── ui/                      # Basic UI components (buttons, inputs, etc.)
  │   │   │   ├── Button/              # Button component (with styles, tests)
  │   │   │   │   ├── Button.tsx
  │   │   │   │   ├── Button.test.tsx
  │   │   │   │   └── Button.styles.ts
  │   │   │   └── Input/
  │   │   └── layout/                  # Layout components (header, footer, sidebar)
  │   │       ├── Header/
  │   │       ├── Footer/
  │   │       └── Sidebar/
  │   ├── features/                    # Feature-specific components
  │   │   ├── UserProfile/             # User profile feature
  │   │   └── Auth/                    # Authentication feature
  │   └── hoc/                         # Higher-order components
  │       ├── withAuth.tsx             # HOC for authentication logic
  │       └── withErrorBoundary.tsx    # HOC for error boundary handling
  ├── config/                          # Configuration files
  │   ├── routes.ts                    # Route configurations
  │   ├── api.ts                       # API configurations (e.g., base URL, headers)
  │   └── constants.ts                 # Application constants
  ├── features/                        # Feature modules
  │   ├── UserProfile/                 # User Profile feature
  │   │   ├── components/              # Feature-specific components
  │   │   ├── hooks/                   # Feature-specific hooks
  │   │   ├── services/                # Feature-specific services (API, logic)
  │   │   ├── store/                   # Feature-specific store
  │   │   │   ├── userProfileSlice.ts  # Redux slice for user profile
  │   │   │   └── selectors.ts         # Redux selectors
  │   │   └── types/                   # Feature-specific types
  │   └── Auth/                        # Auth feature
  ├── layouts/                         # Layout templates
  │   ├── MainLayout/
  │   ├── AuthLayout/
  │   └── DashboardLayout/
  ├── lib/                             # Library configurations and utilities
  │   └── redux/                       # Redux setup (middleware, store)
  ├── pages/                           # Page views
  │   ├── public/                      # Public (publicly accessible) pages
  │   └── private/                     # Protected (auth-required) pages
  ├── services/                        # Application services
  │   ├── api/                         # RTK Query API services
  │   │   ├── endpoints/               # Endpoint definitions
  │   │   │   ├── userProfile.ts
  │   │   │   └── auth.ts
  │   ├── interceptors/                # HTTP interceptors (auth, error handling)
  │   └── socket/                      # WebSocket services
  ├── store/                           # Redux store setup (global state management)
  │   ├── middleware/                  # Custom Redux middleware
  │   │   ├── logger.ts
  │   │   └── analytics.ts
  │   ├── enhancers/                   # Store enhancers (e.g., redux devtools)
  │   └── rootReducer.ts               # Combine all reducers
  ├── hooks/                           # Custom hooks
  │   ├── common/                      # Shared hooks (across the app)
  │   └── api/                         # Hooks specific to API calls (e.g., `useFetch` from RTK Query)
  ├── types/                           # Type definitions
  │   ├── api/                         # API types (e.g., API response types)
  │   ├── store/                       # Store-related types (e.g., state shape, actions)
  │   └── common/                      # Shared types (e.g., form types, utility types)
  ├── utils/                           # Utility functions
  │   ├── helpers/                     # Helper functions (e.g., date formatting)
  │   ├── formatters/                  # Data formatting utilities (e.g., currency)
  │   ├── validators/                  # Validation utilities (e.g., form validation)
  │   └── testing/                     # Test utilities (e.g., mock data)
  └── context/                         # React Context Providers
      ├── ThemeContext/
      └── AuthContext/
