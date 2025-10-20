#!/bin/bash
# sync-wiki.sh - Synchronize docs/wiki/ to GitHub Wiki

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIKI_DIR="$REPO_DIR/docs/wiki-github"

echo "🔄 Synchronizing documentation to GitHub Wiki..."

# Initialize submodule if needed
if [ ! -d "$WIKI_DIR/.git" ]; then
    echo "📥 Initializing wiki submodule..."
    cd "$REPO_DIR"
    git submodule update --init --recursive
fi

# Update wiki repository
cd "$WIKI_DIR"
echo "📦 Pulling latest changes..."
git pull origin master

# Copy documentation files with CamelCase naming
echo "📝 Copying documentation files..."
cp "$REPO_DIR/docs/wiki/installation.md" Installation.md
cp "$REPO_DIR/docs/wiki/configuration.md" Configuration.md
cp "$REPO_DIR/docs/wiki/reconfiguration.md" Reconfiguration.md
cp "$REPO_DIR/docs/wiki/features.md" Features.md

# Create Home page
echo "🏠 Creating Home page..."
cat > Home.md << 'EOF'
# Smart Appliance Monitor Documentation

Welcome to the Smart Appliance Monitor wiki! This documentation will help you install, configure, and use the integration.

## User Guides

* [[Installation]] - Complete installation guide (manual, HACS, troubleshooting)
* [[Configuration]] - Initial setup, appliance profiles, and advanced settings
* [[Reconfiguration]] - How to modify settings without losing historical data
* [[Features]] - Complete reference for all entities, services, and features

## Overview

Smart Appliance Monitor is a Home Assistant custom integration that automatically detects and tracks appliance cycles using power consumption data from smart plugs.

### Key Features

- **Automatic Cycle Detection** - Intelligent start/stop detection with configurable thresholds
- **15 Entities per Appliance** - Comprehensive monitoring (10 sensors, 2 binary sensors, 2 switches, 1 button)
- **Appliance Profiles** - Pre-configured thresholds optimized for different appliance types
- **Dynamic Pricing** - Support for variable electricity rates via Home Assistant entities
- **Smart Notifications** - Alerts when cycles start, finish, or exceed expected duration
- **Statistics Tracking** - Daily and monthly cost tracking, cycle history

### Supported Appliances

Works with any appliance connected via a smart plug with power monitoring:
- Washing machines
- Dishwashers
- Dryers
- Water heaters
- Ovens
- Coffee makers
- And more!

## Quick Start

1. **Install** the integration (see [[Installation]])
2. **Configure** your first appliance (see [[Configuration]])
3. **Monitor** cycle detection and adjust thresholds if needed
4. **Explore** all available features (see [[Features]])

## Developer Resources

For developer documentation, see the main repository:

* [Contributing Guide](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CONTRIBUTING.md) - How to contribute to the project
* [Architecture Documentation](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/ARCHITECTURE.md) - Technical architecture and component design
* [Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md) - Version history and changes

## Links

* [GitHub Repository](https://github.com/legaetan/ha-smart_appliance_monitor) - Source code and main documentation
* [Report an Issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues) - Bug reports and feature requests
* [Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions) - Questions and community support
* [Latest Release](https://github.com/legaetan/ha-smart_appliance_monitor/releases) - Download the latest version

## Version

Current version: **0.1.0**

Last updated: October 2025

## License

This project is licensed under the MIT License.
EOF

# Create Sidebar
echo "📋 Creating Sidebar..."
cat > _Sidebar.md << 'EOF'
**[Home](Home)**

---

**User Guides**
* [Installation](Installation)
* [Configuration](Configuration)
* [Reconfiguration](Reconfiguration)
* [Features](Features)

---

**Developer Docs**
* [Contributing](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CONTRIBUTING.md)
* [Architecture](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/ARCHITECTURE.md)
* [Changelog](https://github.com/legaetan/ha-smart_appliance_monitor/blob/main/CHANGELOG.md)

---

**Links**
* [GitHub Repo](https://github.com/legaetan/ha-smart_appliance_monitor)
* [Report Issue](https://github.com/legaetan/ha-smart_appliance_monitor/issues)
* [Discussions](https://github.com/legaetan/ha-smart_appliance_monitor/discussions)
EOF

# Check for changes
if git diff --quiet; then
    echo "✅ No changes to sync"
    exit 0
fi

# Commit and push changes
echo "💾 Committing changes..."
git add .
git commit -m "Sync documentation from main repository

Updated: $(date '+%Y-%m-%d %H:%M:%S')"

echo "⬆️  Pushing to GitHub..."
GH_TOKEN=$(gh auth token) && git -c credential.helper="!f() { echo \"username=legaetan\"; echo \"password=$GH_TOKEN\"; }; f" push origin master

echo "✅ Wiki synchronized successfully!"
echo "🌐 View at: https://github.com/legaetan/ha-smart_appliance_monitor/wiki"

# Return to main repo
cd "$REPO_DIR"
echo "💡 Don't forget to commit the submodule reference in the main repo if needed"

