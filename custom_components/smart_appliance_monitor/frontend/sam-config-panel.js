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
          padding: 24px;
          max-width: 1400px;
          margin: 0 auto;
          background: var(--primary-background-color);
        }
        .sam-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 32px;
          padding-bottom: 16px;
          border-bottom: 2px solid var(--divider-color);
        }
        .sam-header-left {
          display: flex;
          align-items: center;
          gap: 16px;
        }
        .sam-header h1 {
          margin: 0;
          font-size: 2.5em;
          font-weight: 700;
          color: var(--primary-text-color);
        }
        .sam-header-badge {
          background: var(--primary-color);
          color: white;
          padding: 6px 14px;
          border-radius: 20px;
          font-size: 0.9em;
          font-weight: 600;
        }
        .sam-card {
          background: var(--card-background-color);
          border-radius: 12px;
          padding: 20px;
          margin-bottom: 20px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .sam-section-title {
          font-size: 1.4em;
          font-weight: 600;
          margin-bottom: 16px;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .sam-appliance-card {
          background: var(--card-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 12px;
          padding: 20px;
          margin-bottom: 16px;
          transition: all 0.3s ease;
          box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .sam-appliance-card:hover {
          transform: translateY(-3px);
          box-shadow: 0 6px 16px rgba(0,0,0,0.12);
          border-color: var(--primary-color);
        }
        .sam-appliance-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }
        .sam-appliance-info {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .sam-appliance-icon {
          font-size: 2em;
        }
        .sam-appliance-name {
          font-size: 1.2em;
          font-weight: 600;
          color: var(--primary-text-color);
        }
        .sam-badge {
          display: inline-block;
          padding: 6px 14px;
          border-radius: 16px;
          font-size: 0.85em;
          font-weight: 600;
          text-transform: uppercase;
        }
        .sam-badge-idle {
          background: #95a5a6;
          color: white;
        }
        .sam-badge-running {
          background: #3498db;
          color: white;
        }
        .sam-badge-finished {
          background: #2ecc71;
          color: white;
        }
        .sam-badge-success {
          background: #2ecc71;
          color: white;
        }
        .sam-badge-warning {
          background: #f39c12;
          color: white;
        }
        .sam-stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 12px;
          margin-top: 12px;
        }
        .sam-stat-item {
          text-align: center;
          padding: 12px;
          background: var(--secondary-background-color);
          border-radius: 8px;
        }
        .sam-stat-value {
          font-size: 1.4em;
          font-weight: 700;
          color: var(--primary-color);
          display: block;
        }
        .sam-stat-label {
          font-size: 0.85em;
          color: var(--secondary-text-color);
          margin-top: 4px;
          display: block;
        }
        .sam-button {
          background: var(--primary-color);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          font-size: 0.95em;
          transition: all 0.2s ease;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .sam-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .sam-button:active {
          transform: translateY(0);
        }
        .sam-button-secondary {
          background: var(--secondary-background-color);
          color: var(--primary-text-color);
        }
        .sam-button-primary {
          background: var(--primary-color);
          color: white;
        }
        .sam-loading {
          text-align: center;
          padding: 48px;
          color: var(--secondary-text-color);
          font-size: 1.1em;
        }
        .sam-modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.6);
          backdrop-filter: blur(4px);
          display: none;
          justify-content: center;
          align-items: center;
          z-index: 1000;
          animation: fadeIn 0.2s ease;
        }
        .sam-modal.show {
          display: flex;
        }
        .sam-modal-content {
          background: var(--card-background-color);
          border-radius: 16px;
          padding: 28px;
          max-width: 650px;
          width: 90%;
          max-height: 85vh;
          overflow-y: auto;
          box-shadow: 0 10px 40px rgba(0,0,0,0.3);
          animation: slideUp 0.3s ease;
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { transform: translateY(20px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
        .sam-modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
          padding-bottom: 16px;
          border-bottom: 2px solid var(--divider-color);
        }
        .sam-modal-title {
          font-size: 1.6em;
          font-weight: 700;
          color: var(--primary-text-color);
        }
        .sam-modal-close {
          background: var(--secondary-background-color);
          border: none;
          width: 36px;
          height: 36px;
          border-radius: 50%;
          font-size: 1.4em;
          cursor: pointer;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
        }
        .sam-modal-close:hover {
          background: var(--error-color);
          color: white;
          transform: rotate(90deg);
        }
        .sam-form-group {
          margin-bottom: 20px;
        }
        .sam-form-label {
          display: block;
          margin-bottom: 12px;
          font-weight: 600;
          font-size: 1.1em;
          color: var(--primary-text-color);
        }
        .sam-checkbox-group {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .sam-checkbox-item {
          display: flex;
          align-items: flex-start;
          padding: 14px;
          background: var(--secondary-background-color);
          border-radius: 10px;
          border: 2px solid transparent;
          transition: all 0.2s ease;
          cursor: pointer;
        }
        .sam-checkbox-item:hover {
          border-color: var(--primary-color);
          background: var(--card-background-color);
        }
        .sam-checkbox-item input {
          margin-right: 14px;
          width: 22px;
          height: 22px;
          cursor: pointer;
          flex-shrink: 0;
          margin-top: 2px;
        }
        .sam-checkbox-item label {
          flex: 1;
          cursor: pointer;
        }
        .sam-checkbox-item .description {
          font-size: 0.9em;
          color: var(--secondary-text-color);
          margin-top: 4px;
          line-height: 1.4;
        }
        .sam-modal-actions {
          display: flex;
          gap: 12px;
          justify-content: flex-end;
          margin-top: 28px;
          padding-top: 20px;
          border-top: 1px solid var(--divider-color);
        }
        .sam-dashboard-status {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 16px;
          background: var(--secondary-background-color);
          border-radius: 10px;
          margin-bottom: 16px;
        }
        .sam-dashboard-status-icon {
          font-size: 2em;
        }
        .sam-logs-container {
          max-height: 200px;
          overflow-y: auto;
          font-family: 'Courier New', monospace;
          font-size: 0.9em;
          background: var(--secondary-background-color);
          padding: 12px;
          border-radius: 8px;
        }
        .sam-log-entry {
          padding: 4px 0;
          border-bottom: 1px solid var(--divider-color);
        }
        .sam-log-entry:last-child {
          border-bottom: none;
        }
      </style>
      <div class="sam-config-panel">
        <div class="sam-header">
          <div class="sam-header-left">
            <h1>⚡ Smart Appliances</h1>
            <span class="sam-header-badge" id="appliances-count">0 appareils</span>
          </div>
        </div>
        
        <div class="sam-card">
          <div class="sam-section-title">📊 Dashboard</div>
          <div id="dashboard-status" class="sam-loading">Chargement...</div>
          <div id="dashboard-actions" style="margin-top: 16px; display: none; display: flex; gap: 12px;">
            <button class="sam-button sam-button-primary" id="create-dashboard">📝 Créer le Dashboard</button>
            <button class="sam-button sam-button-secondary" id="rebuild-dashboard">🔄 Reconstruire</button>
          </div>
        </div>

        <div class="sam-card">
          <div class="sam-section-title">🔧 Appareils</div>
          <div id="appliances-list" class="sam-loading">Chargement des appareils...</div>
        </div>

        <div class="sam-card">
          <div class="sam-section-title">📝 Logs</div>
          <div id="logs-container" class="sam-logs-container">
            <div class="sam-log-entry">✅ Panel de configuration chargé</div>
          </div>
        </div>
      </div>
      
      <!-- Modal for card sections configuration -->
      <div class="sam-modal" id="config-modal">
        <div class="sam-modal-content">
          <div class="sam-modal-header">
            <div class="sam-modal-title" id="modal-title">Configuration</div>
            <button class="sam-modal-close" id="modal-close">×</button>
          </div>
          <div id="modal-body"></div>
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

    const modalClose = this.querySelector("#modal-close");
    if (modalClose) {
      modalClose.addEventListener("click", () => this._closeModal());
    }

    const modal = this.querySelector("#config-modal");
    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          this._closeModal();
        }
      });
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
      // No need for config anymore (removed color settings)
      this._config = { global_settings: {} };
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
      
      // Update appliances count in header
      const countBadge = this.querySelector("#appliances-count");
      if (countBadge) {
        countBadge.textContent = `${applianceStates.length} appareil${applianceStates.length > 1 ? "s" : ""}`;
      }
      
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
        const currentState = state.state || "idle";
        
        // Get badge class based on state
        const badgeClass = `sam-badge-${currentState}`;
        const stateLabel = currentState.charAt(0).toUpperCase() + currentState.slice(1);
        
        // Try to get stats from related entities
        const dailyCyclesEntity = this._hass.states[`sensor.${applianceId}_daily_cycles`] || 
                                   this._hass.states[`sensor.${applianceId}_total_cycles_today`];
        const dailyCostEntity = this._hass.states[`sensor.${applianceId}_daily_cost`];
        const monthlyCyclesEntity = this._hass.states[`sensor.${applianceId}_monthly_cycles`];
        
        const dailyCycles = dailyCyclesEntity ? dailyCyclesEntity.state : "0";
        const dailyCost = dailyCostEntity ? parseFloat(dailyCostEntity.state).toFixed(2) : "0.00";
        const monthlyCycles = monthlyCyclesEntity ? monthlyCyclesEntity.state : "0";

        return `
        <div class="sam-appliance-card">
          <div class="sam-appliance-header">
            <div class="sam-appliance-info">
              <span class="sam-appliance-icon">🔌</span>
              <div>
                <div class="sam-appliance-name">${name}</div>
                <span class="sam-badge ${badgeClass}">${stateLabel}</span>
              </div>
            </div>
            <button class="sam-button sam-button-primary" data-action="configure" data-id="${applianceId}">
              ⚙️ Configurer
            </button>
          </div>
          <div class="sam-stats-grid">
            <div class="sam-stat-item">
              <span class="sam-stat-value">${dailyCycles}</span>
              <span class="sam-stat-label">Cycles Aujourd'hui</span>
            </div>
            <div class="sam-stat-item">
              <span class="sam-stat-value">${dailyCost}€</span>
              <span class="sam-stat-label">Coût Aujourd'hui</span>
            </div>
            <div class="sam-stat-item">
              <span class="sam-stat-value">${monthlyCycles}</span>
              <span class="sam-stat-label">Cycles Ce Mois</span>
            </div>
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
    if (action === "configure") {
      this._openConfigureModal(applianceId);
    }
  }

  _openConfigureModal(applianceId) {
    const modal = this.querySelector("#config-modal");
    const modalTitle = this.querySelector("#modal-title");
    const modalBody = this.querySelector("#modal-body");

    // Find appliance name
    const state = this._coordinators.find(
      (s) => s.entity_id === `sensor.${applianceId}_state`
    );
    const applianceName = state ? state.attributes.friendly_name : applianceId;

    modalTitle.textContent = `⚙️ Configuration - ${applianceName}`;

    // Build form
    const sections = [
      { id: "status", label: "Status", description: "Gauge de puissance et état" },
      {
        id: "statistics_basic",
        label: "Statistiques Basiques",
        description: "Stats aujourd'hui et ce mois",
      },
      {
        id: "statistics_advanced",
        label: "Statistiques Avancées",
        description: "Fréquences, moyennes, tendances",
      },
      {
        id: "current_cycle",
        label: "Cycle en Cours",
        description: "Durée, énergie, coût du cycle actuel",
      },
      {
        id: "power_graph",
        label: "Graphique Puissance",
        description: "Historique de puissance sur 24h",
      },
      { id: "ai_actions", label: "Actions IA", description: "Boutons d'analyse IA" },
      {
        id: "services",
        label: "Services & Actions",
        description: "Export, sync, historique",
      },
      {
        id: "controls",
        label: "Contrôles",
        description: "Monitoring, notifications, reset",
      },
    ];

    const checkboxes = sections
      .map(
        (section) => `
        <div class="sam-checkbox-item">
          <input type="checkbox" id="section-${section.id}" checked />
          <label for="section-${section.id}">
            <div><strong>${section.label}</strong></div>
            <div class="description">${section.description}</div>
          </label>
        </div>
      `
      )
      .join("");

    modalBody.innerHTML = `
      <div class="sam-form-group">
        <div class="sam-form-label">Sections de cartes à afficher :</div>
        <div class="sam-checkbox-group">
          ${checkboxes}
        </div>
      </div>
      <div class="sam-modal-actions">
        <button class="sam-button sam-button-secondary" id="modal-cancel">Annuler</button>
        <button class="sam-button" id="modal-save">💾 Sauvegarder</button>
      </div>
    `;

    // Attach modal actions
    modalBody.querySelector("#modal-cancel").addEventListener("click", () => {
      this._closeModal();
    });

    modalBody.querySelector("#modal-save").addEventListener("click", () => {
      this._saveApplianceConfig(applianceId);
    });

    modal.classList.add("show");
  }

  _closeModal() {
    const modal = this.querySelector("#config-modal");
    modal.classList.remove("show");
  }

  async _saveApplianceConfig(applianceId) {
    const sections = {
      status: this.querySelector("#section-status").checked,
      statistics_basic: this.querySelector("#section-statistics_basic").checked,
      statistics_advanced: this.querySelector("#section-statistics_advanced")
        .checked,
      current_cycle: this.querySelector("#section-current_cycle").checked,
      power_graph: this.querySelector("#section-power_graph").checked,
      ai_actions: this.querySelector("#section-ai_actions").checked,
      services: this.querySelector("#section-services").checked,
      controls: this.querySelector("#section-controls").checked,
    };

    this._log(`Sauvegarde configuration pour ${applianceId}...`);

    try {
      await this._hass.callService("smart_appliance_monitor", "configure_dashboard", {
        appliance_views: {
          [applianceId]: {
            sections_visible: sections,
          },
        },
      });

      this._log(`✅ Configuration sauvegardée pour ${applianceId}`);
      this._closeModal();

      // Rebuild dashboard
      this._log("🔄 Régénération du dashboard...");
      await this._hass.callService(
        "smart_appliance_monitor",
        "generate_dashboard_yaml",
        {}
      );
      this._log("✅ Dashboard régénéré avec succès !");
    } catch (err) {
      this._log(`❌ Erreur sauvegarde: ${err.message}`);
    }
  }

  _log(message) {
    const container = this.querySelector("#logs-container");
    if (!container) return;

    const time = new Date().toLocaleTimeString();
    const logEntry = document.createElement("div");
    logEntry.className = "sam-log-entry";
    logEntry.textContent = `[${time}] ${message}`;
    container.appendChild(logEntry);

    // Keep only last 10 logs
    while (container.children.length > 10) {
      container.removeChild(container.firstChild);
    }
    
    // Auto-scroll to bottom
    container.scrollTop = container.scrollHeight;
  }
}

customElements.define("sam-config-panel", SamConfigPanel);

