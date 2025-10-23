/**
 * Smart Appliances Configuration Panel
 * Frontend interface for managing dashboard configuration
 */

class SamConfigPanel extends HTMLElement {
  constructor() {
    super();
    this.hass = null;
    this._config = null;
    this._coordinators = [];
  }

  set hass(hass) {
    this._hass = hass;
    if (!this.content) {
      this._initialize();
    }
    this._update();
  }

  get hass() {
    return this._hass;
  }

  _initialize() {
    this.innerHTML = `
      <style>
        .sam-config-panel {
          padding: 16px;
          max-width: 1200px;
          margin: 0 auto;
        }
        .sam-header {
          display: flex;
          align-items: center;
          margin-bottom: 24px;
        }
        .sam-header h1 {
          margin: 0;
          font-size: 2em;
        }
        .sam-section {
          background: var(--card-background-color);
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 16px;
        }
        .sam-section-title {
          font-size: 1.2em;
          font-weight: bold;
          margin-bottom: 12px;
        }
        .sam-appliance-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px;
          border-bottom: 1px solid var(--divider-color);
        }
        .sam-appliance-info {
          flex: 1;
        }
        .sam-appliance-name {
          font-weight: bold;
        }
        .sam-appliance-status {
          font-size: 0.9em;
          color: var(--secondary-text-color);
        }
        .sam-appliance-actions {
          display: flex;
          gap: 8px;
        }
        .sam-button {
          background: var(--primary-color);
          color: var(--text-primary-color);
          border: none;
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
        }
        .sam-button:hover {
          opacity: 0.8;
        }
        .sam-button-secondary {
          background: var(--secondary-background-color);
          color: var(--primary-text-color);
        }
        .sam-button-danger {
          background: var(--error-color);
        }
        .sam-checkbox {
          margin-right: 8px;
        }
        .sam-color-input {
          width: 60px;
          height: 32px;
          border: 1px solid var(--divider-color);
          border-radius: 4px;
        }
        .sam-loading {
          text-align: center;
          padding: 32px;
          color: var(--secondary-text-color);
        }
      </style>
      <div class="sam-config-panel">
        <div class="sam-header">
          <h1>⚡ Smart Appliances Configuration</h1>
        </div>
        
        <div class="sam-section">
          <div class="sam-section-title">🌍 Configuration Globale</div>
          <div id="global-settings">
            <label>
              <input type="checkbox" class="sam-checkbox" id="use-custom-cards" />
              Utiliser les cartes personnalisées
            </label>
            <br />
            <label>
              <input type="checkbox" class="sam-checkbox" id="auto-update" />
              Mise à jour automatique
            </label>
            <br />
            <label>
              Couleur principale:
              <input type="color" class="sam-color-input" id="primary-color" value="#3498db" />
            </label>
          </div>
        </div>

        <div class="sam-section">
          <div class="sam-section-title">📊 Dashboard</div>
          <div id="dashboard-status" class="sam-loading">Chargement...</div>
          <div id="dashboard-actions" style="margin-top: 16px; display: none;">
            <button class="sam-button" id="create-dashboard">Créer le Dashboard</button>
            <button class="sam-button sam-button-secondary" id="rebuild-dashboard">Reconstruire</button>
          </div>
        </div>

        <div class="sam-section">
          <div class="sam-section-title">🔧 Appareils (Vues)</div>
          <div id="appliances-list" class="sam-loading">Chargement des appareils...</div>
        </div>

        <div class="sam-section">
          <div class="sam-section-title">📝 Logs</div>
          <div id="logs-container" style="font-family: monospace; font-size: 0.9em;">
            <div>Dashboard configuration panel chargé</div>
          </div>
        </div>
      </div>
    `;

    this.content = this.querySelector(".sam-config-panel");

    // Attach event listeners
    this._attachEventListeners();
  }

  _attachEventListeners() {
    const createBtn = this.querySelector("#create-dashboard");
    if (createBtn) {
      createBtn.addEventListener("click", () => this._createDashboard());
    }

    const rebuildBtn = this.querySelector("#rebuild-dashboard");
    if (rebuildBtn) {
      rebuildBtn.addEventListener("click", () => this._rebuildDashboard());
    }
  }

  async _update() {
    if (!this._hass) return;

    // Load configuration
    await this._loadConfig();

    // Load appliances
    await this._loadAppliances();

    // Check dashboard status
    await this._checkDashboardStatus();
  }

  async _loadConfig() {
    try {
      // Get config via service call (not WebSocket)
      // For now, use default config - in production, this would call a service
      this._config = {
        global_settings: {
          use_custom_cards: true,
          auto_update: true,
          color_scheme: {
            primary: "#3498db",
          },
        },
      };
      this._updateGlobalSettings();
    } catch (err) {
      this._log(`Erreur chargement config: ${err.message}`);
    }
  }

  async _loadAppliances() {
    try {
      // Get all SAM entities
      const states = this._hass.states;
      const applianceStates = Object.values(states).filter(
        (state) =>
          state.entity_id.startsWith("sensor.") &&
          state.entity_id.endsWith("_state") &&
          state.attributes.friendly_name
      );

      this._coordinators = applianceStates;
      this._updateAppliancesList();
    } catch (err) {
      this._log(`Erreur chargement appareils: ${err.message}`);
    }
  }

  async _checkDashboardStatus() {
    const statusDiv = this.querySelector("#dashboard-status");
    const actionsDiv = this.querySelector("#dashboard-actions");

    // Check if dashboard storage file exists
    try {
      // We check indirectly by trying to access the dashboard
      const dashboardExists = await this._checkDashboardFile();

      if (dashboardExists) {
        statusDiv.innerHTML = `
          <div style="color: var(--success-color);">
            ✅ Dashboard créé et disponible
            <br />
            <a href="/lovelace/smart-appliances" target="_blank">Ouvrir le dashboard</a>
          </div>
        `;
      } else {
        statusDiv.innerHTML = `
          <div style="color: var(--warning-color);">
            ⚠️ Dashboard non créé
          </div>
        `;
      }

      actionsDiv.style.display = "block";
    } catch (err) {
      statusDiv.innerHTML = `
        <div style="color: var(--error-color);">
          ❌ Erreur vérification dashboard
        </div>
      `;
      this._log(`Erreur: ${err.message}`);
    }
  }

  async _checkDashboardFile() {
    // Try to call a service to check if dashboard exists
    // For now, we assume it exists if we can see SAM entities
    return this._coordinators.length > 0;
  }

  _updateGlobalSettings() {
    if (!this._config) return;

    const useCustomCards = this.querySelector("#use-custom-cards");
    const autoUpdate = this.querySelector("#auto-update");
    const primaryColor = this.querySelector("#primary-color");

    if (useCustomCards) {
      useCustomCards.checked =
        this._config.global_settings?.use_custom_cards ?? true;
    }
    if (autoUpdate) {
      autoUpdate.checked = this._config.global_settings?.auto_update ?? true;
    }
    if (primaryColor) {
      primaryColor.value =
        this._config.global_settings?.color_scheme?.primary ?? "#3498db";
    }
  }

  _updateAppliancesList() {
    const container = this.querySelector("#appliances-list");
    if (!container) return;

    if (this._coordinators.length === 0) {
      container.innerHTML = `
        <div class="sam-loading">Aucun appareil configuré</div>
      `;
      return;
    }

    const html = this._coordinators
      .map((state) => {
        const name = state.attributes.friendly_name;
        const entityId = state.entity_id;
        const applianceId = entityId.replace("sensor.", "").replace("_state", "");

        return `
        <div class="sam-appliance-item">
          <div class="sam-appliance-info">
            <div class="sam-appliance-name">${name}</div>
            <div class="sam-appliance-status">ID: ${applianceId}</div>
          </div>
          <div class="sam-appliance-actions">
            <button class="sam-button sam-button-secondary" data-action="configure" data-id="${applianceId}">
              ⚙️ Configurer
            </button>
          </div>
        </div>
      `;
      })
      .join("");

    container.innerHTML = html;

    // Attach action buttons
    container.querySelectorAll("[data-action]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const action = e.target.dataset.action;
        const id = e.target.dataset.id;
        this._handleApplianceAction(action, id);
      });
    });
  }

  async _createDashboard() {
    this._log("Génération du fichier YAML...");

    try {
      await this._hass.callService("smart_appliance_monitor", "generate_dashboard_yaml", {});

      this._log("✅ Dashboard YAML généré avec succès !");
      this._log("📋 Vérifiez les notifications pour les instructions de configuration.");
      await this._update();
    } catch (err) {
      this._log(`❌ Erreur génération dashboard: ${err.message}`);
    }
  }

  async _rebuildDashboard() {
    this._log("Régénération du dashboard YAML...");

    try {
      await this._hass.callService(
        "smart_appliance_monitor",
        "generate_dashboard_yaml",
        {}
      );

      this._log("✅ Dashboard YAML régénéré avec succès !");
      this._log("🔄 Redémarrez Home Assistant pour voir les changements.");
      await this._update();
    } catch (err) {
      this._log(`❌ Erreur régénération dashboard: ${err.message}`);
    }
  }

  _handleApplianceAction(action, applianceId) {
    this._log(`Action ${action} pour ${applianceId}`);
    // Implement configuration dialog here
  }

  _log(message) {
    const container = this.querySelector("#logs-container");
    if (!container) return;

    const time = new Date().toLocaleTimeString();
    const logEntry = document.createElement("div");
    logEntry.textContent = `[${time}] ${message}`;
    container.appendChild(logEntry);

    // Keep only last 10 logs
    while (container.children.length > 10) {
      container.removeChild(container.firstChild);
    }
  }
}

customElements.define("sam-config-panel", SamConfigPanel);

