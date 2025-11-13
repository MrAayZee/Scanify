# Update System for Private Repositories

## How It Works

Since this repository is **private**, the standard GitHub Releases API won't work without authentication. Instead, we use a simpler approach with a `version.json` file.

### For Users

- The app checks `version.json` on GitHub to see if a new version is available
- Works with both public and private repositories
- No authentication needed
- Automatic check on startup + manual check button

### For Developers (Releasing Updates)

When you want to release a new version:

#### Step 1: Update Version Files

1. Update `VERSION` in `scanify.py`:

   ```python
   VERSION = "1.0.1"  # Change this
   ```

2. Update `version.json`:
   ```json
   {
     "version": "1.0.1",
     "release_date": "2025-11-13",
     "download_url": "https://github.com/MrAayZee/Scanify/releases/latest",
     "changelog": ["Fixed bug X", "Added feature Y", "Improved performance"]
   }
   ```

#### Step 2: Commit and Tag

```powershell
git add scanify.py version.json
git commit -m "Release v1.0.1"
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin main
git push origin v1.0.1
```

#### Step 3: Create GitHub Release

1. Go to: https://github.com/MrAayZee/Scanify/releases
2. Click "Draft a new release"
3. Choose tag `v1.0.1`
4. Add release notes
5. **Upload the installer** (.exe file from `installer_output/`)
6. Publish release

### Making Repository Public (Optional)

If you want to make the repo public so others can contribute:

1. Go to: https://github.com/MrAayZee/Scanify/settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" → "Make public"

The update checker will work either way!

### Distribution Options

#### Option 1: Private Repo + Releases

- Keep code private
- Users download from Releases page (must be collaborators or you share direct link)
- Update checker works via `version.json`

#### Option 2: Public Repo

- Code visible to everyone
- Anyone can download from Releases
- Users can contribute via pull requests
- Update checker works the same way

#### Option 3: Separate Distribution Repo

- Keep main code private
- Create public `Scanify-Releases` repo
- Only publish installers there
- Update `GITHUB_REPO` to point to releases repo
