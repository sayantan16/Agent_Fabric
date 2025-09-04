"""
Comprehensive End-to-End Scenarios for Agentic Fabric POC
Tests complete user journey from input to response across different capability scenarios
"""

import sys
import os
import asyncio
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.registry import RegistryManager
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory


class ComprehensiveScenarioTests:
    """Test suite for comprehensive end-to-end scenarios."""

    def __init__(self):
        self.orchestrator = Orchestrator()
        self.registry = RegistryManager()
        self.test_results = []

    async def run_all_scenarios(self):
        """Run all comprehensive test scenarios."""
        print("\n" + "=" * 80)
        print("AGENTIC FABRIC POC - COMPREHENSIVE END-TO-END SCENARIOS")
        print("=" * 80)

        scenarios = [
            ("All Components Present", self.test_all_components_present),
            ("Missing Agents, Tools Present", self.test_missing_agents_present_tools),
            ("Present Agents, Missing Tools", self.test_present_agents_missing_tools),
            ("Complex Mixed Dependencies", self.test_complex_mixed_dependencies),
            ("Completely New Domain", self.test_completely_new_domain),
            ("Ambiguous Multi-Path Request", self.test_ambiguous_request),
        ]

        passed = 0
        failed = 0

        for scenario_name, test_func in scenarios:
            print(f"\n{'='*60}")
            print(f"SCENARIO: {scenario_name}")
            print("=" * 60)

            try:
                result = await test_func()
                if result:
                    passed += 1
                    print(f"\n{scenario_name}: PASSED")
                else:
                    failed += 1
                    print(f"\n{scenario_name}: FAILED")
            except Exception as e:
                failed += 1
                print(f"\n{scenario_name}: ERROR - {str(e)}")
                import traceback

                traceback.print_exc()

        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE RESULTS: {passed} passed, {failed} failed")
        print("=" * 80)

        if passed == 6:
            print("🎉 ALL SCENARIOS PASSED - BACKEND VALIDATION COMPLETE! 🎉")
            return True
        else:
            print(f"{failed} scenarios need attention")
            return False

    async def test_all_components_present(self):
        """
        SCENARIO 1: All Components Present
        Request that uses only existing agents and tools
        Expected: Smooth execution without any dynamic creation
        """
        request = """
        Analyze this text and extract both email addresses and URLs:
        "Contact us at support@company.com or sales@business.org. 
        Visit our sites at https://company.com and https://docs.business.org"
        """

        print("Testing with existing agents: email_extractor, url_extractor")

        result = await self.orchestrator.process_request(
            user_request=request,
            auto_create=False,  # Should not need to create anything
        )

        # Validate results
        success = (
            result["status"] == "success"
            and len(result.get("workflow", {}).get("steps", [])) >= 1
            and result.get("metadata", {}).get("components_created", 0)
            == 0  # No new components
        )

        print(f"Status: {result['status']}")
        print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")
        print(
            f"Components Created: {result.get('metadata', {}).get('components_created', 'N/A')}"
        )
        print(f"Response Length: {len(result.get('response', ''))}")

        return success

    async def test_missing_agents_present_tools(self):
        """
        SCENARIO 2: Missing Agents, Tools Present
        Request that needs new agents but tools exist
        Expected: Dynamic agent creation, tool reuse
        """
        request = """
        Create a statistical report from these numbers: [10, 20, 30, 40, 50, 25, 35, 45]
        Calculate mean, median, and standard deviation, then format as a professional report.
        """

        print("Testing agent creation with existing calculate_mean tool")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Validate dynamic creation occurred
        success = (
            result["status"] in ["success", "partial"]
            and result.get("metadata", {}).get("components_created", 0) > 0
        )

        print(f"Status: {result['status']}")
        print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")
        print(
            f"Components Created: {result.get('metadata', {}).get('components_created', 'N/A')}"
        )

        return success

    async def test_present_agents_missing_tools(self):
        """
        SCENARIO 3: Present Agents, Missing Tools
        Request that existing agents can handle but need new tools
        Expected: Dynamic tool creation, agent reuse
        """
        request = """
        Extract all phone numbers from this text using the text_analyzer:
        "Call us at (555) 123-4567 or (555) 987-6543. Emergency: 911"
        """

        print("Testing tool creation for text_analyzer agent")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Should use existing text_analyzer but may create phone extraction tool
        success = result["status"] in ["success", "partial"] and "text_analyzer" in str(
            result.get("workflow", {})
        )

        print(f"Status: {result['status']}")
        print(f"Workflow: {result.get('workflow', {}).get('steps', [])}")

        return success

    async def test_complex_mixed_dependencies(self):
        """
        SCENARIO 4: Complex Mixed Dependencies
        Multi-step request with some agents present, some missing, complex tool chain
        Expected: Intelligent dependency resolution and creation
        """
        request = """
        Process this data pipeline:
        1. Read data from a CSV file (simulated data)
        2. Clean and validate the data  
        3. Calculate summary statistics
        4. Generate a bar chart visualization
        5. Create a formatted report with insights
        """

        print("Testing complex multi-agent pipeline with mixed dependencies")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Complex workflow should be planned and executed
        success = (
            result["status"] in ["success", "partial"]
            and len(result.get("workflow", {}).get("steps", []))
            >= 3  # Multi-step workflow
        )

        print(f"Status: {result['status']}")
        print(f"Workflow Steps: {len(result.get('workflow', {}).get('steps', []))}")
        print(f"Execution Time: {result.get('execution_time', 'N/A')}s")

        return success

    async def test_completely_new_domain(self):
        """
        SCENARIO 5: Completely New Domain
        Request for entirely new capability not covered by existing system
        Expected: Full agent+tool chain creation from scratch
        """
        request = """
        Create a password strength analyzer that:
        - Checks password length, complexity, and common patterns
        - Generates a security score from 1-100
        - Provides specific recommendations for improvement
        - Tests this password: "MyP@ssw0rd123"
        """

        print("Testing completely new domain - password analysis")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Should create new components and execute successfully
        success = (
            result["status"] in ["success", "partial"]
            and result.get("metadata", {}).get("components_created", 0) > 0
            and len(result.get("response", "")) > 100  # Substantial response
        )

        print(f"Status: {result['status']}")
        print(
            f"Components Created: {result.get('metadata', {}).get('components_created', 'N/A')}"
        )
        print(
            f"Response Quality: {'High' if len(result.get('response', '')) > 200 else 'Low'}"
        )

        return success

    async def test_ambiguous_request(self):
        """
        SCENARIO 6: Ambiguous Multi-Path Request
        Request that could be interpreted multiple ways, testing orchestrator intelligence
        Expected: Intelligent disambiguation and optimal agent selection
        """
        request = """
        "Analyze this customer feedback data"
        [No specific data provided, ambiguous request]
        """

        print("Testing ambiguous request handling and clarification")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Should handle ambiguity gracefully, either by asking for clarification or making reasonable assumptions
        success = (
            result["status"] in ["success", "partial", "missing_capabilities"]
            and len(result.get("response", "")) > 50  # Some meaningful response
        )

        print(f"Status: {result['status']}")
        print(
            f"Response Handling: {'Clarification' if 'clarify' in result.get('response', '').lower() else 'Assumption'}"
        )

        return success


async def main():
    """Run comprehensive scenarios."""
    print("Starting Comprehensive End-to-End Scenario Testing")
    print("Goal: Validate complete user journey from input to response")

    tester = ComprehensiveScenarioTests()
    success = await tester.run_all_scenarios()

    if success:
        print("\nBACKEND VALIDATION COMPLETE - SYSTEM READY FOR PRODUCTION 🎊")
        print("All user journey scenarios working correctly")
        print("Dynamic component creation functioning")
        print("Complex workflow orchestration operational")
        print("Error handling and edge cases covered")
    else:
        print("\n🔧 Additional tuning needed before production readiness")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
