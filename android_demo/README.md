# Spontime Android Demo App

A demonstration Android application for the Spontime API, showcasing authentication and core API functionality.

## Features

- **User Registration** - Create new accounts
- **User Login** - Authenticate with existing credentials
- **View Plans** - Browse all available plans
- **Create Plans** - Create new social plans
- **Profile Viewing** - View authenticated user profile
- **Logout** - Securely logout and clear tokens

## Technologies

- **Language**: Kotlin
- **Minimum SDK**: Android 7.0 (API 24)
- **Target SDK**: Android 14 (API 34)
- **Architecture**: MVVM-inspired
- **Networking**: Retrofit + OkHttp
- **UI**: Material Design 3
- **Async**: Kotlin Coroutines

## Prerequisites

1. **Android Studio**: Latest stable version (Hedgehog or later)
2. **JDK**: Version 17 or higher
3. **Running Backend**: Django backend must be running on `http://localhost:8000`

## Setup Instructions

### 1. Backend Setup

First, ensure the Django backend is running:

```bash
cd /path/to/spontime_monorepo

# Run migrations (first time only)
python manage.py migrate

# Start the development server
python manage.py runserver
```

### 2. Open in Android Studio

1. Open Android Studio
2. Select "Open an existing project"
3. Navigate to `spontime_monorepo/android_demo`
4. Wait for Gradle sync to complete

### 3. Run on Emulator

The app is configured to connect to `http://10.0.2.2:8000/api/` which is the emulator's way of accessing `localhost` on the host machine.

1. Create an Android Virtual Device (AVD) if you don't have one:
   - Tools → Device Manager → Create Device
   - Select a device (e.g., Pixel 5)
   - Download a system image (API 34 recommended)
   - Finish setup

2. Click the "Run" button (green triangle) in Android Studio
3. Select your emulator
4. Wait for the app to install and launch

### 4. Run on Physical Device

To run on a physical Android device:

1. Enable Developer Options on your device
2. Enable USB Debugging
3. Connect device via USB
4. Update `app/build.gradle` to point to your computer's IP:
   ```gradle
   buildConfigField "String", "API_BASE_URL", "\"http://YOUR_IP:8000/api/\""
   ```
5. Ensure your device and computer are on the same network
6. Run the app from Android Studio

## App Structure

```
android_demo/
├── app/
│   ├── src/main/
│   │   ├── java/com/spontime/demo/
│   │   │   ├── api/
│   │   │   │   ├── ApiModels.kt          # Data models
│   │   │   │   ├── ApiService.kt         # API interface
│   │   │   │   └── RetrofitClient.kt     # Network client
│   │   │   ├── LoginActivity.kt          # Login/Register screen
│   │   │   └── DashboardActivity.kt      # Main screen
│   │   ├── res/
│   │   │   ├── layout/                   # UI layouts
│   │   │   └── values/                   # Strings, colors, themes
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
├── settings.gradle
└── README.md
```

## Using the App

### Registration

1. Launch the app
2. Tap "Don't have account? Register"
3. Enter email, username, and password
4. Tap "Register"
5. You'll be automatically logged in and taken to the dashboard

### Login

1. Launch the app
2. Enter your email and password
3. Tap "Login"
4. You'll be taken to the dashboard

### Dashboard

- **View Plans**: Scroll through the list of plans
- **Refresh**: Pull down to refresh the list
- **Create Plan**: Tap the + button (FAB) to create a new plan
- **View Profile**: Tap "Profile" in the header to see your user info
- **Logout**: Tap "Logout" to sign out

## API Endpoints Used

The app demonstrates the following API endpoints:

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `GET /api/plans/` - List all plans
- `POST /api/plans/` - Create a new plan

## Configuration

### Change API Base URL

Edit `app/build.gradle`:

```gradle
buildConfigField "String", "API_BASE_URL", "\"https://your-api.com/api/\""
```

### Enable/Disable Logging

HTTP request/response logging is enabled by default. To disable, edit `RetrofitClient.kt`:

```kotlin
private val loggingInterceptor = HttpLoggingInterceptor().apply {
    level = HttpLoggingInterceptor.Level.NONE  // Change to NONE
}
```

## Troubleshooting

### Cannot connect to backend

**Error**: `Failed to connect to /10.0.2.2:8000`

**Solutions**:
1. Ensure Django backend is running: `python manage.py runserver`
2. Check backend logs for any errors
3. Try accessing `http://localhost:8000/api/` in your browser
4. If on physical device, use your computer's IP instead of `10.0.2.2`

### Network Security Exception

**Error**: `Cleartext HTTP traffic not permitted`

**Solution**: Already handled in `AndroidManifest.xml` with `android:usesCleartextTraffic="true"`. For production, use HTTPS.

### Build Errors

1. Sync Gradle: File → Sync Project with Gradle Files
2. Clean Build: Build → Clean Project, then Build → Rebuild Project
3. Invalidate Caches: File → Invalidate Caches / Restart

### Token Persistence

Tokens are stored in SharedPreferences and persist across app restarts. To clear:
- Logout from the app, or
- Uninstall and reinstall the app

## Future Enhancements

- [ ] Instagram OAuth integration
- [ ] Push notifications
- [ ] Real-time messaging
- [ ] Map view for plans
- [ ] Plan filtering and search
- [ ] User profiles with photos
- [ ] Plan attendee management
- [ ] Check-in functionality

## Security Notes

- This is a **demo application** for development purposes
- Uses cleartext HTTP traffic (not secure for production)
- Stores auth tokens in SharedPreferences (consider encrypted storage for production)
- No certificate pinning or advanced security measures
- For production, implement HTTPS, encrypted storage, and proper security practices

## License

This demo app is part of the Spontime project.
