# GitHub Actions Permissions Fix

## Problem
The GitHub Actions workflow was failing with a 403 error when trying to create releases:
```
Resource not accessible by integration
```

## Root Causes
1. **Missing permissions** - The `GITHUB_TOKEN` didn't have `contents: write` permission
2. **Invalid parameter** - The `overwrite` parameter is not valid for `softprops/action-gh-release@v2`
3. **Main branch releases** - Trying to create releases for main branch pushes without proper tags

## Fixes Applied

### 1. Added Required Permissions
```yaml
permissions:
  contents: write
```

### 2. Removed Invalid Parameter
- Removed `overwrite: ${{ github.ref == 'refs/heads/main' }}` (not supported)

### 3. Simplified Release Strategy
- **Triggers only on tags** (e.g., `v1.0.0`, `v2.1.3`)
- **Manual trigger** via `workflow_dispatch`
- **No main branch releases** (simplified approach)

## How to Create Releases

### For Official Releases
```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
# → Automatically triggers build and creates release
```

### For Manual Builds
1. Go to GitHub Actions tab
2. Select "Build macOS DMG" workflow
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Workflow Features
- ✅ **Builds macOS app** with PyInstaller
- ✅ **Creates DMG installer** with proper app bundle
- ✅ **Uploads artifacts** for download
- ✅ **Creates GitHub release** with DMG attached
- ✅ **Includes installation instructions**
- ✅ **Handles security warnings**

## Files Modified
- `.github/workflows/build-macos.yml` - Fixed permissions and parameters

## Result
The GitHub Actions workflow now works properly and will create releases when you push version tags!
