/**
 * Smart Appliance Cycle Card Editor
 * Visual configuration editor
 */

import { LitElement, html, css } from 'lit';
import { fireEvent } from '../utils/helpers.js';

class SmartApplianceCycleCardEditor extends LitElement {
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
            placeholder="Auto-detected from appliance type"
          ></ha-icon-picker>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <ha-formfield label="Show power graph">
            <ha-switch
              .checked=${this.config.show_power_graph !== false}
              .configValue=${'show_power_graph'}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Display mini graph of power consumption</div>
        </div>

        <div class="config-section">
          <ha-formfield label="Show action buttons">
            <ha-switch
              .checked=${this.config.show_action_buttons !== false}
              .configValue=${'show_action_buttons'}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Show start, stop, and reset buttons</div>
        </div>

        <div class="config-section">
          <ha-formfield label="Show current power">
            <ha-switch
              .checked=${this.config.show_current_power === true}
              .configValue=${'show_current_power'}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <div class="config-hint">Display current power consumption value</div>
        </div>

        <div class="config-divider"></div>

        <div class="config-section">
          <div class="config-label">Graph duration (hours)</div>
          <ha-slider
            .value=${this.config.graph_hours || 0.5}
            .configValue=${'graph_hours'}
            @change=${this._valueChanged}
            min="0.25"
            max="2"
            step="0.25"
            labeled
          ></ha-slider>
          <div class="config-hint">Time range for power graph: ${this.config.graph_hours || 0.5}h</div>
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

      ha-slider {
        width: 100%;
      }
    `;
  }
}

customElements.define('smart-appliance-cycle-card-editor', SmartApplianceCycleCardEditor);
