# Release Automation Setup

## Overview
GitHub Actions now automatically creates releases when:
1. **Pushes to main branch** - Creates/updates a "latest" release
2. **Tag pushes** - Creates a versioned release (e.g., v1.0.0)

## How It Works

### Main Branch Pushes
- **Trigger**: Every push to `main` branch
- **Release**: Creates/updates "latest" release
- **DMG Name**: `Simple Editor-latest.dmg`
- **Type**: Stable release (not prerelease)

### Tag Pushes
- **Trigger**: Pushes with tags like `v1.0.0`, `v2.1.3`, etc.
- **Release**: Creates versioned release
- **DMG Name**: `Simple Editor-v1.0.0.dmg`
- **Type**: Stable release (not prerelease)

## Workflow Features

### Automatic Build
- Uses `build_simple_macos.sh` for consistent builds
- Creates DMG with proper app bundle
- Includes app icon and Info.plist

### Release Management
- **Overwrite**: Main branch releases overwrite the "latest" release
- **Versioning**: Tag releases create new versioned releases
- **Artifacts**: DMG files are uploaded as release assets

### User Instructions
Each release includes:
- Installation instructions
- System requirements
- Security warning bypass instructions
- Feature list

## Usage

### For Development
```bash
# Push to main branch
git push origin main
# → Creates/updates "latest" release automatically
```

### For Releases
```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0
# → Creates "v1.0.0" release automatically
```

## Benefits
- ✅ **Automatic**: No manual release creation needed
- ✅ **Consistent**: Same build process every time
- ✅ **User-friendly**: Clear installation instructions
- ✅ **Versioned**: Proper version management
- ✅ **Latest**: Always have a "latest" release for main branch

## Files Modified
- `.github/workflows/build-macos.yml` - Updated workflow
- `build_simple_macos.sh` - Simple build script
- `RELEASE_AUTOMATION.md` - This documentation
