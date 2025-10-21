/**
 * Smart Appliance Stats Card Editor
 * Visual configuration editor
 */

import { LitElement, html, css } from 'lit';
import { fireEvent } from '../utils/helpers.js';

class SmartApplianceStatsCardEditor extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object }
    };
  }

  setConfig(config) {
    this.config = config;
  }

  _valueChanged(ev) {
    if (!this.config || !this.hass) {
      return;
    }

    const target = ev.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    
    if (this.config[target.configValue] === value) {
      return;
    }

    const newConfig = {
      ...this.config,
      [target.configValue]: value
    };

    fireEvent(this, 'config-changed', { config: newConfig });
  }

  render() {
    if (!this.hass || !this.config) {
      return html``;
    }

    return html`
      <div class="card-config">
        <div class="config-section">
          <div class="config-label">Entity (required)</div>
          <ha-entity-picker
            .hass=${this.hass}
            .value=${this.config.entity}
            .configValue=${'entity'}
            @value-changed=${this._valueChanged}
            .includeDomains=${['sensor']}
            allow-custom-entity
          ></ha-entity-picker>
          <div class="config-hint">Select the state sensor (e.g., sensor.washing_machine_state)</div>
        </div>

        <div class="config-section">
          <div class="config-label">Name (optional)</div>
          <ha-textfield
            .value=${this.config.name || ''}
            .configValue=${'name'}
            @input=${this._valueChanged}
            placeholder="Auto-detected from entity"
          ></ha-textfield>
        </div>

        <div class="config-section">
          <div class="config-label">Icon (optional)</div>
          <ha-icon-picker
            .hass=${this.hass}
            .value=${this.config.icon || ''}
            .configValue=${'icon'}
            @value-changed=${this._valueChanged}
            placeholder="mdi:chart-box"
          ></ha-icon-picker>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <div class="config-label">Default tab</div>
          <ha-select
            .value=${this.config.default_tab || 'today'}
            .configValue=${'default_tab'}
            @selected=${this._valueChanged}
          >
            <mwc-list-item value="today">Today</mwc-list-item>
            <mwc-list-item value="week">Week</mwc-list-item>
            <mwc-list-item value="month">Month</mwc-list-item>
          </ha-select>
          <div class="config-hint">Initial tab to display when card loads</div>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <ha-formfield label="Show trend indicators">
            <ha-switch
              .checked=${this.config.show_trends !== false}
              .configValue=${'show_trends'}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Display arrows and percentages for trends</div>
        </div>

        <div class="config-section">
          <ha-formfield label="Show efficiency metrics">
            <ha-switch
              .checked=${this.config.show_efficiency !== false}
              .configValue=${'show_efficiency'}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Show average cost, energy, and duration per cycle</div>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <div class="config-label">Chart type</div>
          <ha-select
            .value=${this.config.chart_type || 'bar'}
            .configValue=${'chart_type'}
            @selected=${this._valueChanged}
          >
            <mwc-list-item value="bar">Bar chart</mwc-list-item>
            <mwc-list-item value="line">Line chart</mwc-list-item>
          </ha-select>
          <div class="config-hint">Type of chart for historical data (future feature)</div>
        </div>

        <div class="config-section">
          <div class="config-label">Theme</div>
          <ha-select
            .value=${this.config.theme || 'auto'}
            .configValue=${'theme'}
            @selected=${this._valueChanged}
          >
            <mwc-list-item value="auto">Auto (follow HA theme)</mwc-list-item>
            <mwc-list-item value="light">Light</mwc-list-item>
            <mwc-list-item value="dark">Dark</mwc-list-item>
          </ha-select>
        </div>
      </div>
    `;
  }

  static get styles() {
    return css`
      .card-config {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 16px;
      }

      .config-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .config-label {
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .config-hint {
        font-size: 12px;
        color: var(--secondary-text-color);
        font-style: italic;
      }

      .config-divider {
        height: 1px;
        background-color: var(--divider-color);
        margin: 8px 0;
      }

      ha-formfield {
        display: flex;
        align-items: center;
      }

      ha-textfield,
      ha-entity-picker,
      ha-icon-picker,
      ha-select {
        width: 100%;
      }
    `;
  }
}

customElements.define('smart-appliance-stats-card-editor', SmartApplianceStatsCardEditor);
