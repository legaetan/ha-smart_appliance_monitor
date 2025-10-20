/**
 * Helper utilities for Smart Appliance Cards
 */

import { APPLIANCE_TERMINOLOGY, APPLIANCE_ICONS } from './constants.js';

/**
 * Get related entities for an appliance based on the main entity ID
 * @param {Object} hass - Home Assistant object
 * @param {string} mainEntity - Main entity ID (e.g., sensor.washing_machine_state)
 * @returns {Object} Object with all related entity IDs
 */
export function getRelatedEntities(hass, mainEntity) {
  if (!mainEntity || !hass) return null;
  
  // Extract the base name from the entity ID
  // e.g., "sensor.washing_machine_state" -> "washing_machine"
  const match = mainEntity.match(/^sensor\.(.+)_state$/);
  if (!match) return null;
  
  const baseName = match[1];
  
  return {
    // Main entity
    state: mainEntity,
    
    // Sensors
    cycle_duration: `sensor.${baseName}_cycle_duration`,
    cycle_energy: `sensor.${baseName}_cycle_energy`,
    cycle_cost: `sensor.${baseName}_cycle_cost`,
    last_cycle_duration: `sensor.${baseName}_last_cycle_duration`,
    last_cycle_energy: `sensor.${baseName}_last_cycle_energy`,
    last_cycle_cost: `sensor.${baseName}_last_cycle_cost`,
    daily_cycles: `sensor.${baseName}_daily_cycles`,
    daily_cost: `sensor.${baseName}_daily_cost`,
    monthly_cost: `sensor.${baseName}_monthly_cost`,
    
    // Binary sensors
    running: `binary_sensor.${baseName}_running`,
    duration_alert: `binary_sensor.${baseName}_duration_alert`,
    unplugged: `binary_sensor.${baseName}_unplugged`,
    
    // Switches
    monitoring: `switch.${baseName}_monitoring`,
    notifications: `switch.${baseName}_notifications`,
    notify_started: `switch.${baseName}_notify_cycle_started`,
    notify_finished: `switch.${baseName}_notify_cycle_finished`,
    notify_alert: `switch.${baseName}_notify_alert_duration`,
    notify_unplugged: `switch.${baseName}_notify_unplugged`,
    
    // Button
    reset_stats: `button.${baseName}_reset_statistics`
  };
}

/**
 * Get the appliance type from entity or config
 * @param {Object} hass - Home Assistant object
 * @param {string} entity - Entity ID
 * @returns {string} Appliance type (e.g., 'washing_machine', 'dishwasher')
 */
export function getApplianceType(hass, entity) {
  if (!hass || !entity) return 'generic';
  
  const stateObj = hass.states[entity];
  if (!stateObj) return 'generic';
  
  // Try to get from entity attributes
  const applianceType = stateObj.attributes?.appliance_type;
  if (applianceType) return applianceType;
  
  // Try to infer from entity ID
  const entityLower = entity.toLowerCase();
  
  if (entityLower.includes('washing')) return 'washing_machine';
  if (entityLower.includes('dishwasher')) return 'dishwasher';
  if (entityLower.includes('dryer')) return 'dryer';
  if (entityLower.includes('oven')) return 'oven';
  if (entityLower.includes('water') && entityLower.includes('heater')) return 'water_heater';
  if (entityLower.includes('coffee')) return 'coffee_maker';
  if (entityLower.includes('monitor') || entityLower.includes('screen')) return 'monitor';
  if (entityLower.includes('nas')) return 'nas';
  if (entityLower.includes('printer') && entityLower.includes('3d')) return 'printer_3d';
  if (entityLower.includes('vmc') || entityLower.includes('ventilation')) return 'vmc';
  
  return 'generic';
}

/**
 * Get terminology (cycle or session) based on appliance type
 * @param {string} applianceType - Appliance type
 * @returns {string} 'cycle' or 'session'
 */
export function getTerminology(applianceType) {
  return APPLIANCE_TERMINOLOGY[applianceType] || 'cycle';
}

/**
 * Get icon for appliance type
 * @param {string} applianceType - Appliance type
 * @returns {string} Icon name (e.g., 'mdi:washing-machine')
 */
export function getApplianceIcon(applianceType) {
  return APPLIANCE_ICONS[applianceType] || APPLIANCE_ICONS.generic;
}

/**
 * Get entity state value
 * @param {Object} hass - Home Assistant object
 * @param {string} entityId - Entity ID
 * @returns {string|number|null} State value
 */
export function getEntityState(hass, entityId) {
  if (!hass || !entityId) return null;
  
  const stateObj = hass.states[entityId];
  if (!stateObj) return null;
  
  return stateObj.state;
}

/**
 * Get entity attribute value
 * @param {Object} hass - Home Assistant object
 * @param {string} entityId - Entity ID
 * @param {string} attribute - Attribute name
 * @returns {any} Attribute value
 */
export function getEntityAttribute(hass, entityId, attribute) {
  if (!hass || !entityId) return null;
  
  const stateObj = hass.states[entityId];
  if (!stateObj || !stateObj.attributes) return null;
  
  return stateObj.attributes[attribute];
}

/**
 * Get numeric state value (convert string to number if needed)
 * @param {Object} hass - Home Assistant object
 * @param {string} entityId - Entity ID
 * @returns {number|null} Numeric state value
 */
export function getNumericState(hass, entityId) {
  const state = getEntityState(hass, entityId);
  if (state === null || state === 'unknown' || state === 'unavailable') return null;
  
  const num = parseFloat(state);
  return isNaN(num) ? null : num;
}

/**
 * Call a Home Assistant service
 * @param {Object} hass - Home Assistant object
 * @param {string} domain - Service domain
 * @param {string} service - Service name
 * @param {Object} data - Service data
 */
export function callService(hass, domain, service, data = {}) {
  if (!hass) return;
  
  hass.callService(domain, service, data);
}

/**
 * Fire a Home Assistant event
 * @param {Object} element - Custom element
 * @param {string} type - Event type
 * @param {Object} detail - Event detail
 */
export function fireEvent(element, type, detail = {}) {
  const event = new Event(type, {
    bubbles: true,
    composed: true,
    cancelable: false
  });
  event.detail = detail;
  element.dispatchEvent(event);
}

/**
 * Calculate statistics from history data
 * @param {Array} history - Array of history states
 * @param {string} period - Time period ('today', 'week', 'month')
 * @returns {Object} Statistics object
 */
export function calculateStats(history, period = 'today') {
  if (!history || history.length === 0) {
    return {
      count: 0,
      total_energy: 0,
      total_cost: 0,
      avg_duration: 0,
      max_power: 0,
      min_power: 0
    };
  }
  
  // This is a simplified version - actual implementation would need
  // to process the history data based on the period
  const stats = {
    count: history.length,
    total_energy: 0,
    total_cost: 0,
    avg_duration: 0,
    max_power: 0,
    min_power: Infinity
  };
  
  history.forEach(entry => {
    if (entry.attributes) {
      stats.total_energy += parseFloat(entry.attributes.energy || 0);
      stats.total_cost += parseFloat(entry.attributes.cost || 0);
      stats.avg_duration += parseFloat(entry.attributes.duration || 0);
      
      const power = parseFloat(entry.attributes.power || 0);
      if (power > stats.max_power) stats.max_power = power;
      if (power < stats.min_power && power > 0) stats.min_power = power;
    }
  });
  
  if (stats.count > 0) {
    stats.avg_duration = stats.avg_duration / stats.count;
  }
  
  if (stats.min_power === Infinity) stats.min_power = 0;
  
  return stats;
}

/**
 * Get trend direction and percentage
 * @param {number} current - Current value
 * @param {number} previous - Previous value
 * @returns {Object} Trend object with direction and percentage
 */
export function getTrend(current, previous) {
  if (!previous || previous === 0) {
    return { direction: 'stable', percentage: 0 };
  }
  
  const diff = current - previous;
  const percentage = (diff / previous) * 100;
  
  let direction = 'stable';
  if (percentage > 10) direction = 'up';
  else if (percentage < -10) direction = 'down';
  
  return { direction, percentage };
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait = 300) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Deep merge two objects
 * @param {Object} target - Target object
 * @param {Object} source - Source object
 * @returns {Object} Merged object
 */
export function deepMerge(target, source) {
  const output = Object.assign({}, target);
  
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach(key => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          Object.assign(output, { [key]: source[key] });
        } else {
          output[key] = deepMerge(target[key], source[key]);
        }
      } else {
        Object.assign(output, { [key]: source[key] });
      }
    });
  }
  
  return output;
}

/**
 * Check if value is an object
 * @param {any} item - Item to check
 * @returns {boolean} True if object
 */
function isObject(item) {
  return item && typeof item === 'object' && !Array.isArray(item);
}
