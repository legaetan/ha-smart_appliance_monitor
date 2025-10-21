/**
 * Smart Appliance Stats Card
 * Comprehensive statistics display with tabbed interface
 */

import { LitElement, html, css } from 'lit';
import { commonStyles } from '../styles/common-styles.js';
import './stats-card-editor.js';
import {
  getRelatedEntities,
  getApplianceType,
  getTerminology,
  getApplianceIcon,
  getEntityState,
  getNumericState,
  getTrend
} from '../utils/helpers.js';
import {
  formatDuration,
  formatEnergy,
  formatCost,
  formatPercent,
  formatNumber
} from '../utils/formatters.js';
import {
  DEFAULT_CONFIG,
  TIME_PERIODS,
  UPDATE_INTERVALS,
  CARD_VERSION
} from '../utils/constants.js';

class SmartApplianceStatsCard extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
      _entities: { type: Object },
      _applianceType: { type: String },
      _terminology: { type: String },
      _activeTab: { type: String },
      _updateInterval: { type: Number }
    };
  }

  static getConfigElement() {
    return document.createElement('smart-appliance-stats-card-editor');
  }

  static getStubConfig() {
    return {
      entity: 'sensor.washing_machine_state',
      default_tab: 'today',
      show_trends: true,
      show_efficiency: true,
      chart_type: 'bar',
      theme: 'auto'
    };
  }

  constructor() {
    super();
    this._entities = null;
    this._applianceType = 'generic';
    this._terminology = 'cycle';
    this._activeTab = TIME_PERIODS.TODAY;
    this._updateInterval = null;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }

    this.config = {
      ...DEFAULT_CONFIG.stats_card,
      ...config
    };
    
    this._activeTab = this.config.default_tab || TIME_PERIODS.TODAY;
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
    }, UPDATE_INTERVALS.SLOW);
  }

  _stopAutoUpdate() {
    if (this._updateInterval) {
      clearInterval(this._updateInterval);
      this._updateInterval = null;
    }
  }

  _handleTabClick(tab) {
    this._activeTab = tab;
    this.requestUpdate();
  }

  _getDailyCycles() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.daily_cycles) || 0;
  }

  _getDailyCost() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.daily_cost) || 0;
  }

  _getMonthlyCost() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.monthly_cost) || 0;
  }

  _getLastCycleDuration() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.last_cycle_duration) || 0;
  }

  _getLastCycleEnergy() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.last_cycle_energy) || 0;
  }

  _getLastCycleCost() {
    if (!this._entities) return 0;
    return getNumericState(this.hass, this._entities.last_cycle_cost) || 0;
  }

  _renderTabs() {
    return html`
      <div class="tabs">
        <button
          class="tab ${this._activeTab === TIME_PERIODS.TODAY ? 'active' : ''}"
          @click=${() => this._handleTabClick(TIME_PERIODS.TODAY)}
        >
          <ha-icon icon="mdi:calendar-today"></ha-icon>
          Today
        </button>
        <button
          class="tab ${this._activeTab === TIME_PERIODS.WEEK ? 'active' : ''}"
          @click=${() => this._handleTabClick(TIME_PERIODS.WEEK)}
        >
          <ha-icon icon="mdi:calendar-week"></ha-icon>
          Week
        </button>
        <button
          class="tab ${this._activeTab === TIME_PERIODS.MONTH ? 'active' : ''}"
          @click=${() => this._handleTabClick(TIME_PERIODS.MONTH)}
        >
          <ha-icon icon="mdi:calendar-month"></ha-icon>
          Month
        </button>
      </div>
    `;
  }

  _renderTodayView() {
    const cycles = this._getDailyCycles();
    const cost = this._getDailyCost();
    const lastEnergy = this._getLastCycleEnergy();
    const lastDuration = this._getLastCycleDuration();

    // Mock data for yesterday comparison (would need history in real implementation)
    const yesterdayCycles = Math.max(0, cycles - 1);
    const trend = getTrend(cycles, yesterdayCycles);

    return html`
      <div class="stats-view fade-in">
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:counter"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">${this._terminology}s</div>
            <div class="stat-value">${formatNumber(cycles, 0)}</div>
            ${this.config.show_trends ? html`
              <div class="stat-trend ${trend.direction}">
                ${this._renderTrendIcon(trend.direction)}
                ${formatPercent(trend.percentage)}
              </div>
            ` : ''}
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Energy</div>
            <div class="stat-value">${formatEnergy(lastEnergy * cycles)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Cost</div>
            <div class="stat-value">${formatCost(cost)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:timer"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Avg Duration</div>
            <div class="stat-value">${formatDuration(lastDuration, true)}</div>
          </div>
        </div>
      </div>
    `;
  }

  _renderWeekView() {
    const cycles = this._getDailyCycles() * 7; // Mock weekly data
    const cost = this._getDailyCost() * 7;
    const energy = this._getLastCycleEnergy() * cycles;

    return html`
      <div class="stats-view fade-in">
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:counter"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total ${this._terminology}s</div>
            <div class="stat-value">${formatNumber(cycles, 0)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total Energy</div>
            <div class="stat-value">${formatEnergy(energy)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total Cost</div>
            <div class="stat-value">${formatCost(cost)}</div>
          </div>
        </div>

        <div class="info-message">
          <ha-icon icon="mdi:information"></ha-icon>
          Weekly statistics require history data
        </div>
      </div>
    `;
  }

  _renderMonthView() {
    const monthlyCost = this._getMonthlyCost();
    const cycles = this._getDailyCycles() * 30; // Mock monthly data
    const energy = this._getLastCycleEnergy() * cycles;

    return html`
      <div class="stats-view fade-in">
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:counter"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total ${this._terminology}s</div>
            <div class="stat-value">${formatNumber(cycles, 0)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:lightning-bolt"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Total Energy</div>
            <div class="stat-value">${formatEnergy(energy)}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="mdi:currency-eur"></ha-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">Monthly Cost</div>
            <div class="stat-value">${formatCost(monthlyCost)}</div>
          </div>
        </div>

        <div class="info-message">
          <ha-icon icon="mdi:information"></ha-icon>
          Monthly statistics require history data
        </div>
      </div>
    `;
  }

  _renderTrendIcon(direction) {
    switch (direction) {
    case 'up':
      return html`<ha-icon icon="mdi:arrow-up" class="trend-up"></ha-icon>`;
    case 'down':
      return html`<ha-icon icon="mdi:arrow-down" class="trend-down"></ha-icon>`;
    default:
      return html`<ha-icon icon="mdi:arrow-right" class="trend-stable"></ha-icon>`;
    }
  }

  _renderEfficiency() {
    if (!this.config.show_efficiency) return html``;

    const avgCost = this._getLastCycleCost();
    const avgEnergy = this._getLastCycleEnergy();
    const avgDuration = this._getLastCycleDuration();

    return html`
      <div class="divider"></div>
      <div class="efficiency-section">
        <h3 class="section-title">
          <ha-icon icon="mdi:gauge"></ha-icon>
          Efficiency Metrics
        </h3>
        <div class="efficiency-grid">
          <div class="efficiency-item">
            <span class="efficiency-label">Avg Cost/${this._terminology}</span>
            <span class="efficiency-value">${formatCost(avgCost)}</span>
          </div>
          <div class="efficiency-item">
            <span class="efficiency-label">Avg Energy/${this._terminology}</span>
            <span class="efficiency-value">${formatEnergy(avgEnergy)}</span>
          </div>
          <div class="efficiency-item">
            <span class="efficiency-label">Avg Duration</span>
            <span class="efficiency-value">${formatDuration(avgDuration, true)}</span>
          </div>
        </div>
      </div>
    `;
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

    const name = this.config.name || 
      (this.hass.states[this.config.entity]?.attributes?.friendly_name + ' Statistics') || 
      'Appliance Statistics';
    const icon = this.config.icon || 'mdi:chart-box';

    return html`
      <ha-card>
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">
              <ha-icon icon="${icon}"></ha-icon>
              ${name}
            </h2>
          </div>

          ${this._renderTabs()}

          ${this._activeTab === TIME_PERIODS.TODAY ? this._renderTodayView() : ''}
          ${this._activeTab === TIME_PERIODS.WEEK ? this._renderWeekView() : ''}
          ${this._activeTab === TIME_PERIODS.MONTH ? this._renderMonthView() : ''}

          ${this._renderEfficiency()}
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

        .tabs {
          display: flex;
          gap: var(--sac-spacing-sm);
          margin-bottom: var(--sac-spacing);
          border-bottom: 2px solid var(--sac-divider-color);
        }

        .tab {
          flex: 1;
          background: none;
          border: none;
          border-bottom: 2px solid transparent;
          padding: var(--sac-spacing-sm);
          cursor: pointer;
          color: var(--sac-text-secondary);
          font-size: 14px;
          font-weight: 500;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          transition: all var(--sac-transition-fast);
          margin-bottom: -2px;
        }

        .tab:hover {
          color: var(--sac-text-primary);
          background-color: rgba(0, 0, 0, 0.05);
        }

        .tab.active {
          color: var(--sac-primary-color);
          border-bottom-color: var(--sac-primary-color);
        }

        .stats-view {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: var(--sac-spacing);
        }

        .stat-card {
          background: rgba(0, 0, 0, 0.02);
          border-radius: 8px;
          padding: var(--sac-spacing);
          display: flex;
          gap: var(--sac-spacing-sm);
          align-items: flex-start;
        }

        .stat-icon {
          width: 40px;
          height: 40px;
          background: var(--sac-primary-color);
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .stat-icon ha-icon {
          --mdc-icon-size: 24px;
          color: white;
        }

        .stat-content {
          flex: 1;
          min-width: 0;
        }

        .stat-label {
          font-size: 12px;
          color: var(--sac-text-secondary);
          margin-bottom: 4px;
        }

        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: var(--sac-text-primary);
        }

        .stat-trend {
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
          margin-top: 4px;
        }

        .stat-trend.up {
          color: var(--sac-state-error);
        }

        .stat-trend.down {
          color: var(--sac-state-running);
        }

        .stat-trend.stable {
          color: var(--sac-text-secondary);
        }

        .trend-up,
        .trend-down,
        .trend-stable {
          --mdc-icon-size: 16px;
        }

        .section-title {
          font-size: 16px;
          font-weight: 500;
          color: var(--sac-text-primary);
          margin: 0 0 var(--sac-spacing-sm) 0;
          display: flex;
          align-items: center;
          gap: var(--sac-spacing-sm);
        }

        .efficiency-section {
          margin-top: var(--sac-spacing);
        }

        .efficiency-grid {
          display: grid;
          gap: var(--sac-spacing-sm);
        }

        .efficiency-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: var(--sac-spacing-sm);
          background: rgba(0, 0, 0, 0.02);
          border-radius: 6px;
        }

        .efficiency-label {
          font-size: 14px;
          color: var(--sac-text-secondary);
        }

        .efficiency-value {
          font-size: 14px;
          font-weight: 500;
          color: var(--sac-text-primary);
        }

        .info-message {
          grid-column: 1 / -1;
          padding: var(--sac-spacing-sm);
          background: rgba(33, 150, 243, 0.1);
          border-radius: 6px;
          color: var(--sac-text-secondary);
          font-size: 13px;
          display: flex;
          align-items: center;
          gap: var(--sac-spacing-sm);
        }

        @media (max-width: 480px) {
          .stats-view {
            grid-template-columns: 1fr;
          }

          .tab {
            font-size: 12px;
            padding: 6px;
          }

          .stat-value {
            font-size: 18px;
          }
        }
      `
    ];
  }

  getCardSize() {
    return 5;
  }
}

customElements.define('smart-appliance-stats-card', SmartApplianceStatsCard);

// Announce card to Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'smart-appliance-stats-card',
  name: 'Smart Appliance Stats Card',
  description: 'Comprehensive statistics display with tabbed interface',
  preview: true,
  documentationURL: 'https://github.com/legaetan/ha-smart_appliance_monitor/wiki'
});

console.info(
  `%c SMART-APPLIANCE-STATS-CARD %c v${CARD_VERSION} `,
  'color: white; background: #2196f3; font-weight: 700;',
  'color: #2196f3; background: white; font-weight: 700;'
);
