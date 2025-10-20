# Documentation Structure

This directory contains all project documentation.

## Directory Structure

```
docs/
├── wiki-github/       # Git submodule: GitHub Wiki (source of truth)
│   ├── Home.md
│   ├── Installation.md
│   ├── Configuration.md
│   ├── Reconfiguration.md
│   ├── Features.md
│   └── _Sidebar.md
└── archive/           # Historical design documents
    ├── CONCEPT_INTEGRATION_HACS.md
    ├── SPECS_TECHNIQUES_INTEGRATION.md
    ├── RESSOURCES_DEVELOPPEMENT.md
    └── INDEX_COMPLET.md
```

## Wiki Documentation

The `wiki-github/` directory is a **git submodule** that contains the GitHub Wiki:
- https://github.com/legaetan/ha-smart_appliance_monitor.wiki.git

This is the **single source of truth** for user documentation. Edit files directly in this directory.

### Available Pages

- **Home.md** - Wiki home page with overview and quick links
- **Installation.md** - Complete installation guide
- **Configuration.md** - Setup and configuration reference
- **Reconfiguration.md** - How to modify settings without data loss
- **Features.md** - Complete entity and service reference
- **_Sidebar.md** - Wiki navigation sidebar

## Editing Documentation

### Workflow

1. **Navigate to wiki submodule**
   ```bash
   cd docs/wiki-github
   ```

2. **Edit documentation files**
   ```bash
   # Edit any markdown file
   nano Installation.md
   ```

3. **Commit changes in the submodule**
   ```bash
   git add .
   git commit -m "docs: update installation guide"
   ```

4. **Push to GitHub Wiki**
   ```bash
   GH_TOKEN=$(gh auth token) && git -c credential.helper="!f() { echo \"username=legaetan\"; echo \"password=$GH_TOKEN\"; }; f" push origin master
   ```

5. **Update submodule reference in main repo**
   ```bash
   cd ../..  # Back to repo root
   git add docs/wiki-github
   git commit -m "docs: update wiki submodule reference"
   git push
   ```

### Quick Push Command

From `docs/wiki-github/`:
```bash
git add . && git commit -m "docs: update" && GH_TOKEN=$(gh auth token) && git -c credential.helper="!f() { echo \"username=legaetan\"; echo \"password=$GH_TOKEN\"; }; f" push origin master
```

## Working with Submodules

### First Time Clone

When cloning the repository, initialize submodules:

```bash
git clone https://github.com/legaetan/ha-smart_appliance_monitor.git
cd ha-smart_appliance_monitor
git submodule update --init --recursive
```

### One-Line Clone

Clone repository with submodules in one command:

```bash
git clone --recurse-submodules https://github.com/legaetan/ha-smart_appliance_monitor.git
```

### Pull Updates from Wiki

To get latest wiki changes:

```bash
cd docs/wiki-github
git pull origin master
cd ../..
git add docs/wiki-github
git commit -m "docs: update wiki submodule"
git push
```

## Archive

The `archive/` directory contains historical French design documents from the initial project phase. These are preserved for reference but are no longer actively maintained.

## GitHub Wiki Access

The documentation is also available online at:
**https://github.com/legaetan/ha-smart_appliance_monitor/wiki**

Changes pushed to the submodule appear immediately on the GitHub Wiki interface.

## Important Notes

- **Naming Convention**: GitHub Wiki requires CamelCase file names (Installation.md, not installation.md)
- **Submodule Workflow**: Changes must be committed in the submodule first, then the reference updated in the main repo
- **Single Source**: All documentation lives in `wiki-github/` - no duplication
- **Auto-sync**: Changes pushed to the submodule appear instantly on GitHub Wiki
