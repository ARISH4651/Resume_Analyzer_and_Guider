<!--# Flutter Installation Guide for Windows

## Option 1: Install Flutter (Recommended)

### Step 1: Download Flutter SDK
1. Visit: https://docs.flutter.dev/get-started/install/windows
2. Download Flutter SDK (latest stable version)
3. Extract to: `C:\src\flutter` (or your preferred location)

### Step 2: Add Flutter to PATH
```powershell
# Open PowerShell as Administrator and run:
$env:Path += ";C:\src\flutter\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::User)
```

Or manually:
1. Search "Environment Variables" in Windows
2. Edit "Path" under User Variables
3. Add: `C:\src\flutter\bin`
4. Click OK

### Step 3: Verify Installation
```powershell
flutter doctor
```

### Step 4: Install Android Studio (for Android development)
1. Download: https://developer.android.com/studio
2. Install Android SDK
3. Configure emulator

### Step 5: Run Flutter Doctor
```powershell
flutter doctor --android-licenses
flutter doctor
```

---

## Option 2: Quick Test Without Installation

Since your backend is ready, you can test the API functionality first:

### Test Backend API:
```powershell
cd "D:\project\ML PROJECTS\Resume App\backend_api"
..\venv\Scripts\Activate.ps1
python main.py
```

Then test endpoints at: http://localhost:8000/docs

---

## Option 3: Use Flutter Online (Quick Demo)

1. Visit: https://dartpad.dev
2. Create new Flutter project
3. Copy your code from `mobile_app/lib/`
4. Test UI instantly in browser

---

## Current Status Check:

Run this to check if Flutter is already installed somewhere:
```powershell
where.exe flutter
```

If found, add that path to your environment variables.

---

## Recommended Next Steps:

1. **For full mobile development:**
   - Install Flutter SDK (15-20 minutes)
   - Install Android Studio (30 minutes)
   - Set up emulator (10 minutes)

2. **For quick backend testing:**
   - Start FastAPI backend
   - Test with Postman or curl
   - Frontend can wait

3. **For rapid UI testing:**
   - Use DartPad online
   - No installation needed
   - See UI immediately

Which option would you like to proceed with?
