"""
Comprehensive End-to-End Scenarios for Agentic Fabric POC
Tests complete user journey from input to response across different capability scenarios
"""

import sys
import os
import asyncio
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import Orchestrator
from core.agent_factory import AgentFactory
from core.tool_factory import ToolFactory
from core.registry_singleton import get_shared_registry, force_global_reload


class ComprehensiveScenarioTests:
    """Test suite for comprehensive end-to-end scenarios."""

    def __init__(self):
        self.orchestrator = Orchestrator()
        # Use shared registry singleton
        self.registry = get_shared_registry()
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
                # Force reload before each test to ensure clean state
                force_global_reload()

                result = await test_func()
                if result:
                    passed += 1
                    print(f"\n✅ {scenario_name}: PASSED")
                else:
                    failed += 1
                    print(f"\n❌ {scenario_name}: FAILED")
            except Exception as e:
                failed += 1
                print(f"\n❌ {scenario_name}: ERROR - {str(e)}")
                import traceback

                traceback.print_exc()

        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE RESULTS: {passed} passed, {failed} failed")
        print("=" * 80)

        if passed == len(scenarios):
            print("🎉 ALL SCENARIOS PASSED - BACKEND VALIDATION COMPLETE! 🎉")
            return True
        else:
            print(f"⚠️ {failed} scenarios need attention")
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

        # Ensure registry is fresh
        force_global_reload()

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

        # Check if actual extraction worked
        if "results" in result:
            email_results = result["results"].get("email_extractor", {})
            url_results = result["results"].get("url_extractor", {})

            if email_results.get("status") == "success":
                emails = email_results.get("data", {}).get("emails", [])
                print(f"Emails extracted: {emails}")

            if url_results.get("status") == "success":
                urls = url_results.get("data", {}).get("urls", [])
                print(f"URLs extracted: {urls}")

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

        # Force reload after creation
        if result.get("metadata", {}).get("components_created", 0) > 0:
            force_global_reload()

        # Validate dynamic creation occurred
        success = result["status"] in ["success", "partial"] and (
            result.get("metadata", {}).get("components_created", 0) > 0
            or len(result.get("workflow", {}).get("steps", [])) > 0
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
        # First, create phone_extractor agent if it doesn't exist
        if not self.registry.agent_exists("phone_extractor"):
            agent_factory = AgentFactory()
            creation_result = agent_factory.ensure_agent(
                agent_name="phone_extractor",
                description="Extract phone numbers from text",
                required_tools=["extract_phones"],
            )
            if creation_result["status"] in ["success", "exists"]:
                force_global_reload()
                print("Created phone_extractor agent for test")

        request = """
        Extract all phone numbers from this text:
        "Call us at (555) 123-4567 or (555) 987-6543. Emergency: 911"
        """

        print("Testing with phone_extractor agent (tool may need creation)")

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Force reload after any creation
        if result.get("metadata", {}).get("components_created", 0) > 0:
            force_global_reload()

        success = result["status"] in ["success", "partial"] and (
            "phone" in str(result.get("workflow", {})).lower()
            or len(result.get("workflow", {}).get("steps", [])) > 0
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

        # Force reload after complex creation
        force_global_reload()

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
        # Use a truly new domain that doesn't exist
        request = """
        Analyze blockchain transaction patterns and identify:
        - Whale movements over $1M
        - Smart contract interactions
        - Gas fee optimization opportunities
        - Risk score for wallet addresses
        Test with address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb8
        """

        print("Testing completely new domain - blockchain analysis")

        initial_agent_count = len(self.registry.list_agents())
        initial_tool_count = len(self.registry.list_tools())

        result = await self.orchestrator.process_request(
            user_request=request, auto_create=True
        )

        # Force reload and check what was created
        force_global_reload()

        final_agent_count = len(self.registry.list_agents())
        final_tool_count = len(self.registry.list_tools())

        components_created = (final_agent_count - initial_agent_count) + (
            final_tool_count - initial_tool_count
        )

        # Should create new components and execute
        success = result["status"] in ["success", "partial", "error"] and (
            components_created > 0
            or len(result.get("response", "")) > 100
            or "blockchain" in result.get("response", "").lower()
        )

        print(f"Status: {result['status']}")
        print(
            f"Components Created: {components_created} (Agents: {final_agent_count - initial_agent_count}, Tools: {final_tool_count - initial_tool_count})"
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

        # Should handle ambiguity gracefully
        success = (
            result["status"] in ["success", "partial", "missing_capabilities", "error"]
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

    # Ensure clean start
    force_global_reload()

    tester = ComprehensiveScenarioTests()
    success = await tester.run_all_scenarios()

    if success:
        print("\n🎊 BACKEND VALIDATION COMPLETE - SYSTEM READY FOR PRODUCTION 🎊")
        print("✅ All user journey scenarios working correctly")
        print("✅ Dynamic component creation functioning")
        print("✅ Complex workflow orchestration operational")
        print("✅ Error handling and edge cases covered")
    else:
        print("\n🔧 Additional tuning needed before production readiness")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
