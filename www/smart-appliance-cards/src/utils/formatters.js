/**
 * Formatting utilities for Smart Appliance Cards
 */

/**
 * Format duration in seconds to human-readable format
 * @param {number} seconds - Duration in seconds
 * @param {boolean} compact - Use compact format (e.g., "2h 30m" vs "2h 30m 15s")
 * @returns {string} Formatted duration
 */
export function formatDuration(seconds, compact = false) {
  if (!seconds || seconds < 0) return '0s';
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  const parts = [];
  
  if (hours > 0) {
    parts.push(`${hours}h`);
  }
  if (minutes > 0) {
    parts.push(`${minutes}m`);
  }
  if (!compact && secs > 0 && hours === 0) {
    parts.push(`${secs}s`);
  }
  
  return parts.length > 0 ? parts.join(' ') : '0s';
}

/**
 * Format energy consumption
 * @param {number} kwh - Energy in kWh
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted energy
 */
export function formatEnergy(kwh, decimals = 2) {
  if (!kwh || kwh < 0) return '0 kWh';
  
  if (kwh < 1) {
    // Show in Wh for values < 1 kWh
    const wh = Math.round(kwh * 1000);
    return `${wh} Wh`;
  }
  
  return `${kwh.toFixed(decimals)} kWh`;
}

/**
 * Format power consumption
 * @param {number} watts - Power in watts
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted power
 */
export function formatPower(watts, decimals = 0) {
  if (!watts || watts < 0) return '0 W';
  
  if (watts >= 1000) {
    // Show in kW for values >= 1000 W
    const kw = watts / 1000;
    return `${kw.toFixed(1)} kW`;
  }
  
  return `${watts.toFixed(decimals)} W`;
}

/**
 * Format cost
 * @param {number} value - Cost value
 * @param {string} currency - Currency symbol
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted cost
 */
export function formatCost(value, currency = '€', decimals = 2) {
  if (!value || value < 0) return `0.00 ${currency}`;
  
  return `${value.toFixed(decimals)} ${currency}`;
}

/**
 * Format percentage
 * @param {number} value - Percentage value
 * @param {boolean} includeSign - Include + sign for positive values
 * @returns {string} Formatted percentage
 */
export function formatPercent(value, includeSign = true) {
  if (!value && value !== 0) return '0%';
  
  const sign = includeSign && value > 0 ? '+' : '';
  return `${sign}${Math.round(value)}%`;
}

/**
 * Format date
 * @param {Date|string} date - Date object or string
 * @param {string} format - Format type ('short', 'long', 'time')
 * @returns {string} Formatted date
 */
export function formatDate(date, format = 'short') {
  const d = date instanceof Date ? date : new Date(date);
  
  if (format === 'time') {
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  
  if (format === 'long') {
    return d.toLocaleDateString([], { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }
  
  // Short format (default)
  return d.toLocaleDateString([], { 
    month: 'short', 
    day: 'numeric' 
  });
}

/**
 * Format number with locale
 * @param {number} value - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number
 */
export function formatNumber(value, decimals = 0) {
  if (!value && value !== 0) return '0';
  
  return value.toLocaleString(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

/**
 * Get relative time string (e.g., "2 hours ago")
 * @param {Date|string} date - Date to compare
 * @returns {string} Relative time string
 */
export function getRelativeTime(date) {
  const d = date instanceof Date ? date : new Date(date);
  const now = new Date();
  const diffMs = now - d;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  
  if (diffSec < 60) return 'just now';
  if (diffMin < 60) return `${diffMin} min ago`;
  if (diffHour < 24) return `${diffHour} hour${diffHour > 1 ? 's' : ''} ago`;
  if (diffDay < 7) return `${diffDay} day${diffDay > 1 ? 's' : ''} ago`;
  
  return formatDate(d);
}
