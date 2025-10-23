#!/usr/bin/env python3
"""
Script pour appliquer automatiquement les seuils optimisés aux appliances existantes.
"""

import requests
import json
import subprocess

# Configuration
HA_URL = 'https://home.lega.wtf'
HA_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4N2FlY2Y3ZDNkMjk0Y2E3OWE2Mzg2Y2E5ODVjMDIwOSIsImlhdCI6MTc2MDQ3MDA3NCwiZXhwIjoyMDc1ODMwMDc0fQ.U2pF-m2aM2ZIeiC7e1BjQOrygfuvpzIBcEmLPBhGocA'

headers = {
    'Authorization': f'Bearer {HA_TOKEN}',
    'Content-Type': 'application/json',
}

# Nouveaux seuils optimisés (basés sur l'analyse)
OPTIMIZED_THRESHOLDS = {
    'washing_machine': {
        'start_threshold': 100,
        'stop_threshold': 20,
        'start_delay': 60,
        'stop_delay': 120,
    },
    'dishwasher': {
        'start_threshold': 150,
        'stop_threshold': 50,
        'start_delay': 60,
        'stop_delay': 120,
    },
    'dryer': {
        'start_threshold': 200,
        'stop_threshold': 50,
        'start_delay': 30,
        'stop_delay': 120,
    },
    'printer_3d': {
        'start_threshold': 30,
        'stop_threshold': 10,
        'start_delay': 60,
        'stop_delay': 120,
    },
    'monitor': {
        'start_threshold': 40,
        'stop_threshold': 5,
        'start_delay': 30,
        'stop_delay': 60,
    },
    'water_heater': {
        'start_threshold': 1000,
        'stop_threshold': 50,
        'start_delay': 30,
        'stop_delay': 60,
    },
    'vmc': {
        'start_threshold': 20,
        'stop_threshold': 10,
        'start_delay': 30,
        'stop_delay': 60,
    },
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

def update_appliance_options(entry_id, new_options):
    """Met à jour les options d'une appliance via SSH (modification du fichier)."""
    # L'API Home Assistant ne permet pas facilement de mettre à jour les options
    # Il faut passer par un options flow ou modifier directement le fichier storage
    
    # Commande pour mettre à jour via SSH
    update_script = f"""
python3 << 'PYTHON_EOF'
import json

# Lire le fichier
with open('/config/.storage/core.config_entries', 'r') as f:
    data = json.load(f)

# Trouver et mettre à jour l'entrée
for entry in data['data']['entries']:
    if entry['entry_id'] == '{entry_id}':
        if 'options' not in entry:
            entry['options'] = {{}}
        entry['options'].update({json.dumps(new_options)})
        entry['modified_at'] = data['data']['entries'][0]['modified_at']  # Timestamp
        break

# Sauvegarder
with open('/config/.storage/core.config_entries', 'w') as f:
    json.dump(data, f, indent=2)

print('✓ Options mises à jour')
PYTHON_EOF
"""
    
    cmd = ['ssh', '-i', '/home/legaetan/.ssh/id_rsa', 'root@192.168.1.11', update_script]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return result.returncode == 0

def main():
    print("=" * 80)
    print("APPLICATION DES SEUILS OPTIMISÉS")
    print("=" * 80)
    print()
    
    # Récupérer les appliances
    print("Récupération des appliances configurées...")
    appliances = get_appliances_from_ssh()
    print(f"✓ {len(appliances)} appliances trouvées\n")
    
    updated_count = 0
    skipped_count = 0
    
    for appliance in appliances:
        name = appliance['title']
        entry_id = appliance['entry_id']
        appliance_type = appliance.get('data', {}).get('appliance_type')
        current_options = appliance.get('options', {})
        
        print("-" * 80)
        print(f"Appliance: {name} ({appliance_type})")
        
        # Vérifier si on a des seuils optimisés pour ce type
        if appliance_type in OPTIMIZED_THRESHOLDS:
            new_thresholds = OPTIMIZED_THRESHOLDS[appliance_type]
            
            # Afficher les changements
            print(f"  Actuels:")
            print(f"    Start: {current_options.get('start_threshold', 'N/A')}W")
            print(f"    Stop:  {current_options.get('stop_threshold', 'N/A')}W")
            print(f"  Nouveaux:")
            print(f"    Start: {new_thresholds['start_threshold']}W")
            print(f"    Stop:  {new_thresholds['stop_threshold']}W")
            print(f"    Start Delay: {new_thresholds['start_delay']}s")
            print(f"    Stop Delay: {new_thresholds['stop_delay']}s")
            
            # Demander confirmation
            response = input(f"\n  Appliquer ces changements? [O/n]: ").strip().lower()
            
            if response in ['', 'o', 'oui', 'y', 'yes']:
                # Appliquer les changements
                if update_appliance_options(entry_id, new_thresholds):
                    print(f"  ✓ Seuils mis à jour!")
                    updated_count += 1
                else:
                    print(f"  ✗ Erreur lors de la mise à jour")
            else:
                print(f"  ⏭️  Ignoré")
                skipped_count += 1
        else:
            print(f"  ℹ️  Pas de seuils optimisés pour ce type")
            skipped_count += 1
        
        print()
    
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"✓ Appliances mises à jour: {updated_count}")
    print(f"⏭️  Appliances ignorées: {skipped_count}")
    print()
    
    if updated_count > 0:
        print("⚠️  IMPORTANT: Redémarrez Home Assistant pour appliquer les changements!")
        print()
        response = input("Voulez-vous redémarrer Home Assistant maintenant? [o/N]: ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("\nRedémarrage de Home Assistant...")
            restart_url = f'{HA_URL}/api/services/homeassistant/restart'
            response = requests.post(restart_url, headers=headers)
            if response.status_code == 200:
                print("✓ Redémarrage lancé!")
            else:
                print(f"✗ Erreur: {response.status_code}")

if __name__ == '__main__':
    main()

