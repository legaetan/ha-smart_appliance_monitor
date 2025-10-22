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
    CYCLE_ANALYSIS_STRUCTURE,
    ENERGY_DASHBOARD_ANALYSIS_STRUCTURE,
    AI_ANALYSIS_TYPE_PATTERN,
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
        self.language = hass.config.language

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
            # We expect a Markdown response, so we don't enforce a JSON structure
            response = await self._call_ai_task(
                task_name=f"Cycle Analysis - {appliance_name}",
                instructions=prompt,
                structure=CYCLE_ANALYSIS_STRUCTURE,
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
        structure: dict[str, Any] | None,
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
            
            service_data = {
                "entity_id": self.ai_task_entity,
                "task_name": task_name,
                "instructions": instructions,
            }
            if structure:
                service_data["structure"] = structure

            response = await self.hass.services.async_call(
                "ai_task",
                "generate_data",
                service_data,
                blocking=True,
                return_response=True,
            )
            
            _LOGGER.debug("AI Task raw response received: %s", response)
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
        """Build the prompt for cycle analysis based on type.
        
        Args:
            appliance_name: Name of the appliance
            appliance_type: Type of the appliance
            data: Export data
            analysis_type: Type of analysis (pattern, recommendations, all)
            
        Returns:
            Formatted prompt string
        """
        if analysis_type == AI_ANALYSIS_TYPE_PATTERN:
            return self._build_pattern_prompt(appliance_name, appliance_type, data)
        elif analysis_type == AI_ANALYSIS_TYPE_RECOMMENDATIONS:
            return self._build_recommendations_prompt(appliance_name, appliance_type, data)
        elif analysis_type == AI_ANALYSIS_TYPE_ALL:
            # Combine both prompts
            return self._build_combined_prompt(appliance_name, appliance_type, data)
        else:
            # Default to all
            return self._build_combined_prompt(appliance_name, appliance_type, data)
    
    def _build_pattern_prompt(
        self,
        appliance_name: str,
        appliance_type: str,
        data: dict[str, Any],
    ) -> str:
        """Build prompt for pattern analysis only.
        
        Args:
            appliance_name: Name of the appliance
            appliance_type: Type of the appliance
            data: Export data
            
        Returns:
            Formatted prompt string
        """
        currency = data.get("pricing_info", {}).get("currency", "EUR")
        
        prompt_parts = [
            f"Analyze USAGE PATTERNS for the appliance '{appliance_name}' ({appliance_type}).",
            f"The response MUST be in {self.language}.",
            "",
            "## Your Task - PATTERN ANALYSIS ONLY",
            "Focus exclusively on usage patterns:",
            "- Identify most frequent usage hours and days of the week",
            "- Detect usage patterns and trends over time",
            "- Evaluate potential for shifting usage to different time periods",
            "- Suggest optimal scheduling opportunities",
            "",
            f"Currency: {currency}",
            "",
            "## Data to Analyze",
            json.dumps(data, indent=2),
        ]
        
        # Add tariff context if peak/off-peak detected
        if data.get("pricing_info", {}).get("has_tariff_system"):
            prompt_parts.append("")
            prompt_parts.append(self._add_tariff_context(data))
        
        return "\n".join(prompt_parts)
    
    def _build_recommendations_prompt(
        self,
        appliance_name: str,
        appliance_type: str,
        data: dict[str, Any],
    ) -> str:
        """Build prompt for recommendations only.
        
        Args:
            appliance_name: Name of the appliance
            appliance_type: Type of the appliance
            data: Export data
            
        Returns:
            Formatted prompt string
        """
        currency = data.get("pricing_info", {}).get("currency", "EUR")
        
        prompt_parts = [
            f"Provide CONCRETE RECOMMENDATIONS to optimize the appliance '{appliance_name}' ({appliance_type}).",
            f"The response MUST be in {self.language}.",
            "",
            "## Your Task - RECOMMENDATIONS ONLY",
            "Provide actionable recommendations:",
            "1. When to use the appliance (optimal timing based on patterns)",
            "2. How to reduce energy consumption (settings, eco modes, maintenance)",
            "3. Optimal usage frequency and best practices",
            "",
            f"Appliance type: {appliance_type}",
            f"Currency: {currency}",
            "",
            "## Data to Analyze",
            json.dumps(data, indent=2),
        ]
        
        # Add tariff-specific recommendations if applicable
        if data.get("pricing_info", {}).get("has_tariff_system"):
            prompt_parts.append("")
            prompt_parts.append("IMPORTANT: Prioritize timing recommendations based on peak/off-peak tariff structure.")
            prompt_parts.append(self._add_tariff_context(data))
        
        return "\n".join(prompt_parts)
    
    def _build_combined_prompt(
        self,
        appliance_name: str,
        appliance_type: str,
        data: dict[str, Any],
    ) -> str:
        """Build combined prompt for complete analysis.
        
        Args:
            appliance_name: Name of the appliance
            appliance_type: Type of the appliance
            data: Export data
            
        Returns:
            Formatted prompt string
        """
        currency = data.get("pricing_info", {}).get("currency", "EUR")
        
        prompt_parts = [
            f"Analyze the energy data for the appliance '{appliance_name}' ({appliance_type}).",
            "Provide a concise, structured report with BOTH pattern analysis AND recommendations.",
            f"The response MUST be in {self.language}.",
            "",
            "## Your Task",
            "1. PATTERN ANALYSIS:",
            "   - Identify most frequent usage hours and days",
            "   - Detect usage patterns and trends",
            "   - Evaluate potential for shifting usage",
            "",
            "2. RECOMMENDATIONS:",
            "   - When to use the appliance (optimal timing)",
            "   - How to reduce consumption (settings, eco modes)",
            "   - Optimal usage frequency and best practices",
            "",
            f"Appliance type: {appliance_type}",
            f"Currency: {currency}",
            "",
            "## Data to Analyze",
            json.dumps(data, indent=2),
        ]
        
        # Add tariff context if applicable
        if data.get("pricing_info", {}).get("has_tariff_system"):
            prompt_parts.append("")
            prompt_parts.append(self._add_tariff_context(data))
        
        return "\n".join(prompt_parts)
    
    def _add_tariff_context(self, data: dict[str, Any]) -> str:
        """Add tariff system context to the prompt.
        
        Args:
            data: Export data with pricing_info
            
        Returns:
            Formatted tariff context string
        """
        pricing = data.get("pricing_info", {})
        currency = pricing.get("currency", "EUR")
        peak_price = pricing.get("peak_price", 0)
        offpeak_price = pricing.get("offpeak_price", 0)
        peak_hours = pricing.get("peak_hours", "Unknown")
        savings_potential = pricing.get("estimated_savings_potential", 0)
        
        return f"""## Tariff System Information
Peak/Off-peak electricity tariff detected:
- Peak rate: {peak_price:.4f} {currency}/kWh (hours: {peak_hours})
- Off-peak rate: {offpeak_price:.4f} {currency}/kWh
- Estimated savings potential: {savings_potential:.1f}% by shifting to off-peak

CALCULATE potential cost savings by shifting usage to off-peak hours in your analysis."""

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
            "Analyze the following household energy data.",
            f"Provide a concise analysis in {self.language}.",
            "",
            "## Energy Data",
            json.dumps(dashboard_data, indent=2),
            "",
            "## Your Task",
            "1. Assess overall energy efficiency.",
            "2. Identify top energy consumers.",
            "3. Provide actionable recommendations to save energy.",
            "",
            "## Output Requirements (be brief)",
            "- **efficiency_score**: 0-100",
            "- **global_recommendations**: Top recommendations for the home (bullet points).",
            "- **top_optimization_opportunities**: Top 3 opportunities.",
            "- **estimated_monthly_savings_eur**: A single number.",
            "- **peak_hours**: Time range.",
            "- **off_peak_recommendations**: Brief suggestions.",
            "- **inefficient_devices**: List of devices.",
            "- **consumption_trend**: 'increasing', 'stable', or 'decreasing'.",
        ]
        
        return "\n".join(prompt_parts)

    def _process_cycle_analysis_response(self, response: ServiceResponse) -> dict[str, Any]:
        """Process and validate cycle analysis response from structured data.
        
        Args:
            response: Raw AI Task response (containing structured data)
            
        Returns:
            Processed and validated response as a dictionary
        """
        if not isinstance(response, dict):
            _LOGGER.warning("AI Task response is not a dictionary: %s", response)
            return {}

        # Extract the "data" key from the AI Task response
        data = response.get("data", {})
        _LOGGER.debug("Raw AI structured response to be processed: %s", data)
        
        # Helper to safely convert to float, handling None values
        def safe_float(value, default=0.0):
            if value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        result = {
            "summary": data.get("summary", ""),
            "status": data.get("status", "normal"),
            "recommendations": self._parse_recommendations(data.get("recommendations", "")),
            "energy_savings_kwh": safe_float(data.get("energy_savings_kwh"), 0.0),
            "energy_savings_eur": safe_float(data.get("energy_savings_eur"), 0.0),
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
            data: Structured analysis data (with recommendations already parsed as list)
            
        Returns:
            Formatted full analysis text in Markdown
        """
        parts = []
        
        if summary := data.get("summary"):
            parts.append(f"**Résumé:** {summary}")
        
        if recommendations := data.get("recommendations"):
            # Recommendations are already a list
            if isinstance(recommendations, list) and recommendations:
                parts.append("\n**Recommandations:**")
                for rec in recommendations:
                    parts.append(f"- {rec}")
            elif isinstance(recommendations, str):
                # If it's still a string, parse it
                recs = self._parse_recommendations(recommendations)
                if recs:
                    parts.append("\n**Recommandations:**")
                    for rec in recs:
                        parts.append(f"- {rec}")
        
        if insights := data.get("insights"):
            parts.append(f"\n**Insights:**\n{insights}")
        
        if optimal_hours := data.get("optimal_hours"):
            parts.append(f"\n**Heures Optimales:** {optimal_hours}")
        
        savings_kwh = data.get("energy_savings_kwh") or 0
        savings_eur = data.get("energy_savings_eur") or 0
        if savings_kwh > 0 or savings_eur > 0:
            parts.append(f"\n**Économies Potentielles:** {savings_kwh} kWh / {savings_eur} EUR")
        
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

