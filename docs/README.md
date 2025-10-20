# Documentation Structure

This directory contains all project documentation.

## Directory Structure

```
docs/
├── wiki/              # Source documentation (markdown files)
│   ├── installation.md
│   ├── configuration.md
│   ├── reconfiguration.md
│   └── features.md
├── wiki-github/       # Git submodule: GitHub Wiki repository
│   └── (auto-synced from wiki/)
└── archive/           # Historical design documents
    ├── CONCEPT_INTEGRATION_HACS.md
    ├── SPECS_TECHNIQUES_INTEGRATION.md
    ├── RESSOURCES_DEVELOPPEMENT.md
    └── INDEX_COMPLET.md
```

## Wiki Documentation

### Source Files (`wiki/`)

The `wiki/` directory contains the source markdown files for the user documentation:

- **installation.md** - Complete installation guide (manual, HACS, troubleshooting)
- **configuration.md** - Initial setup, appliance profiles, advanced settings
- **reconfiguration.md** - How to modify settings without losing data
- **features.md** - Complete reference for all entities and services

These are the **source of truth** for documentation. Edit these files when updating documentation.

### GitHub Wiki (`wiki-github/`)

The `wiki-github/` directory is a **git submodule** that references the GitHub Wiki repository:
- https://github.com/legaetan/ha-smart_appliance_monitor.wiki.git

This directory is **automatically synced** from `wiki/` using the sync script.

**Do not edit files in `wiki-github/` directly** - changes will be overwritten during sync.

## Synchronizing to GitHub Wiki

To sync documentation from `wiki/` to the GitHub Wiki:

```bash
./sync-wiki.sh
```

This script will:
1. Update the wiki submodule
2. Copy files from `wiki/` with proper naming (CamelCase)
3. Generate Home and Sidebar pages
4. Commit and push to GitHub Wiki

The GitHub Wiki is accessible at:
https://github.com/legaetan/ha-smart_appliance_monitor/wiki

## Archive

The `archive/` directory contains historical French design documents from the initial project phase. These are preserved for reference but are no longer actively maintained.

## Working with Submodules

### First Time Clone

When cloning the repository, initialize submodules:

```bash
git clone https://github.com/legaetan/ha-smart_appliance_monitor.git
cd ha-smart_appliance_monitor
git submodule update --init --recursive
```

### Updating Submodule

To pull latest changes from the wiki submodule:

```bash
cd docs/wiki-github
git pull origin master
cd ../..
git add docs/wiki-github
git commit -m "Update wiki submodule reference"
```

### One-Line Clone

Clone repository with submodules in one command:

```bash
git clone --recurse-submodules https://github.com/legaetan/ha-smart_appliance_monitor.git
```

## Documentation Workflow

1. **Edit** documentation in `docs/wiki/*.md`
2. **Test** locally (view markdown)
3. **Commit** changes to main repository
4. **Sync** to GitHub Wiki: `./sync-wiki.sh`
5. **Verify** on https://github.com/legaetan/ha-smart_appliance_monitor/wiki

## Notes

- The wiki submodule is a separate Git repository
- Changes to `docs/wiki/` must be synced manually using the script
- The GitHub Wiki has its own commit history (in the submodule)
- Main repository tracks the submodule reference (commit hash)

