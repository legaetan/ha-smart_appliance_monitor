/**
 * Constants for Smart Appliance Cards
 */

// Appliance states
export const STATES = {
  IDLE: 'idle',
  RUNNING: 'running',
  FINISHED: 'finished',
  UNKNOWN: 'unknown'
};

// State colors
export const STATE_COLORS = {
  idle: '#9e9e9e',
  running: '#4caf50',
  finished: '#2196f3',
  unknown: '#ff9800'
};

// State icons
export const STATE_ICONS = {
  idle: 'mdi:power-standby',
  running: 'mdi:play-circle',
  finished: 'mdi:check-circle',
  unknown: 'mdi:help-circle'
};

// Appliance type terminology (cycle vs session)
export const APPLIANCE_TERMINOLOGY = {
  washing_machine: 'cycle',
  dishwasher: 'cycle',
  dryer: 'cycle',
  oven: 'cycle',
  water_heater: 'cycle',
  coffee_maker: 'cycle',
  monitor: 'session',
  nas: 'session',
  printer_3d: 'session',
  vmc: 'session',
  generic: 'cycle'
};

// Appliance type icons
export const APPLIANCE_ICONS = {
  washing_machine: 'mdi:washing-machine',
  dishwasher: 'mdi:dishwasher',
  dryer: 'mdi:tumble-dryer',
  oven: 'mdi:stove',
  water_heater: 'mdi:water-boiler',
  coffee_maker: 'mdi:coffee-maker',
  monitor: 'mdi:monitor',
  nas: 'mdi:nas',
  printer_3d: 'mdi:printer-3d',
  vmc: 'mdi:fan',
  generic: 'mdi:power-plug'
};

// Card version
export const CARD_VERSION = '0.4.0';

// Default configuration
export const DEFAULT_CONFIG = {
  cycle_card: {
    show_power_graph: true,
    show_action_buttons: true,
    show_current_power: false,
    graph_hours: 0.5,
    theme: 'auto'
  },
  stats_card: {
    default_tab: 'today',
    show_trends: true,
    show_efficiency: true,
    chart_type: 'bar',
    theme: 'auto'
  }
};

// Time periods for statistics
export const TIME_PERIODS = {
  TODAY: 'today',
  WEEK: 'week',
  MONTH: 'month'
};

// Trend thresholds (percentage)
export const TREND_THRESHOLD = 10;

// Update intervals (milliseconds)
export const UPDATE_INTERVALS = {
  FAST: 1000,      // 1 second (for running state)
  NORMAL: 5000,    // 5 seconds (for idle/finished)
  SLOW: 30000      // 30 seconds (for statistics)
};
