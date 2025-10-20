"""Tests pour la fonctionnalité d'export de données."""
from __future__ import annotations

import csv
import json
import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from custom_components.smart_appliance_monitor.export import (
    SmartApplianceDataExporter,
)
from custom_components.smart_appliance_monitor.coordinator import (
    SmartApplianceCoordinator,
)


@pytest.mark.asyncio
async def test_exporter_initialization(mock_hass, mock_config_entry):
    """Test l'initialisation de l'exportateur."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    exporter = SmartApplianceDataExporter(coordinator)
    
    assert exporter.coordinator == coordinator
    assert exporter.hass == mock_hass
    assert exporter.appliance_name == "Four"
    assert exporter.entry_id == "test_entry_id"


@pytest.mark.asyncio
async def test_get_base_data(mock_hass, mock_config_entry):
    """Test la récupération des données de base."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
    }
    
    exporter = SmartApplianceDataExporter(coordinator)
    base_data = exporter._get_base_data()
    
    assert base_data["appliance_name"] == "Four"
    assert base_data["appliance_type"] == "oven"
    assert base_data["power_sensor"] == "sensor.prise_four_power"
    assert base_data["energy_sensor"] == "sensor.prise_four_energy"
    assert base_data["current_state"] == "idle"
    assert base_data["current_power"] == 0.0
    assert base_data["monitoring_enabled"] is True
    assert "last_update" in base_data


@pytest.mark.asyncio
async def test_get_cycle_data_none(mock_hass, mock_config_entry):
    """Test le formatage de données de cycle quand il n'y en a pas."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    exporter = SmartApplianceDataExporter(coordinator)
    
    cycle_data = exporter._get_cycle_data(None)
    
    assert cycle_data["start_time"] is None
    assert cycle_data["end_time"] is None
    assert cycle_data["duration_minutes"] == 0
    assert cycle_data["energy_kwh"] == 0
    assert cycle_data["cost_eur"] == 0
    assert cycle_data["peak_power_w"] == 0


@pytest.mark.asyncio
async def test_get_cycle_data_with_data(mock_hass, mock_config_entry):
    """Test le formatage de données de cycle avec des vraies données."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    exporter = SmartApplianceDataExporter(coordinator)
    
    start_time = datetime(2025, 10, 20, 18, 0, 0)
    end_time = datetime(2025, 10, 20, 19, 15, 0)
    
    cycle = {
        "start_time": start_time,
        "end_time": end_time,
        "duration": 75.0,
        "energy": 1.234,
        "cost": 0.31,
        "peak_power": 1850,
    }
    
    cycle_data = exporter._get_cycle_data(cycle)
    
    assert cycle_data["start_time"] == start_time.isoformat()
    assert cycle_data["end_time"] == end_time.isoformat()
    assert cycle_data["duration_minutes"] == 75.0
    assert cycle_data["energy_kwh"] == 1.234
    assert cycle_data["cost_eur"] == 0.31
    assert cycle_data["peak_power_w"] == 1850


@pytest.mark.asyncio
async def test_export_summary(mock_hass, mock_config_entry):
    """Test la génération du résumé d'export."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "current_cycle": {"duration": 30.0},
        "last_cycle": {"duration": 60.0},
    }
    coordinator.daily_stats = {"cycles": 2, "total_energy": 2.5, "total_cost": 0.63}
    coordinator.monthly_stats = {"total_energy": 45.0, "total_cost": 11.3}
    coordinator._cycle_history = [{"duration": 60.0}] * 5
    
    exporter = SmartApplianceDataExporter(coordinator)
    summary = exporter.get_export_summary()
    
    assert summary["has_current_cycle"] is True
    assert summary["has_last_cycle"] is True
    assert summary["daily_cycles"] == 2
    assert summary["daily_energy"] == 2.5
    assert summary["daily_cost"] == 0.63
    assert summary["monthly_energy"] == 45.0
    assert summary["monthly_cost"] == 11.3
    assert summary["history_size"] == 5


@pytest.mark.asyncio
async def test_export_to_csv_content(mock_hass, mock_config_entry):
    """Test l'export CSV sans fichier (contenu seul)."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 5.0,
        "current_cycle": None,
        "last_cycle": {
            "start_time": datetime(2025, 10, 20, 18, 0, 0),
            "end_time": datetime(2025, 10, 20, 19, 15, 0),
            "duration": 75.0,
            "energy": 1.234,
            "cost": 0.31,
            "peak_power": 1850,
        },
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 2,
        "total_energy": 2.5,
        "total_cost": 0.63,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 45.0,
        "total_cost": 11.3,
    }
    
    exporter = SmartApplianceDataExporter(coordinator)
    csv_content = exporter.export_to_csv()
    
    # Vérifier que le CSV contient des données
    assert len(csv_content) > 0
    assert "appliance_name" in csv_content
    assert "Four" in csv_content
    assert "1.234" in csv_content  # Energy du dernier cycle


@pytest.mark.asyncio
async def test_export_to_csv_file(mock_hass, mock_config_entry):
    """Test l'export CSV vers un fichier."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    
    exporter = SmartApplianceDataExporter(coordinator)
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name
    
    try:
        # Export vers fichier
        csv_content = exporter.export_to_csv(tmp_path)
        
        # Vérifier que le fichier existe
        assert os.path.exists(tmp_path)
        
        # Vérifier que le contenu est correct
        with open(tmp_path, 'r') as f:
            file_content = f.read()
            assert "appliance_name" in file_content
            assert "Four" in file_content
    finally:
        # Nettoyer
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@pytest.mark.asyncio
async def test_export_to_json_content(mock_hass, mock_config_entry):
    """Test l'export JSON sans fichier (contenu seul)."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "running",
        "power": 850.0,
        "energy": 1.5,
        "current_cycle": {
            "start_time": datetime(2025, 10, 20, 18, 0, 0),
            "duration": 30.0,
            "energy": 0.425,
        },
        "last_cycle": {
            "start_time": datetime(2025, 10, 20, 12, 0, 0),
            "end_time": datetime(2025, 10, 20, 13, 15, 0),
            "duration": 75.0,
            "energy": 1.234,
            "cost": 0.31,
            "peak_power": 1850,
        },
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 2,
        "total_energy": 2.5,
        "total_cost": 0.63,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 45.0,
        "total_cost": 11.3,
    }
    coordinator._cycle_history = [
        {
            "start_time": datetime(2025, 10, 19, 10, 0, 0),
            "end_time": datetime(2025, 10, 19, 11, 0, 0),
            "duration": 60.0,
            "energy": 1.2,
            "cost": 0.3,
            "peak_power": 1800,
        }
    ]
    
    exporter = SmartApplianceDataExporter(coordinator)
    json_content = exporter.export_to_json()
    
    # Parser le JSON
    data = json.loads(json_content)
    
    # Vérifier la structure
    assert data["appliance_name"] == "Four"
    assert data["appliance_type"] == "oven"
    assert data["current_state"] == "running"
    assert data["current_power"] == 850.0
    assert data["current_cycle"]["duration_minutes"] == 30.0
    assert data["last_cycle"]["duration_minutes"] == 75.0
    assert data["daily_stats"]["cycles"] == 2
    assert data["monthly_stats"]["total_energy_kwh"] == 45.0
    assert len(data["cycle_history"]) == 1


@pytest.mark.asyncio
async def test_export_to_json_file(mock_hass, mock_config_entry):
    """Test l'export JSON vers un fichier."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator._cycle_history = []
    
    exporter = SmartApplianceDataExporter(coordinator)
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        tmp_path = tmp.name
    
    try:
        # Export vers fichier
        json_content = exporter.export_to_json(tmp_path)
        
        # Vérifier que le fichier existe
        assert os.path.exists(tmp_path)
        
        # Vérifier que le contenu est du JSON valide
        with open(tmp_path, 'r') as f:
            data = json.load(f)
            assert data["appliance_name"] == "Four"
            assert data["appliance_type"] == "oven"
    finally:
        # Nettoyer
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@pytest.mark.asyncio
async def test_export_json_with_empty_history(mock_hass, mock_config_entry):
    """Test l'export JSON sans historique de cycles."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator._cycle_history = []
    
    exporter = SmartApplianceDataExporter(coordinator)
    json_content = exporter.export_to_json()
    
    data = json.loads(json_content)
    
    assert data["cycle_history"] == []
    assert data["current_cycle"]["start_time"] is None
    assert data["last_cycle"]["start_time"] is None


@pytest.mark.asyncio
async def test_export_with_all_features_enabled(mock_hass, mock_config_entry):
    """Test l'export avec toutes les fonctionnalités activées."""
    mock_config_entry.options = {
        "enable_auto_shutdown": True,
        "enable_energy_limits": True,
        "enable_scheduling": True,
        "enable_anomaly_detection": True,
    }
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator._cycle_history = []
    
    exporter = SmartApplianceDataExporter(coordinator)
    json_content = exporter.export_to_json()
    
    data = json.loads(json_content)
    
    assert data["auto_shutdown_enabled"] is True
    assert data["energy_limits_enabled"] is True
    assert data["scheduling_enabled"] is True
    assert data["anomaly_detection_enabled"] is True


@pytest.mark.asyncio
async def test_export_csv_with_special_characters(mock_hass, mock_config_entry):
    """Test l'export CSV avec des caractères spéciaux."""
    mock_config_entry.data["appliance_name"] = "Lave-vaisselle (Cuisine)"
    
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    
    exporter = SmartApplianceDataExporter(coordinator)
    csv_content = exporter.export_to_csv()
    
    # Le nom avec caractères spéciaux doit être présent
    assert "Lave-vaisselle (Cuisine)" in csv_content or "Lave-vaisselle" in csv_content


@pytest.mark.asyncio
async def test_export_error_handling_invalid_path(mock_hass, mock_config_entry):
    """Test la gestion d'erreur avec un chemin invalide."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    
    exporter = SmartApplianceDataExporter(coordinator)
    
    # Chemin invalide (répertoire qui n'existe pas)
    invalid_path = "/nonexistent/directory/export.csv"
    
    # Doit lever une exception
    with pytest.raises(Exception):
        exporter.export_to_csv(invalid_path)


@pytest.mark.asyncio
async def test_export_json_valid_format(mock_hass, mock_config_entry):
    """Test que le JSON exporté est valide et bien formaté."""
    coordinator = SmartApplianceCoordinator(mock_hass, mock_config_entry)
    coordinator.data = {
        "state": "idle",
        "power": 0.0,
        "energy": 0.0,
        "current_cycle": None,
        "last_cycle": None,
    }
    coordinator.daily_stats = {
        "date": datetime(2025, 10, 20).date(),
        "cycles": 0,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator.monthly_stats = {
        "year": 2025,
        "month": 10,
        "total_energy": 0,
        "total_cost": 0,
    }
    coordinator._cycle_history = []
    
    exporter = SmartApplianceDataExporter(coordinator)
    json_content = exporter.export_to_json()
    
    # Doit pouvoir être parsé
    data = json.loads(json_content)
    
    # Vérifier que c'est bien formaté (avec indentation)
    assert "\n" in json_content  # Contient des sauts de ligne
    assert "  " in json_content  # Contient des indentations

