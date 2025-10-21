"""AI client for Smart Appliance Monitor using Home Assistant AI Tasks.

This module provides AI analysis capabilities using the ai_task.generate_data service.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant, ServiceResponse
from homeassistant.exceptions import HomeAssistantError

from .const import (
    ANALYSIS_STRUCTURE,
    ENERGY_DASHBOARD_ANALYSIS_STRUCTURE,
    AI_ANALYSIS_TYPE_PATTERN,
    AI_ANALYSIS_TYPE_COMPARATIVE,
    AI_ANALYSIS_TYPE_RECOMMENDATIONS,
    AI_ANALYSIS_TYPE_ALL,
)

_LOGGER = logging.getLogger(__name__)


class SmartApplianceAIClient:
    """AI client for analyzing appliance cycles and energy consumption."""

    def __init__(self, hass: HomeAssistant, ai_task_entity: str) -> None:
        """Initialize the AI client.
        
        Args:
            hass: Home Assistant instance
            ai_task_entity: Entity ID of the AI Task to use
        """
        self.hass = hass
        self.ai_task_entity = ai_task_entity

    async def async_analyze_cycle_data(
        self,
        appliance_name: str,
        appliance_type: str,
        data: dict[str, Any],
        analysis_type: str = AI_ANALYSIS_TYPE_ALL,
    ) -> dict[str, Any]:
        """Analyze cycle data using AI.
        
        Args:
            appliance_name: Name of the appliance
            appliance_type: Type of the appliance
            data: Export data from the appliance
            analysis_type: Type of analysis to perform
            
        Returns:
            AI analysis results
            
        Raises:
            HomeAssistantError: If AI analysis fails
        """
        _LOGGER.debug("Starting AI analysis for %s (%s)", appliance_name, analysis_type)
        
        # Build the prompt
        prompt = self._build_cycle_analysis_prompt(
            appliance_name, appliance_type, data, analysis_type
        )
        
        # Call the AI Task
        try:
            response = await self._call_ai_task(
                task_name=f"Cycle Analysis - {appliance_name}",
                instructions=prompt,
                structure=ANALYSIS_STRUCTURE,
            )
            
            # Process and validate response
            result = self._process_cycle_analysis_response(response)
            result["analysis_type"] = analysis_type
            result["appliance_name"] = appliance_name
            result["appliance_type"] = appliance_type
            result["timestamp"] = datetime.now().isoformat()
            
            _LOGGER.info("AI analysis completed for %s", appliance_name)
            return result
            
        except Exception as err:
            _LOGGER.error("AI analysis failed for %s: %s", appliance_name, err)
            raise HomeAssistantError(f"AI analysis failed: {err}") from err

    async def async_analyze_energy_dashboard(
        self,
        dashboard_data: dict[str, Any],
        period: str = "today",
        compare_previous: bool = False,
    ) -> dict[str, Any]:
        """Analyze energy dashboard data using AI.
        
        Args:
            dashboard_data: Aggregated energy data from dashboard
            period: Analysis period (today/yesterday/week/month)
            compare_previous: Whether to include comparison with previous period
            
        Returns:
            AI analysis results for energy dashboard
            
        Raises:
            HomeAssistantError: If AI analysis fails
        """
        _LOGGER.debug("Starting Energy Dashboard AI analysis for period: %s", period)
        
        # Build the prompt for energy dashboard analysis
        prompt = self._build_energy_dashboard_prompt(
            dashboard_data, period, compare_previous
        )
        
        # Call the AI Task
        try:
            response = await self._call_ai_task(
                task_name=f"Energy Dashboard Analysis - {period}",
                instructions=prompt,
                structure=ENERGY_DASHBOARD_ANALYSIS_STRUCTURE,
            )
            
            # Process and validate response
            result = self._process_energy_dashboard_response(response)
            result["analysis_period"] = period
            result["comparison_included"] = compare_previous
            result["timestamp"] = datetime.now().isoformat()
            
            _LOGGER.info("Energy Dashboard AI analysis completed for period: %s", period)
            return result
            
        except Exception as err:
            _LOGGER.error("Energy Dashboard AI analysis failed: %s", err)
            raise HomeAssistantError(f"Energy Dashboard AI analysis failed: {err}") from err

    async def _call_ai_task(
        self,
        task_name: str,
        instructions: str,
        structure: dict[str, Any],
    ) -> ServiceResponse:
        """Call the AI Task service.
        
        Args:
            task_name: Name of the task
            instructions: Instructions/prompt for the AI
            structure: Expected response structure
            
        Returns:
            AI Task response
            
        Raises:
            HomeAssistantError: If service call fails
        """
        try:
            _LOGGER.debug("Calling ai_task.generate_data with entity: %s", self.ai_task_entity)
            
            response = await self.hass.services.async_call(
                "ai_task",
                "generate_data",
                {
                    "entity_id": self.ai_task_entity,
                    "task_name": task_name,
                    "instructions": instructions,
                    "structure": structure,
                },
                blocking=True,
                return_response=True,
            )
            
            _LOGGER.debug("AI Task response received")
            return response
            
        except Exception as err:
            _LOGGER.error("AI Task service call failed: %s", err)
            raise HomeAssistantError(f"AI Task service call failed: {err}") from err

    def _build_cycle_analysis_prompt(
        self,
        appliance_name: str,
        appliance_type: str,
        data: dict[str, Any],
        analysis_type: str,
    ) -> str:
        """Build the prompt for cycle analysis.
        
        Args:
            appliance_name: Name of the appliance
            appliance_type: Type of the appliance
            data: Export data
            analysis_type: Type of analysis
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            f"You are an energy efficiency expert analyzing a {appliance_type} named '{appliance_name}'.",
            "",
            "## Context",
            f"Appliance Type: {appliance_type}",
            f"Analysis Type: {analysis_type}",
            "",
            "## Data",
            json.dumps(data, indent=2),
            "",
            "## Your Task",
        ]
        
        if analysis_type == AI_ANALYSIS_TYPE_PATTERN or analysis_type == AI_ANALYSIS_TYPE_ALL:
            prompt_parts.extend([
                "1. **Pattern Analysis**: Identify usage patterns, recurring schedules, and habits.",
                "   - What are the typical usage hours?",
                "   - Are there recurring patterns (daily/weekly)?",
                "   - Is the appliance used efficiently?",
                "",
            ])
        
        if analysis_type == AI_ANALYSIS_TYPE_COMPARATIVE or analysis_type == AI_ANALYSIS_TYPE_ALL:
            prompt_parts.extend([
                "2. **Comparative Analysis**: Compare current performance with historical data.",
                "   - How does current consumption compare to averages?",
                "   - Are there any unusual patterns or anomalies?",
                "   - Is consumption trending up or down?",
                "",
            ])
        
        if analysis_type == AI_ANALYSIS_TYPE_RECOMMENDATIONS or analysis_type == AI_ANALYSIS_TYPE_ALL:
            prompt_parts.extend([
                "3. **Recommendations**: Provide actionable advice for optimization.",
                "   - How can the user reduce energy consumption?",
                "   - What are the best usage hours for cost savings?",
                "   - Any maintenance or efficiency tips?",
                "",
            ])
        
        prompt_parts.extend([
            "## Output Requirements",
            "- **summary**: 2-3 sentence overview of findings",
            "- **status**: 'optimized', 'normal', or 'needs_improvement'",
            "- **recommendations**: Clear, actionable recommendations (one per line)",
            "- **energy_savings_kwh**: Estimated potential savings in kWh (if applicable)",
            "- **energy_savings_eur**: Estimated potential cost savings in EUR (if applicable)",
            "- **optimal_hours**: Recommended usage hours (e.g., '22:00-06:00 for off-peak rates')",
            "- **insights**: Key insights from the analysis",
            "",
            "Be specific, practical, and focus on actionable insights.",
        ])
        
        return "\n".join(prompt_parts)

    def _build_energy_dashboard_prompt(
        self,
        dashboard_data: dict[str, Any],
        period: str,
        compare_previous: bool,
    ) -> str:
        """Build the prompt for energy dashboard analysis.
        
        Args:
            dashboard_data: Aggregated energy data
            period: Analysis period
            compare_previous: Include comparison
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "You are a home energy efficiency consultant analyzing overall household energy consumption.",
            "",
            "## Context",
            f"Analysis Period: {period}",
            f"Comparison with Previous Period: {'Yes' if compare_previous else 'No'}",
            "",
            "## Energy Data",
            json.dumps(dashboard_data, indent=2),
            "",
            "## Your Task",
            "",
            "Analyze the entire home's energy consumption and provide:",
            "",
            "1. **Global Assessment**: Overall energy efficiency of the home",
            "2. **Top Consumers**: Identify which appliances use the most energy",
            "3. **Optimization Opportunities**: Where can savings be made?",
            "4. **Usage Patterns**: Peak hours, inefficient times, trends",
            "5. **Actionable Recommendations**: Specific steps to reduce consumption",
            "",
        ]
        
        if compare_previous:
            prompt_parts.extend([
                "6. **Trend Analysis**: Compare with previous period and explain changes",
                "",
            ])
        
        prompt_parts.extend([
            "## Output Requirements",
            "- **efficiency_score**: 0-100 score for overall home energy efficiency",
            "- **global_recommendations**: Top recommendations for the entire home (one per line)",
            "- **top_optimization_opportunities**: Top 3 specific opportunities with highest impact",
            "- **estimated_monthly_savings_eur**: Realistic estimate of monthly savings if recommendations followed",
            "- **peak_hours**: When does the home use most energy?",
            "- **off_peak_recommendations**: Which appliances should be moved to off-peak hours?",
            "- **inefficient_devices**: Which devices are using more energy than expected?",
            "- **consumption_trend**: 'increasing', 'stable', or 'decreasing'",
            "",
            "Focus on practical, household-level advice that can make a real difference.",
        ])
        
        return "\n".join(prompt_parts)

    def _process_cycle_analysis_response(self, response: ServiceResponse) -> dict[str, Any]:
        """Process and validate cycle analysis response.
        
        Args:
            response: Raw AI Task response
            
        Returns:
            Processed and validated response
        """
        # Extract response data
        if isinstance(response, dict):
            data = response
        else:
            data = {}
        
        # Ensure required fields are present
        result = {
            "summary": data.get("summary", "Analysis completed"),
            "status": data.get("status", "normal"),
            "recommendations": self._parse_recommendations(data.get("recommendations", "")),
            "energy_savings_kwh": float(data.get("energy_savings_kwh", 0)),
            "energy_savings_eur": float(data.get("energy_savings_eur", 0)),
            "optimal_hours": data.get("optimal_hours", ""),
            "insights": data.get("insights", ""),
            "full_analysis": self._build_full_analysis_text(data),
        }
        
        return result

    def _process_energy_dashboard_response(self, response: ServiceResponse) -> dict[str, Any]:
        """Process and validate energy dashboard response.
        
        Args:
            response: Raw AI Task response
            
        Returns:
            Processed and validated response
        """
        # Extract response data
        if isinstance(response, dict):
            data = response
        else:
            data = {}
        
        # Ensure required fields are present
        result = {
            "efficiency_score": int(data.get("efficiency_score", 50)),
            "global_recommendations": self._parse_recommendations(
                data.get("global_recommendations", "")
            ),
            "top_optimization_opportunities": self._parse_recommendations(
                data.get("top_optimization_opportunities", "")
            ),
            "estimated_monthly_savings_eur": float(
                data.get("estimated_monthly_savings_eur", 0)
            ),
            "peak_hours": data.get("peak_hours", ""),
            "off_peak_recommendations": data.get("off_peak_recommendations", ""),
            "inefficient_devices": self._parse_recommendations(
                data.get("inefficient_devices", "")
            ),
            "consumption_trend": data.get("consumption_trend", "stable"),
            "full_analysis": self._build_full_dashboard_analysis_text(data),
        }
        
        return result

    def _parse_recommendations(self, recommendations_text: str) -> list[str]:
        """Parse recommendations from text to list.
        
        Args:
            recommendations_text: Text with recommendations (one per line)
            
        Returns:
            List of recommendations
        """
        if not recommendations_text:
            return []
        
        # Split by newlines and clean up
        lines = [
            line.strip()
            for line in recommendations_text.split("\n")
            if line.strip()
        ]
        
        # Remove common list markers (-, *, •, numbers)
        cleaned = []
        for line in lines:
            # Remove leading markers
            line = line.lstrip("-*•").strip()
            # Remove leading numbers with dots
            if line and line[0].isdigit():
                parts = line.split(".", 1)
                if len(parts) > 1:
                    line = parts[1].strip()
            
            if line:
                cleaned.append(line)
        
        return cleaned

    def _build_full_analysis_text(self, data: dict[str, Any]) -> str:
        """Build full analysis text from structured data.
        
        Args:
            data: Structured analysis data
            
        Returns:
            Formatted full analysis text
        """
        parts = []
        
        if data.get("summary"):
            parts.append(f"Summary: {data['summary']}")
        
        if data.get("insights"):
            parts.append(f"\nInsights:\n{data['insights']}")
        
        if data.get("recommendations"):
            recs = self._parse_recommendations(data["recommendations"])
            if recs:
                parts.append("\nRecommendations:")
                for i, rec in enumerate(recs, 1):
                    parts.append(f"{i}. {rec}")
        
        if data.get("optimal_hours"):
            parts.append(f"\nOptimal Usage Hours: {data['optimal_hours']}")
        
        return "\n".join(parts) if parts else "Analysis completed"

    def _build_full_dashboard_analysis_text(self, data: dict[str, Any]) -> str:
        """Build full dashboard analysis text from structured data.
        
        Args:
            data: Structured dashboard analysis data
            
        Returns:
            Formatted full analysis text
        """
        parts = []
        
        parts.append(f"Efficiency Score: {data.get('efficiency_score', 50)}/100")
        
        if data.get("consumption_trend"):
            parts.append(f"Trend: {data['consumption_trend']}")
        
        if data.get("global_recommendations"):
            recs = self._parse_recommendations(data["global_recommendations"])
            if recs:
                parts.append("\nGlobal Recommendations:")
                for i, rec in enumerate(recs, 1):
                    parts.append(f"{i}. {rec}")
        
        if data.get("top_optimization_opportunities"):
            opps = self._parse_recommendations(data["top_optimization_opportunities"])
            if opps:
                parts.append("\nTop Optimization Opportunities:")
                for i, opp in enumerate(opps, 1):
                    parts.append(f"{i}. {opp}")
        
        if data.get("peak_hours"):
            parts.append(f"\nPeak Hours: {data['peak_hours']}")
        
        if data.get("off_peak_recommendations"):
            parts.append(f"\nOff-Peak Recommendations:\n{data['off_peak_recommendations']}")
        
        return "\n".join(parts) if parts else "Dashboard analysis completed"

