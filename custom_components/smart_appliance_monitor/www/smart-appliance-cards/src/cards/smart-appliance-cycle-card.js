/**
 * Smart Appliance Cycle Card
 * Display current cycle/session with visual progress
 */

import { LitElement, html, css } from 'lit';
import { commonStyles } from '../styles/common-styles.js';
import './cycle-card-editor.js';
import {
  getRelatedEntities,
  getApplianceType,
  getTerminology,
  getApplianceIcon,
  getEntityState,
  getNumericState,
  callService,
  fireEvent
} from '../utils/helpers.js';
import {
  formatDuration,
  formatEnergy,
  formatPower,
  formatCost
} from '../utils/formatters.js';
import {
  STATES,
  STATE_COLORS,
  STATE_ICONS,
  DEFAULT_CONFIG,
  UPDATE_INTERVALS,
  CARD_VERSION
} from '../utils/constants.js';

class SmartApplianceCycleCard extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
      _entities: { type: Object },
      _applianceType: { type: String },
      _terminology: { type: String },
      _updateInterval: { type: Number }
    };
  }

  static getConfigElement() {
    return document.createElement('smart-appliance-cycle-card-editor');
  }

  static getStubConfig() {
    return {
      entity: 'sensor.washing_machine_state',
      show_power_graph: true,
      show_action_buttons: true,
      show_current_power: false,
      graph_hours: 0.5,
      theme: 'auto'
    };
  }

  constructor() {
    super();
    this._entities = null;
    this._applianceType = 'generic';
    this._terminology = 'cycle';
    this._updateInterval = null;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }

    this.config = {
      ...DEFAULT_CONFIG.cycle_card,
      ...config
    };
  }

  connectedCallback() {
    super.connectedCallback();
    this._startAutoUpdate();
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this._stopAutoUpdate();
  }

  updated(changedProps) {
    super.updated(changedProps);
    
    if (changedProps.has('hass') || changedProps.has('config')) {
      if (this.hass && this.config?.entity) {
        this._entities = getRelatedEntities(this.hass, this.config.entity);
        this._applianceType = getApplianceType(this.hass, this.config.entity);
        this._terminology = getTerminology(this._applianceType);
      }
    }
  }

  _startAutoUpdate() {
    this._stopAutoUpdate();
    this._updateInterval = setInterval(() => {
      this.requestUpdate();
    }, UPDATE_INTERVALS.FAST);
  }

  _stopAutoUpdate() {
    if (this._updateInterval) {
      clearInterval(this._updateInterval);
      this._updateInterval = null;
    }
  }

  _getState() {
    if (!this._entities) return STATES.UNKNOWN;
    const state = getEntityState(this.hass, this._entities.state);
    return state || STATES.UNKNOWN;
  }

  _isRunning() {
    return this._getState() === STATES.RUNNING;
  }

  _isFinished() {
    return this._getState() === STATES.FINISHED;
  }

  _isIdle() {
    return this._getState() === STATES.IDLE;
  }

  _isUnplugged() {
    if (!this._entities) return false;
    return getEntityState(this.hass, this._entities.unplugged) === 'on';
  }

  _hasAlert() {
    if (!this._entities) return false;
    return getEntityState(this.hass, this._entities.duration_alert) === 'on';
  }

  _isMonitoring() {
    if (!this._entities) return true;
    return getEntityState(this.hass, this._entities.monitoring) === 'on';
  }

  _getCurrentDuration() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.cycle_duration) || 0;
  }

  _getCurrentEnergy() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.cycle_energy) || 0;
  }

  _getCurrentCost() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.cycle_cost) || 0;
  }

  _handleStopMonitoring() {
    if (!this._entities) return;
    callService(this.hass, 'switch', 'turn_off', {
      entity_id: this._entities.monitoring
    });
  }

  _handleResetStats() {
    if (!this._entities) return;
    callService(this.hass, 'button', 'press', {
      entity_id: this._entities.reset_stats
    });
  }

  _handleStartCycle() {
    if (!this.config.entity) return;
    const baseName = this.config.entity.replace('sensor.', '').replace('_state', '');
    callService(this.hass, 'smart_appliance_monitor', 'start_cycle', {
      entity_id: `sensor.${baseName}_state`
    });
  }

  _renderStatusIndicator() {
    const state = this._getState();
    const icon = STATE_ICONS[state] || STATE_ICONS.unknown;
    const color = STATE_COLORS[state] || STATE_COLORS.unknown;
    const isRunning = this._isRunning();

    return html`
      <div class="status-indicator ${isRunning ? 'pulse' : ''}">
        <div 
          class="status-circle" 
          style="background-color: ${color};"
        >
          <ha-icon 
            icon="${icon}"
            class="${isRunning ? 'rotate' : ''}"
          ></ha-icon>
        </div>
        <div class="status-text">
          <div class="status-label">${state}</div>
          <div class="status-sublabel">${this._terminology}</div>
        </div>
      </div>
    `;
  }

  _renderCurrentValues() {
    const duration = this._getCurrentDuration();
    const energy = this._getCurrentEnergy();
    const cost = this._getCurrentCost();

    return html`
      <div class="current-values">
        <div class="value-row">
          <span class="value-label">
            <ha-icon icon="mdi:timer-outline"></ha-icon>
            Duration
          </span>
          <span class="value-text">${formatDuration(duration)}</span>
        </div>
        
        <div class="value-row">
          <span class="value-label">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
            Energy
          </span>
          <span class="value-text">${formatEnergy(energy)}</span>
        </div>
        
        <div class="value-row">
          <span class="value-label">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
            Cost
          </span>
          <span class="value-text">${formatCost(cost)}</span>
        </div>
      </div>
    `;
  }

  _renderActionButtons() {
    if (!this.config.show_action_buttons) return html``;

    const state = this._getState();
    const canReset = state === STATES.IDLE || state === STATES.FINISHED;
    const canStart = state === STATES.IDLE;

    return html`
      <div class="action-buttons">
        ${canStart ? html`
          <button class="button" @click="${this._handleStartCycle}">
            <ha-icon icon="mdi:play"></ha-icon>
            Start ${this._terminology}
          </button>
        ` : ''}
        
        ${this._isRunning() ? html`
          <button class="button button-danger" @click="${this._handleStopMonitoring}">
            <ha-icon icon="mdi:stop"></ha-icon>
            Stop Monitoring
          </button>
        ` : ''}
        
        ${canReset ? html`
          <button class="button button-secondary" @click="${this._handleResetStats}">
            <ha-icon icon="mdi:refresh"></ha-icon>
            Reset Stats
          </button>
        ` : ''}
      </div>
    `;
  }

  _renderAlerts() {
    const alerts = [];

    if (this._isUnplugged()) {
      alerts.push(html`
        <div class="alert-container alert-error">
          <ha-icon icon="mdi:power-plug-off"></ha-icon>
          <span>Appliance is unplugged or powered off</span>
        </div>
      `);
    }

    if (this._hasAlert()) {
      alerts.push(html`
        <div class="alert-container alert-warning">
          <ha-icon icon="mdi:alert"></ha-icon>
          <span>${this._terminology} duration exceeds expected time</span>
        </div>
      `);
    }

    if (!this._isMonitoring() && !this._isUnplugged()) {
      alerts.push(html`
        <div class="alert-container alert-info">
          <ha-icon icon="mdi:information"></ha-icon>
          <span>Monitoring is currently disabled</span>
        </div>
      `);
    }

    return alerts;
  }

  render() {
    if (!this.hass || !this.config) {
      return html`<div class="loading">Loading...</div>`;
    }

    if (!this._entities) {
      return html`
        <ha-card>
          <div class="card">
            <div class="alert-container alert-error">
              <ha-icon icon="mdi:alert-circle"></ha-icon>
              <span>Entity not found: ${this.config.entity}</span>
            </div>
          </div>
        </ha-card>
      `;
    }

    const name = this.config.name || this.hass.states[this.config.entity]?.attributes?.friendly_name || 'Appliance';
    const icon = this.config.icon || getApplianceIcon(this._applianceType);

    return html`
      <ha-card>
        <div class="card fade-in">
          <div class="card-header">
            <h2 class="card-title">
              <ha-icon icon="${icon}"></ha-icon>
              ${name}
            </h2>
          </div>

          ${this._renderAlerts()}
          
          ${this._renderStatusIndicator()}
          
          <div class="divider"></div>
          
          ${this._renderCurrentValues()}
          
          ${this._renderActionButtons()}
        </div>
      </ha-card>
    `;
  }

  static get styles() {
    return [
      commonStyles,
      css`
        :host {
          display: block;
        }

        ha-card {
          height: 100%;
        }

        .status-indicator {
          display: flex;
          align-items: center;
          gap: var(--sac-spacing);
          margin: var(--sac-spacing) 0;
        }

        .status-circle {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: var(--sac-shadow-md);
        }

        .status-circle ha-icon {
          --mdc-icon-size: 40px;
          color: white;
        }

        .status-text {
          flex: 1;
        }

        .status-label {
          font-size: 24px;
          font-weight: 600;
          color: var(--sac-text-primary);
          text-transform: capitalize;
        }

        .status-sublabel {
          font-size: 14px;
          color: var(--sac-text-secondary);
          text-transform: capitalize;
        }

        .current-values {
          margin: var(--sac-spacing) 0;
        }

        .action-buttons {
          display: flex;
          flex-direction: column;
          gap: var(--sac-spacing-sm);
          margin-top: var(--sac-spacing);
        }

        @media (max-width: 480px) {
          .status-circle {
            width: 60px;
            height: 60px;
          }

          .status-circle ha-icon {
            --mdc-icon-size: 30px;
          }

          .status-label {
            font-size: 20px;
          }
        }
      `
    ];
  }

  getCardSize() {
    return 4;
  }
}

customElements.define('smart-appliance-cycle-card', SmartApplianceCycleCard);

// Announce card to Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'smart-appliance-cycle-card',
  name: 'Smart Appliance Cycle Card',
  description: 'Display current cycle/session with visual progress',
  preview: true,
  documentationURL: 'https://github.com/legaetan/ha-smart_appliance_monitor/wiki'
});

console.info(
  `%c SMART-APPLIANCE-CYCLE-CARD %c v${CARD_VERSION} `,
  'color: white; background: #4caf50; font-weight: 700;',
  'color: #4caf50; background: white; font-weight: 700;'
);
