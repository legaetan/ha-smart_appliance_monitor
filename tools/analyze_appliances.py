#!/usr/bin/env python3
"""Analyse des appliances Smart Appliance Monitor et recommandation de seuils optimaux."""

import requests
import json
from datetime import datetime, timezone, timedelta
import statistics
import subprocess

# Configuration
HA_URL = 'https://home.lega.wtf'
HA_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4N2FlY2Y3ZDNkMjk0Y2E3OWE2Mzg2Y2E5ODVjMDIwOSIsImlhdCI6MTc2MDQ3MDA3NCwiZXhwIjoyMDc1ODMwMDc0fQ.U2pF-m2aM2ZIeiC7e1BjQOrygfuvpzIBcEmLPBhGocA'

headers = {
    'Authorization': f'Bearer {HA_TOKEN}',
    'Content-Type': 'application/json',
}

def get_appliances_from_ssh():
    """Récupère les appliances depuis le fichier de configuration via SSH."""
    cmd = [
        'ssh', '-i', '/home/legaetan/.ssh/id_rsa', 'root@192.168.1.11',
        'cat /config/.storage/core.config_entries | jq \'.data.entries[] | select(.domain == "smart_appliance_monitor")\' | jq -s .'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []

def get_history(entity_id, start_date):
    """Récupère l'historique d'une entité depuis une date jusqu'à maintenant."""
    start_timestamp = start_date.isoformat()
    end_timestamp = datetime.now(timezone.utc).isoformat()
    
    url = f'{HA_URL}/api/history/period/{start_timestamp}'
    params = {
        'filter_entity_id': entity_id,
        'end_time': end_timestamp
    }
    
    print(f"  Fetching history for {entity_id}...")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            return data[0]
    return []

def analyze_power_data(power_values):
    """Analyse les données de puissance pour déterminer les seuils optimaux."""
    if not power_values or len(power_values) < 10:
        return None
    
    # Filtrer les valeurs invalides
    valid_values = [v for v in power_values if v is not None and v >= 0]
    if len(valid_values) < 10:
        return None
    
    # Statistiques de base
    min_power = min(valid_values)
    max_power = max(valid_values)
    mean_power = statistics.mean(valid_values)
    median_power = statistics.median(valid_values)
    
    # Calculer les percentiles
    sorted_values = sorted(valid_values)
    n = len(sorted_values)
    p10 = sorted_values[int(n * 0.10)]
    p25 = sorted_values[int(n * 0.25)]
    p75 = sorted_values[int(n * 0.75)]
    p90 = sorted_values[int(n * 0.90)]
    
    # Détecter les clusters
    low_values = [v for v in valid_values if v <= p25]
    high_values = [v for v in valid_values if v >= p75]
    
    # Stop threshold: basé sur les valeurs basses + marge
    if low_values:
        stop_threshold = min(max(low_values) * 1.5, p25 * 1.2)
    else:
        stop_threshold = p10 * 1.5
    
    # Start threshold: basé sur le gap entre valeurs basses et hautes
    if high_values and low_values:
        gap = min(high_values) - max(low_values)
        if gap > 10:
            start_threshold = max(low_values) + gap * 0.3
        else:
            start_threshold = p25 * 1.5
    else:
        start_threshold = p25 * 1.5
    
    # Arrondir
    stop_threshold = round(stop_threshold / 5) * 5
    start_threshold = round(start_threshold / 10) * 10
    
    # S'assurer que start > stop
    if start_threshold <= stop_threshold:
        start_threshold = stop_threshold * 2
    
    return {
        'min': round(min_power, 2),
        'max': round(max_power, 2),
        'mean': round(mean_power, 2),
        'median': round(median_power, 2),
        'p10': round(p10, 2),
        'p25': round(p25, 2),
        'p75': round(p75, 2),
        'p90': round(p90, 2),
        'recommended_stop_threshold': int(stop_threshold),
        'recommended_start_threshold': int(start_threshold),
        'sample_count': len(valid_values),
    }

def main():
    """Fonction principale."""
    print("=" * 80)
    print("ANALYSE DES APPLIANCES SMART APPLIANCE MONITOR")
    print("=" * 80)
    print()
    
    # Depuis le 20 octobre 2025 (date où la plupart des capteurs ont des données)
    start_date = datetime(2025, 10, 20, 0, 0, 0, tzinfo=timezone.utc)
    print(f"Période d'analyse: Depuis le 20 octobre 2025 jusqu'à maintenant")
    print()
    
    # Récupérer les appliances via SSH
    print("Récupération des appliances configurées (via SSH)...")
    appliances = get_appliances_from_ssh()
    print(f"✓ {len(appliances)} appliances trouvées\n")
    
    results = []
    
    # Analyser chaque appliance
    for appliance in appliances:
        print("-" * 80)
        print(f"Analyse: {appliance['title']}")
        print("-" * 80)
        
        data = appliance.get('data', {})
        options = appliance.get('options', {})
        
        appliance_name = data.get('appliance_name')
        appliance_type = data.get('appliance_type')
        power_sensor = data.get('power_sensor')
        energy_sensor = data.get('energy_sensor')
        
        current_start_threshold = options.get('start_threshold', 'N/A')
        current_stop_threshold = options.get('stop_threshold', 'N/A')
        
        print(f"Type: {appliance_type}")
        print(f"Capteur de puissance: {power_sensor}")
        print(f"Seuils actuels: Start={current_start_threshold}W, Stop={current_stop_threshold}W")
        print()
        
        # Skip "other" type appliances - garder valeurs par défaut
        if appliance_type == 'other':
            print("ℹ️  Type 'other' - Seuils par défaut conservés")
            results.append({
                'name': appliance['title'],
                'type': appliance_type,
                'power_sensor': power_sensor,
                'current_start': current_start_threshold,
                'current_stop': current_stop_threshold,
                'analysis': None,
                'status': 'other_skipped'
            })
            print()
            continue
        
        # Récupérer l'historique
        history = get_history(power_sensor, start_date)
        
        if not history:
            print("⚠️  Pas de données historiques disponibles")
            results.append({
                'name': appliance['title'],
                'type': appliance_type,
                'power_sensor': power_sensor,
                'current_start': current_start_threshold,
                'current_stop': current_stop_threshold,
                'analysis': None,
                'status': 'no_data'
            })
            print()
            continue
        
        # Extraire les valeurs de puissance
        power_values = []
        for state in history:
            try:
                # API standard format
                value = float(state['state'])
                power_values.append(value)
            except (ValueError, KeyError, TypeError):
                continue
        
        print(f"✓ {len(power_values)} relevés de puissance analysés")
        
        # Analyser les données
        analysis = analyze_power_data(power_values)
        
        if analysis:
            print()
            print("Statistiques de puissance:")
            print(f"  Min: {analysis['min']}W")
            print(f"  P10: {analysis['p10']}W")
            print(f"  P25: {analysis['p25']}W")
            print(f"  Médiane: {analysis['median']}W")
            print(f"  Moyenne: {analysis['mean']}W")
            print(f"  P75: {analysis['p75']}W")
            print(f"  P90: {analysis['p90']}W")
            print(f"  Max: {analysis['max']}W")
            print()
            print("Seuils recommandés:")
            print(f"  Start Threshold: {analysis['recommended_start_threshold']}W")
            print(f"  Stop Threshold: {analysis['recommended_stop_threshold']}W")
            
            # Comparer avec les seuils actuels
            if current_start_threshold != 'N/A' and current_stop_threshold != 'N/A':
                start_diff = abs(current_start_threshold - analysis['recommended_start_threshold'])
                stop_diff = abs(current_stop_threshold - analysis['recommended_stop_threshold'])
                
                start_diff_pct = (start_diff / current_start_threshold * 100) if current_start_threshold > 0 else 0
                stop_diff_pct = (stop_diff / current_stop_threshold * 100) if current_stop_threshold > 0 else 0
                
                print()
                if start_diff_pct > 20 or stop_diff_pct > 20:
                    print("⚠️  AJUSTEMENT RECOMMANDÉ")
                    if start_diff_pct > 20:
                        print(f"   - Start threshold: écart de {start_diff_pct:.1f}%")
                    if stop_diff_pct > 20:
                        print(f"   - Stop threshold: écart de {stop_diff_pct:.1f}%")
                else:
                    print("✅ SEUILS OPTIMAUX")
                
                status = 'needs_adjustment' if (start_diff_pct > 20 or stop_diff_pct > 20) else 'optimal'
            else:
                status = 'not_configured'
            
            results.append({
                'name': appliance['title'],
                'type': appliance_type,
                'power_sensor': power_sensor,
                'current_start': current_start_threshold,
                'current_stop': current_stop_threshold,
                'analysis': analysis,
                'status': status
            })
        else:
            print("⚠️  Pas assez de données pour l'analyse")
            results.append({
                'name': appliance['title'],
                'type': appliance_type,
                'power_sensor': power_sensor,
                'current_start': current_start_threshold,
                'current_stop': current_stop_threshold,
                'analysis': None,
                'status': 'insufficient_data'
            })
        
        print()
    
    # Résumé final
    print("=" * 80)
    print("RÉSUMÉ DE L'ANALYSE")
    print("=" * 80)
    print()
    
    optimal_count = sum(1 for r in results if r['status'] == 'optimal')
    needs_adjustment = [r for r in results if r['status'] == 'needs_adjustment']
    not_configured = [r for r in results if r['status'] == 'not_configured']
    other_skipped = [r for r in results if r['status'] == 'other_skipped']
    
    print(f"✅ Appliances optimales: {optimal_count}")
    print(f"⚠️  Appliances nécessitant un ajustement: {len(needs_adjustment)}")
    print(f"ℹ️  Appliances non configurées: {len(not_configured)}")
    print(f"⏭️  Appliances 'other' ignorées: {len(other_skipped)}")
    print()
    
    if needs_adjustment:
        print("AJUSTEMENTS RECOMMANDÉS:")
        print()
        for r in needs_adjustment:
            print(f"📌 {r['name']} ({r['type']})")
            print(f"   Actuels: Start={r['current_start']}W, Stop={r['current_stop']}W")
            if r['analysis']:
                print(f"   Recommandés: Start={r['analysis']['recommended_start_threshold']}W, Stop={r['analysis']['recommended_stop_threshold']}W")
            print()
    
    if not_configured:
        print("CONFIGURATION RECOMMANDÉE:")
        print()
        for r in not_configured:
            print(f"📌 {r['name']} ({r['type']})")
            if r['analysis']:
                print(f"   Recommandés: Start={r['analysis']['recommended_start_threshold']}W, Stop={r['analysis']['recommended_stop_threshold']}W")
            print()
    
    # Recommandation pour le profil "air_conditioner"
    clim_result = next((r for r in results if r['name'] == 'Clim'), None)
    if clim_result and clim_result['analysis']:
        print("=" * 80)
        print("PROFIL AIR_CONDITIONER RECOMMANDÉ")
        print("=" * 80)
        print()
        print("Basé sur l'analyse de votre climatisation, voici le profil recommandé:")
        print()
        print(f"    \"air_conditioner\": {{")
        print(f"        \"start_threshold\": {clim_result['analysis']['recommended_start_threshold']},")
        print(f"        \"stop_threshold\": {clim_result['analysis']['recommended_stop_threshold']},")
        print(f"        \"start_delay\": 120,  # 2 minutes")
        print(f"        \"stop_delay\": 300,  # 5 minutes (cycles du compresseur)")
        print(f"        \"alert_duration\": 43200,  # 12 heures")
        print(f"    }},")
        print()
    
    # Sauvegarder les résultats
    with open('/home/legaetan/syncthing_lega.wtf_stacks/HA/ha-smart_appliance_monitor/analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("✓ Résultats sauvegardés dans analysis_results.json")

if __name__ == '__main__':
    main()

