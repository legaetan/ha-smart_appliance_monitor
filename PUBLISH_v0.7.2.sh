#!/bin/bash
# Script de publication de la release v0.7.2
# Smart Appliance Monitor

set -e

echo "🚀 Publication de Smart Appliance Monitor v0.7.2"
echo "=================================================="
echo ""

# Vérification de la version
VERSION=$(cat version)
if [ "$VERSION" != "0.7.2" ]; then
    echo "❌ Erreur: version dans le fichier 'version' est $VERSION au lieu de 0.7.2"
    exit 1
fi

MANIFEST_VERSION=$(grep '"version"' custom_components/smart_appliance_monitor/manifest.json | cut -d'"' -f4)
if [ "$MANIFEST_VERSION" != "0.7.2" ]; then
    echo "❌ Erreur: version dans manifest.json est $MANIFEST_VERSION au lieu de 0.7.2"
    exit 1
fi

echo "✅ Versions vérifiées: $VERSION"
echo ""

# Vérification de l'archive
if [ ! -f "smart_appliance_monitor-v0.7.2.zip" ]; then
    echo "❌ Erreur: Archive smart_appliance_monitor-v0.7.2.zip introuvable"
    exit 1
fi

ARCHIVE_SIZE=$(du -h smart_appliance_monitor-v0.7.2.zip | cut -f1)
echo "✅ Archive trouvée: smart_appliance_monitor-v0.7.2.zip ($ARCHIVE_SIZE)"
echo ""

# Affichage des fichiers modifiés
echo "📝 Fichiers modifiés:"
git status --short || echo "  (git non disponible)"
echo ""

# Commit des changements
echo "📦 Étape 1: Commit des changements"
read -p "   Voulez-vous commiter les changements? (o/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Oo]$ ]]; then
    git add -A
    git commit -m "Release v0.7.2 - Fix AI services registration + Complete documentation

- Fixed critical bug preventing AI services from being registered on update
- Added comprehensive AI-Analysis wiki page (527 lines)
- Updated wiki sidebar with Energy & AI section
- Updated Features.md with v0.6.0 and v0.7.0 sections
- All 13 services now properly available after update
- Complete release notes and documentation

Closes issue with 'configure_ai' service not found error."
    echo "   ✅ Commit créé"
else
    echo "   ⏭️  Commit ignoré"
fi
echo ""

# Création du tag
echo "🏷️  Étape 2: Création du tag v0.7.2"
read -p "   Voulez-vous créer le tag? (o/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Oo]$ ]]; then
    git tag -a v0.7.2 -m "Version 0.7.2 - Critical AI services fix

This release fixes a critical bug where AI services were not registered
when upgrading from v0.6.0 to v0.7.0/v0.7.1.

Key fixes:
- AI services (configure_ai, analyze_cycles, analyze_energy_dashboard) now properly registered
- Complete AI-powered analysis documentation added to wiki
- All 13 services available after Home Assistant restart

Breaking changes: None
Migration: Restart Home Assistant after update"
    echo "   ✅ Tag v0.7.2 créé"
else
    echo "   ⏭️  Tag ignoré"
fi
echo ""

# Push vers GitHub
echo "⬆️  Étape 3: Push vers GitHub"
read -p "   Voulez-vous pusher vers GitHub? (o/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "   Pushing main branch..."
    git push origin main
    echo "   Pushing tag v0.7.2..."
    git push origin v0.7.2
    echo "   ✅ Push terminé"
else
    echo "   ⏭️  Push ignoré"
fi
echo ""

# Instructions pour GitHub Release
echo "📋 Étape 4: Créer la release sur GitHub"
echo ""
echo "   1. Aller sur: https://github.com/legaetan/ha-smart_appliance_monitor/releases/new"
echo "   2. Sélectionner le tag: v0.7.2"
echo "   3. Titre de la release: v0.7.2 - AI Services Fix + Complete Documentation"
echo "   4. Description: Copier depuis docs/release_notes/RELEASE_NOTES_v0.7.2.md"
echo "   5. Attacher le fichier: smart_appliance_monitor-v0.7.2.zip"
echo "   6. Cocher 'Set as the latest release'"
echo "   7. Cliquer sur 'Publish release'"
echo ""

# Résumé final
echo "✨ Release v0.7.2 prête!"
echo "========================"
echo ""
echo "📦 Archive: smart_appliance_monitor-v0.7.2.zip ($ARCHIVE_SIZE)"
echo "📝 Release notes: docs/release_notes/RELEASE_NOTES_v0.7.2.md"
echo "📚 Documentation: docs/wiki-github/AI-Analysis.md (527 lignes)"
echo "🔧 Bug fix: Services AI maintenant enregistrés correctement"
echo ""
echo "🎯 Actions suivantes:"
echo "   - Créer la release GitHub avec l'archive"
echo "   - Attendre validation HACS"
echo "   - Annoncer la release dans Home Assistant Community"
echo ""
echo "Merci! 🤖⚡"

