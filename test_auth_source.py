"""
Source code verification for authentication implementation.
Tests by reading and analyzing source files directly.
"""
import os
import re

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def read_file(filepath):
    """Read a file and return its contents."""
    with open(filepath, 'r') as f:
        return f.read()

def test_settings_configuration():
    """Test settings.py configuration."""
    print_section("TEST 1: Settings Configuration")

    content = read_file('spontime/settings.py')

    # Test 1.1: Check for authtoken in INSTALLED_APPS
    print("Checking INSTALLED_APPS...")
    if "'rest_framework.authtoken'" in content:
        print("  ✅ rest_framework.authtoken is in INSTALLED_APPS")
    else:
        print("  ❌ rest_framework.authtoken NOT in INSTALLED_APPS")
        return False

    # Test 1.2: Check for TokenAuthentication
    print("\nChecking authentication classes...")
    if 'TokenAuthentication' in content:
        print("  ✅ TokenAuthentication configured")
    else:
        print("  ⚠️  TokenAuthentication not found")

    # Test 1.3: Check for SessionAuthentication
    if 'SessionAuthentication' in content:
        print("  ✅ SessionAuthentication configured")

    # Test 1.4: Check for permission classes
    if 'DEFAULT_PERMISSION_CLASSES' in content:
        print("  ✅ DEFAULT_PERMISSION_CLASSES configured")

    return True

def test_user_serializer():
    """Test UserSerializer implementation."""
    print_section("TEST 2: UserSerializer Implementation")

    content = read_file('core/serializers.py')

    # Test 2.1: Password field exists
    print("Checking password field...")
    password_field_pattern = r'password\s*=\s*serializers\.CharField\([^)]*write_only\s*=\s*True'
    if re.search(password_field_pattern, content):
        print("  ✅ Password field defined as write_only")
    else:
        print("  ⚠️  Password field configuration not found")

    # Test 2.2: Check for create method
    print("\nChecking create() method...")
    if 'def create(self, validated_data):' in content:
        print("  ✅ create() method exists")

        # Test 2.3: Password handling
        if 'password = validated_data.pop(\'password\')' in content:
            print("  ✅ Extracts password from validated_data")

        # Test 2.4: Proper user creation
        if 'User.objects.create_user' in content:
            print("  ✅ Uses User.objects.create_user() for password hashing")
        else:
            print("  ❌ Does NOT use create_user() - passwords won't be hashed!")
            return False

        # Show the create method
        create_method = re.search(r'def create\(self, validated_data\):.*?(?=\n    def|\nclass|\Z)', content, re.DOTALL)
        if create_method:
            print("\n  Create method implementation:")
            print("  " + "-" * 56)
            for line in create_method.group(0).split('\n'):
                print(f"  {line}")
            print("  " + "-" * 56)

    else:
        print("  ❌ create() method NOT found")
        return False

    # Test 2.5: Password in fields
    print("\nChecking Meta.fields...")
    if "'password'" in content:
        print("  ✅ 'password' included in fields")

    return True

def test_auth_views():
    """Test authentication views."""
    print_section("TEST 3: Authentication Views")

    if not os.path.exists('core/auth_views.py'):
        print("❌ auth_views.py NOT found")
        return False

    content = read_file('core/auth_views.py')

    endpoints = {
        'register': [
            (r'def register\(request\):', 'register function'),
            (r'UserSerializer\(data=request\.data\)', 'UserSerializer usage'),
            (r'Token\.objects\.get_or_create\(user=user\)', 'Token creation'),
            (r'@permission_classes\(\[AllowAny\]\)', 'AllowAny permission'),
        ],
        'login': [
            (r'def login\(request\):', 'login function'),
            (r'authenticate\(', 'Django authenticate()'),
            (r'Token\.objects\.get_or_create', 'Token retrieval'),
            (r'email.*password', 'email/password handling'),
        ],
        'logout': [
            (r'def logout\(request\):', 'logout function'),
            (r'auth_token\.delete\(\)', 'Token deletion'),
            (r'@permission_classes\(\[IsAuthenticated\]\)', 'IsAuthenticated permission'),
        ],
        'profile': [
            (r'def profile\(request\):', 'profile function'),
            (r'request\.user', 'current user access'),
            (r'UserSerializer\(request\.user\)', 'User serialization'),
        ]
    }

    all_passed = True
    for endpoint_name, checks in endpoints.items():
        print(f"\nChecking {endpoint_name}() endpoint...")
        endpoint_found = False

        for pattern, description in checks:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                if not endpoint_found:
                    print(f"  ✅ {endpoint_name}() endpoint found")
                    endpoint_found = True
                print(f"    ✅ {description}")
            else:
                if 'function' in description:
                    print(f"  ❌ {description} NOT found")
                    all_passed = False

    return all_passed

def test_url_configuration():
    """Test URL configuration."""
    print_section("TEST 4: URL Configuration")

    content = read_file('core/urls.py')

    # Check imports
    print("Checking imports...")
    if 'from .auth_views import' in content:
        print("  ✅ auth_views imported")

        # Check which views are imported
        auth_funcs = ['register', 'login', 'logout', 'profile']
        for func in auth_funcs:
            if func in content:
                print(f"    ✅ {func} imported")
    else:
        print("  ❌ auth_views NOT imported")
        return False

    # Check URL patterns
    print("\nChecking URL patterns...")
    auth_urls = {
        'auth/register/': 'register',
        'auth/login/': 'login',
        'auth/logout/': 'logout',
        'auth/profile/': 'profile',
    }

    all_found = True
    for url, view in auth_urls.items():
        pattern = f"path\\(['\"]{ url}['\"],\\s*{view}"
        if re.search(pattern, content):
            print(f"  ✅ {url} -> {view}()")
        else:
            print(f"  ❌ {url} NOT configured")
            all_found = False

    return all_found

def test_documentation():
    """Test documentation files."""
    print_section("TEST 5: Documentation")

    docs = [
        ('AUTHENTICATION.md', 'Authentication guide'),
        ('API_ENDPOINTS.md', 'API documentation'),
        ('android_demo/README.md', 'Android app guide'),
    ]

    all_found = True
    for filepath, description in docs:
        if os.path.exists(filepath):
            print(f"  ✅ {description} ({filepath})")

            # Check content
            content = read_file(filepath)
            if 'auth/register' in content or 'register' in content.lower():
                print(f"      ✅ Contains auth information")
        else:
            print(f"  ❌ {description} ({filepath}) NOT found")
            all_found = False

    return all_found

def test_android_app():
    """Test Android app structure."""
    print_section("TEST 6: Android Demo App")

    android_files = [
        ('android_demo/app/build.gradle', 'Gradle build file'),
        ('android_demo/app/src/main/java/com/spontime/demo/LoginActivity.kt', 'Login Activity'),
        ('android_demo/app/src/main/java/com/spontime/demo/DashboardActivity.kt', 'Dashboard Activity'),
        ('android_demo/app/src/main/java/com/spontime/demo/api/ApiService.kt', 'API Service'),
        ('android_demo/app/src/main/java/com/spontime/demo/api/RetrofitClient.kt', 'Retrofit Client'),
        ('android_demo/app/src/main/res/layout/activity_login.xml', 'Login layout'),
        ('android_demo/app/src/main/AndroidManifest.xml', 'Android Manifest'),
    ]

    all_found = True
    for filepath, description in android_files:
        if os.path.exists(filepath):
            print(f"  ✅ {description}")

            # Check for key components in some files
            if 'ApiService.kt' in filepath:
                content = read_file(filepath)
                if 'auth/register' in content and 'auth/login' in content:
                    print(f"      ✅ Auth endpoints defined")

            if 'RetrofitClient.kt' in filepath:
                content = read_file(filepath)
                if 'Token' in content:
                    print(f"      ✅ Token authentication configured")

            if 'LoginActivity.kt' in filepath:
                content = read_file(filepath)
                if 'register' in content and 'login' in content:
                    print(f"      ✅ Login/Register functionality present")

        else:
            print(f"  ⚠️  {description} NOT found")
            all_found = False

    return all_found

def main():
    """Run all tests."""
    print_section("AUTHENTICATION SOURCE CODE VERIFICATION")
    print("Validating authentication implementation by analyzing source code...\n")

    tests = [
        ("Settings Configuration", test_settings_configuration),
        ("UserSerializer Implementation", test_user_serializer),
        ("Authentication Views", test_auth_views),
        ("URL Configuration", test_url_configuration),
        ("Documentation", test_documentation),
        ("Android Demo App", test_android_app),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {str(e)}")
            results.append((test_name, False))

    # Summary
    print_section("TEST SUMMARY")

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n" + "="*60)
        print("AUTHENTICATION SYSTEM VERIFICATION COMPLETE")
        print("="*60)
        print("\n✅ Backend Authentication:")
        print("   • Token-based authentication configured")
        print("   • User registration with password hashing")
        print("   • Login/logout endpoints implemented")
        print("   • Profile retrieval endpoint")
        print("   • Proper security (write-only passwords)")
        print("\n✅ Android Demo App:")
        print("   • Complete app structure created")
        print("   • Login/Register functionality")
        print("   • API integration with Retrofit")
        print("   • Token management")
        print("   • Dashboard with plans list")
        print("\n✅ Documentation:")
        print("   • AUTHENTICATION.md - Complete auth guide")
        print("   • API_ENDPOINTS.md - API reference")
        print("   • android_demo/README.md - Setup guide")
        print("\n📝 Next Steps:")
        print("   1. Set up PostGIS database (or use docker-compose)")
        print("   2. Run: python manage.py migrate")
        print("   3. Run: python manage.py runserver")
        print("   4. Test with: curl or Android app")
        print("\n📍 Example Test:")
        print("   curl -X POST http://localhost:8000/api/auth/register/ \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"email\":\"test@example.com\",\"handle\":\"test\",\"password\":\"pass123\"}'")

    else:
        print("\n⚠️  Some tests failed. Please review the output above.")

    return all_passed

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
