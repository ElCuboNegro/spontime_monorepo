<!--
Sync Impact Report
==================
Version Change: 1.0.0 → 1.3.0
Modified Principles:
  - Principle VII (NEW): Business & UX Impact First - added to enforce feature value validation
Added Sections:
  - Frontend Stack specification updated from "To be determined" to "React Native (MANDATORY)"
  - Mobile-specific requirements added to Frontend Stack
  - Branch Strategy expanded to full Gitflow workflow with protected branches
  - Pre-Merge Requirements (NON-NEGOTIABLE) - mandatory test/build validation before PR merge
Removed Sections: N/A
Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section already references constitution
  ✅ spec-template.md - Success Criteria section aligns with business/UX impact requirement
  ✅ tasks-template.md - Task organization supports user story independence
  ⚠ plan-template.md - Mobile + API structure (Option 3) aligns with React Native mobile app
Follow-up TODOs:
  - Ratification date to be confirmed by project team
  - Update frontend/ directory structure for React Native conventions
  - Create 'develop' branch as integration branch ✅ DONE
  - Configure branch protection rules on GitHub for main and develop
  - Setup CI/CD pipeline to enforce pre-merge requirements
-->

# Spontime Constitution

## Core Principles

### I. Monorepo Architecture (NON-NEGOTIABLE)

The project MUST maintain a clear separation between backend and frontend within a unified repository structure:

- Backend code resides in `backend/` directory with Django/DRF implementation
- Frontend code resides in `frontend/` directory with interface components
- Root-level orchestration via docker-compose.yml coordinates both services
- Each subsystem MUST be independently runnable for development
- Shared resources (documentation, configuration) live at repository root

**Rationale**: Enables coordinated development across full stack while maintaining clear boundaries, simplifies dependency management, and ensures atomic cross-stack changes.

### II. BDD-Driven Development (NON-NEGOTIABLE)

All user-facing functionality MUST be specified through Behavior-Driven Development:

- Feature files MUST be written before implementation using Gherkin syntax
- Backend features use behave framework in `backend/features/`
- Frontend features use feature files in `frontend/features/`
- Each feature file MUST contain Given-When-Then scenarios
- Feature files serve as living documentation and acceptance criteria
- Implementation MUST satisfy feature scenarios before completion

**Rationale**: Ensures requirements are testable, provides clear acceptance criteria, creates executable documentation, and aligns technical implementation with user needs.

### III. API-First Design

RESTful APIs MUST be the primary interface for backend services:

- All endpoints MUST be documented in `backend/API.md`
- API responses MUST use consistent JSON structure
- Geospatial data MUST use GeoJSON format (RFC 7946)
- Authentication/authorization MUST be enforced at API layer
- APIs MUST be versioned if breaking changes are introduced
- Error responses MUST include meaningful status codes and messages

**Rationale**: Decouples frontend from backend implementation, enables mobile/web clients to share backend, facilitates API testing, and provides clear integration contracts.

### IV. Geospatial Native

Location-based features MUST use proper geospatial primitives:

- PostGIS extension MUST be used for all spatial queries
- Coordinates MUST follow [longitude, latitude] order per GeoJSON spec
- SRID 4326 (WGS 84) MUST be used for all geographic data
- Distance calculations MUST use geography types for accuracy
- Spatial indexes MUST be created for performance-critical queries

**Rationale**: Ensures accurate geographic calculations, maintains industry standard coordinate systems, and provides performant location-based queries at scale.

### V. Background Processing Architecture

Long-running and scheduled tasks MUST use asynchronous processing:

- Celery MUST be used for background task execution
- Redis MUST be used as message broker and result backend
- Periodic tasks MUST be defined using Celery Beat
- Tasks MUST be idempotent and handle failures gracefully
- Task status and errors MUST be logged for observability
- Blocking operations MUST NOT occur in web request handlers

**Rationale**: Prevents request timeouts, enables scheduled automation (clustering, recommendations), allows horizontal scaling of workers, and improves user experience through responsiveness.

### VI. Code Quality Gates (NON-NEGOTIABLE)

All code changes MUST pass quality checks before merge:

- Pre-commit hooks MUST run on every commit (Black, isort, flake8)
- Backend unit tests MUST be written using pytest
- Backend BDD tests MUST be written using behave
- Test coverage MUST be measured and tracked
- CI pipeline MUST validate all checks on pull requests
- No code bypasses quality gates without documented justification

**Rationale**: Maintains consistent code style, catches bugs early, ensures requirements are met, and reduces technical debt accumulation.

### VII. Business & UX Impact First (NON-NEGOTIABLE)

No feature SHALL be developed unless it has direct, measurable impact on business value or user experience:

- Every feature specification MUST include explicit business justification or UX improvement
- Feature proposals MUST answer: "What business metric improves?" OR "What user pain point is solved?"
- Features lacking clear business/UX impact MUST be rejected during specification phase
- Technical improvements MUST be framed as enablers for future business/UX features
- Complexity for complexity's sake is prohibited
- "Nice to have" features without measurable value are deprioritized indefinitely

**Rationale**: Ensures engineering resources focus on delivering measurable value, prevents feature bloat, maintains lean development practices, and aligns technical work with business objectives and user needs.

## Technology Stack & Constraints

### Backend Stack (MANDATORY)

- **Language**: Python 3.12+
- **Framework**: Django 5 with Django REST Framework
- **Database**: PostgreSQL with PostGIS extension
- **Task Queue**: Celery with Redis broker
- **Testing**: pytest (unit), behave (BDD)
- **Code Quality**: Black, isort, flake8 via pre-commit hooks

### Frontend Stack (MANDATORY)

- **Platform**: iOS and Android mobile applications
- **Framework**: React Native with TypeScript
- **Structure**: `frontend/` directory with React Native project structure
  - `src/` - Application source code (components, screens, services)
  - `features/` - BDD feature files for acceptance criteria
  - `tests/` - Unit and integration tests
  - `ios/` - iOS native project files
  - `android/` - Android native project files
- **State Management**: Redux Toolkit or React Context (based on complexity needs)
- **Navigation**: React Navigation
- **Maps**: react-native-maps with native map providers
- **Geolocation**: @react-native-community/geolocation
- **Testing**: Jest (unit), Detox (E2E), BDD feature files (acceptance)
- **Code Quality**: ESLint, Prettier, TypeScript strict mode
- **API Integration**: MUST consume backend REST API endpoints using Axios or Fetch
- **Deployment**:
  - iOS: App Store via Fastlane/TestFlight
  - Android: Google Play Store via Fastlane/Internal Testing

### Infrastructure

- **Containerization**: Docker with docker-compose for backend services
- **Backend Services**: PostgreSQL/PostGIS, Redis, Django API, Celery Worker, Celery Beat
- **Networking**: Backend services communicate via docker-compose network
- **Port Allocation**: Backend API 8000, DB 5432, Redis 6379
- **Mobile Development**:
  - iOS: Xcode with iOS Simulator or physical device
  - Android: Android Studio with emulator or physical device
  - Metro bundler runs on default port 8081

### Performance Requirements

- API endpoints SHOULD respond within 200ms p95 for non-geospatial queries
- Geospatial queries SHOULD respond within 500ms p95 for typical datasets
- Background tasks MUST complete within their schedule interval
- Database queries MUST use appropriate indexes for large datasets
- Mobile app SHOULD maintain 60fps during normal interactions
- Mobile app SHOULD launch in under 3 seconds on modern devices
- Map rendering SHOULD complete within 2 seconds for typical viewport

### Security Requirements

- Environment variables MUST be used for secrets (never commit .env files)
- Authentication MUST be required for user-specific endpoints
- Input validation MUST occur at API serializer layer
- SQL injection MUST be prevented via Django ORM usage
- CORS MUST be configured appropriately for mobile app access
- Mobile app MUST store sensitive tokens securely (iOS Keychain, Android Keystore)
- API communication MUST use HTTPS in production
- Location permissions MUST be explicitly requested with user-facing justification

## Development Workflow

### Feature Development Process

1. **Business Validation**: Validate feature has measurable business/UX impact (Principle VII)
2. **Specification**: Create feature specification using `/speckit.specify` command
3. **Planning**: Generate implementation plan using `/speckit.plan` command
4. **BDD Definition**: Write feature files with acceptance scenarios
5. **Task Generation**: Create tasks.md using `/speckit.tasks` command
6. **Implementation**: Execute tasks in priority order (P1 → P2 → P3)
7. **Validation**: Verify feature files pass before marking complete

### Branch Strategy (Gitflow)

**Protected Branches:**

- **`main`**: Production-ready code, protected from direct commits
- **`develop`**: Integration branch for features, stable but not production-ready

**Workflow:**

1. **Feature Development**:
   - Create feature branch from `develop`: `git checkout -b ###-feature-name develop`
   - Branch naming: `###-feature-name` format (### = issue number)
   - Develop and commit changes on feature branch
   - Push feature branch: `git push origin ###-feature-name`

2. **Integration to Develop**:
   - Create pull request: `###-feature-name` → `develop`
   - PR MUST reference feature specification
   - CI MUST pass before merge approval
   - Code review MUST verify constitution compliance
   - Merge via pull request (squash or merge commit)

3. **Release to Main**:
   - Create release branch from `develop`: `release/vX.Y.Z`
   - Perform final testing and bug fixes on release branch
   - Create pull request: `release/vX.Y.Z` → `main`
   - Tag release on `main`: `git tag vX.Y.Z`
   - Merge back to `develop` if fixes were made

4. **Hotfix Process**:
   - Create hotfix branch from `main`: `hotfix/issue-description`
   - Fix critical production issue
   - Create PR to both `main` AND `develop`
   - Tag new version on `main`

**Branch Protection Rules:**

- `main` and `develop` MUST be protected from direct commits
- All changes MUST go through pull request review
- CI/CD pipeline MUST pass before merge
- At least one approval required for PRs to `main`

### Testing Requirements

- **Backend Unit Tests**: MUST cover business logic and models (pytest)
- **Backend Integration Tests**: MUST verify API endpoint contracts
- **Backend BDD Tests**: MUST validate user scenarios from feature files (behave)
- **Mobile Unit Tests**: MUST cover business logic and utilities (Jest)
- **Mobile E2E Tests**: SHOULD cover critical user flows (Detox)
- **Mobile Manual Testing**: SHOULD test on both iOS and Android devices
- **Manual Testing**: SHOULD follow quickstart.md validation steps

### Documentation Requirements

- Feature specifications MUST live in `.specify/` directory
- API changes MUST be documented in `backend/API.md`
- Architectural decisions MUST be captured in implementation plans
- README files MUST be kept current for backend and frontend

### Code Review Requirements

- All changes MUST go through pull request review
- Reviewer MUST verify constitution compliance (especially Principle VII: Business/UX Impact)
- Feature proposals without clear business/UX impact MUST be rejected
- Complexity additions MUST be justified in plan.md Complexity Tracking section
- Breaking changes MUST include migration plan
- Mobile UI changes SHOULD include screenshots for iOS and Android

### Pre-Merge Requirements (NON-NEGOTIABLE)

Before ANY pull request can be merged, the following MUST pass:

**Backend Validation:**

- All unit tests MUST pass: `cd backend && pytest`
- All BDD tests MUST pass: `cd backend && behave`
- Backend build MUST succeed: `docker-compose build backend`
- No test failures or errors are acceptable

**Mobile Validation (when applicable):**

- Mobile unit tests MUST pass: `cd frontend && npm test`
- TypeScript compilation MUST succeed: `cd frontend && npx tsc --noEmit`
- Linting MUST pass: `cd frontend && npm run lint`

**CI/CD Pipeline:**

- All automated CI checks MUST be green
- No bypassing of automated checks is permitted
- Failed tests MUST be fixed before merge, not after

**Exception Process:**

- If tests are temporarily broken due to infrastructure issues (not code issues), document in PR
- Requires explicit approval from at least two reviewers
- Issue MUST be created to track test fix with immediate priority

## Governance

### Constitution Authority

This constitution supersedes all other development practices and coding standards. When conflicts arise between this document and other guidance, this constitution takes precedence.

### Amendment Process

Constitution amendments require:

1. Documented rationale for the change
2. Impact analysis on existing code and templates
3. Version bump following semantic versioning (MAJOR.MINOR.PATCH)
4. Update of dependent templates and documentation
5. Team approval before finalization

### Version Bump Rules

- **MAJOR**: Backward-incompatible principle removals or redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review

- All pull requests MUST verify alignment with core principles
- Constitution violations MUST be called out in code review
- Justified violations MUST be documented in Complexity Tracking
- Templates MUST reference constitution checks where applicable

### Guidance Files

- Use `.specify/templates/` for consistent feature workflows
- Use `backend/API.md` for API contract reference
- Use `README.md` files for setup and operational guidance
- Use feature specifications in `.specify/` for requirements truth

**Version**: 1.3.0 | **Ratified**: TODO(RATIFICATION_DATE): Confirm with project team | **Last Amended**: 2025-01-05
