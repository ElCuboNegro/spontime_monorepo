# Spontime Frontend

Frontend application for Spontime - a location-based social planning platform.

## Overview

This frontend will provide interfaces for:
- User authentication and profile management
- Creating and managing spontaneous plans
- Discovering places and checking in
- Viewing personalized recommendations
- Exploring place clusters on interactive maps

## Project Structure

```
frontend/
├── src/                    # Source code
│   ├── components/        # Reusable UI components
│   ├── pages/            # Page components
│   ├── services/         # API service layer
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   ├── types/            # TypeScript type definitions
│   └── styles/           # Global styles and themes
├── features/             # BDD feature files for testing
│   ├── authentication.feature
│   ├── plans.feature
│   ├── recommendations.feature
│   ├── places.feature
│   ├── clusters.feature
│   └── profile.feature
├── public/               # Static assets
└── tests/                # Unit and integration tests
```

## Features

### Authentication & Profile
- User registration and login
- Profile management
- Privacy settings
- Friend connections

### Plans
- Create and manage plans
- Search nearby plans
- Join/leave plans
- View participants

### Places
- Browse and search places
- Check-in functionality
- View check-in history
- Add new places

### Recommendations
- Personalized place recommendations
- Category filtering
- Save for later
- Share with friends

### Clusters
- View place clusters on map
- Explore areas with multiple places
- Filter by category

## Feature Files

The `features/` directory contains BDD-style feature files that describe the expected behavior of each interface component. These serve as:

1. **Requirements Specification**: Clear description of what needs to be built
2. **Test Scenarios**: Basis for end-to-end tests
3. **Documentation**: User-facing functionality documentation

### Feature Files Included

- **authentication.feature**: User login, registration, and session management
- **plans.feature**: Plan creation, management, and participation
- **recommendations.feature**: Personalized recommendations feed
- **places.feature**: Place discovery and check-in functionality
- **clusters.feature**: Place clustering and map visualization
- **profile.feature**: User profile and settings management

## Getting Started

### Prerequisites

TBD - Will be updated once framework is chosen

### Installation

TBD - Will be updated once implementation begins

### Development

TBD - Will be updated once implementation begins

### Testing

TBD - Will be updated once implementation begins

## API Integration

The frontend will communicate with the backend API documented in [../backend/API.md](../backend/API.md).

Key endpoints:
- `/api/auth/` - Authentication
- `/api/users/` - User management
- `/api/plans/` - Plan operations
- `/api/places/` - Place discovery
- `/api/recs/` - Recommendations
- `/api/checkins/` - Check-ins
- `/api/clusters/` - Place clusters

## Technology Stack

To be determined. Potential options:
- React / Next.js
- Vue.js
- Svelte
- React Native (for mobile)

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
