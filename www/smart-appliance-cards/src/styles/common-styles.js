/**
 * Common styles for Smart Appliance Cards
 */

import { css } from 'lit';

export const commonStyles = css`
  :host {
    --sac-primary-color: var(--primary-color, #03a9f4);
    --sac-text-primary: var(--primary-text-color, #212121);
    --sac-text-secondary: var(--secondary-text-color, #727272);
    --sac-card-background: var(--card-background-color, #fff);
    --sac-divider-color: var(--divider-color, rgba(0, 0, 0, 0.12));
    --sac-border-radius: var(--ha-card-border-radius, 12px);
    --sac-spacing: 16px;
    --sac-spacing-sm: 8px;
    --sac-spacing-lg: 24px;
    
    /* State colors */
    --sac-state-idle: var(--state-inactive-color, #9e9e9e);
    --sac-state-running: var(--state-active-color, #4caf50);
    --sac-state-finished: var(--state-finished-color, #2196f3);
    --sac-state-alert: var(--warning-color, #ff9800);
    --sac-state-error: var(--error-color, #f44336);
    
    /* Shadows */
    --sac-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
    --sac-shadow-md: 0 2px 8px rgba(0, 0, 0, 0.15);
    --sac-shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.2);
    
    /* Transitions */
    --sac-transition-fast: 150ms ease-out;
    --sac-transition-normal: 300ms ease-out;
    --sac-transition-slow: 500ms ease-out;
  }
  
  /* Card container */
  .card {
    background: var(--sac-card-background);
    border-radius: var(--sac-border-radius);
    padding: var(--sac-spacing);
    box-shadow: var(--sac-shadow-sm);
    position: relative;
    overflow: hidden;
  }
  
  /* Card header */
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--sac-spacing);
  }
  
  .card-title {
    font-size: 20px;
    font-weight: 500;
    color: var(--sac-text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
  }
  
  /* Icon styles */
  ha-icon {
    color: var(--sac-text-secondary);
  }
  
  .icon-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: var(--sac-spacing-sm);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color var(--sac-transition-fast);
  }
  
  .icon-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  .icon-button:active {
    background-color: rgba(0, 0, 0, 0.1);
  }
  
  /* Status indicators */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 14px;
    font-weight: 500;
    text-transform: capitalize;
  }
  
  .status-badge.idle {
    background-color: rgba(158, 158, 158, 0.1);
    color: var(--sac-state-idle);
  }
  
  .status-badge.running {
    background-color: rgba(76, 175, 80, 0.1);
    color: var(--sac-state-running);
  }
  
  .status-badge.finished {
    background-color: rgba(33, 150, 243, 0.1);
    color: var(--sac-state-finished);
  }
  
  /* Value displays */
  .value-container {
    display: flex;
    flex-direction: column;
    gap: var(--sac-spacing-sm);
  }
  
  .value-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--sac-spacing-sm) 0;
  }
  
  .value-label {
    font-size: 14px;
    color: var(--sac-text-secondary);
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
  }
  
  .value-text {
    font-size: 16px;
    font-weight: 500;
    color: var(--sac-text-primary);
  }
  
  .value-large {
    font-size: 24px;
    font-weight: 600;
  }
  
  /* Divider */
  .divider {
    height: 1px;
    background-color: var(--sac-divider-color);
    margin: var(--sac-spacing) 0;
  }
  
  /* Buttons */
  .button {
    background: var(--sac-primary-color);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--sac-transition-fast);
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
  }
  
  .button:hover {
    opacity: 0.9;
    box-shadow: var(--sac-shadow-md);
  }
  
  .button:active {
    transform: scale(0.98);
  }
  
  .button-secondary {
    background: transparent;
    color: var(--sac-primary-color);
    border: 1px solid var(--sac-primary-color);
  }
  
  .button-danger {
    background: var(--sac-state-error);
  }
  
  .button-group {
    display: flex;
    gap: var(--sac-spacing-sm);
    flex-wrap: wrap;
  }
  
  /* Alert/Warning states */
  .alert-container {
    padding: var(--sac-spacing-sm);
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: var(--sac-spacing-sm);
    margin-bottom: var(--sac-spacing);
  }
  
  .alert-warning {
    background-color: rgba(255, 152, 0, 0.1);
    border-left: 4px solid var(--sac-state-alert);
  }
  
  .alert-error {
    background-color: rgba(244, 67, 54, 0.1);
    border-left: 4px solid var(--sac-state-error);
  }
  
  .alert-info {
    background-color: rgba(33, 150, 243, 0.1);
    border-left: 4px solid var(--sac-state-finished);
  }
  
  /* Loading state */
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--sac-spacing-lg);
    color: var(--sac-text-secondary);
  }
  
  /* Animations */
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .pulse {
    animation: pulse 2s ease-in-out infinite;
  }
  
  .rotate {
    animation: rotate 2s linear infinite;
  }
  
  .fade-in {
    animation: fadeIn var(--sac-transition-normal) ease-out;
  }
  
  /* Grid layouts */
  .grid {
    display: grid;
    gap: var(--sac-spacing);
  }
  
  .grid-2 {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .grid-3 {
    grid-template-columns: repeat(3, 1fr);
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .card {
      padding: var(--sac-spacing-sm);
    }
    
    .card-title {
      font-size: 18px;
    }
    
    .value-large {
      font-size: 20px;
    }
    
    .grid-2,
    .grid-3 {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 480px) {
    :host {
      --sac-spacing: 12px;
      --sac-spacing-sm: 6px;
    }
    
    .button-group {
      flex-direction: column;
    }
    
    .button {
      width: 100%;
      justify-content: center;
    }
  }
`;
