"""
Multi-Agent Data Flow Test: CSV Analysis to PDF Summary
File: test_data_flow_workflow.py

This test validates that data flows correctly between agents in a multi-step workflow.
Workflow: CSV Data Analysis → Statistical Summary → PDF Report Generation
"""

import asyncio
import csv
import os
import sys
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.simplified_orchestrator import SimplifiedOrchestrator
from core.registry_singleton import get_shared_registry


def create_sample_sales_csv():
    """Create a sample sales CSV file for testing"""

    filename = "test_sales_data.csv"

    # Generate realistic sales data
    products = ["Widget A", "Widget B", "Gadget Pro", "Super Tool", "Premium Kit"]
    regions = ["North", "South", "East", "West", "Central"]
    sales_reps = [
        "Alice Johnson",
        "Bob Smith",
        "Carol Davis",
        "David Wilson",
        "Eva Brown",
    ]

    data = []
    start_date = datetime(2024, 1, 1)

    for i in range(150):  # Generate 150 sales records
        record = {
            "Date": (start_date + timedelta(days=random.randint(0, 365))).strftime(
                "%Y-%m-%d"
            ),
            "Product": random.choice(products),
            "Region": random.choice(regions),
            "Sales_Rep": random.choice(sales_reps),
            "Units_Sold": random.randint(1, 50),
            "Unit_Price": round(random.uniform(25.0, 500.0), 2),
            "Customer_Type": random.choice(["Enterprise", "SMB", "Individual"]),
            "Discount_Applied": round(random.uniform(0, 0.25), 2),
        }
        record["Total_Revenue"] = round(
            record["Units_Sold"]
            * record["Unit_Price"]
            * (1 - record["Discount_Applied"]),
            2,
        )
        data.append(record)

    # Write CSV file
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "Date",
            "Product",
            "Region",
            "Sales_Rep",
            "Units_Sold",
            "Unit_Price",
            "Customer_Type",
            "Discount_Applied",
            "Total_Revenue",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Created sample sales data: {filename}")
    print(f"Records: {len(data)}")
    print(f"Sample record: {data[0]}")
    return filename


async def test_multi_agent_data_flow():
    """Test complete data flow: CSV → Analysis → PDF Summary"""

    print("MULTI-AGENT DATA FLOW TEST")
    print("=" * 60)
    print("Workflow: CSV Analysis → Statistical Summary → PDF Report")
    print()

    # Step 1: Create test data
    csv_file = create_sample_sales_csv()

    # Step 2: Initialize orchestrator
    orchestrator = SimplifiedOrchestrator()

    # Step 3: Check available agents
    registry = get_shared_registry()
    available_agents = list(registry.agents.get("agents", {}).keys())
    print(f"Available agents: {available_agents}")
    print()

    # Step 4: Execute multi-agent workflow
    request = """Analyze this sales data CSV file and create a comprehensive summary PDF report. 
    
    The report should include:
    1. Total sales figures and trends
    2. Performance by region and product
    3. Top performing sales representatives
    4. Customer type analysis
    5. Revenue insights and patterns
    
    Please process the data thoroughly and generate a professional PDF summary."""

    files = [{"path": csv_file, "original_name": "sales_data.csv", "type": "text/csv"}]

    print(f"Request: {request[:100]}...")
    print(f"File: {csv_file}")
    print()

    start_time = datetime.now()

    try:
        result = await orchestrator.process_request(
            request, files=files, auto_create=True
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        print("RESULTS:")
        print("=" * 40)
        print(f"Status: {result['status']}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(
            f"Workflow Type: {result.get('metadata', {}).get('workflow_type', 'unknown')}"
        )

        # Check if multi-agent workflow was used
        workflow_info = result.get("workflow", {})
        if isinstance(workflow_info, dict):
            agents_used = workflow_info.get("agents", [])
            print(f"Agents Used: {agents_used}")
            print(f"Agent Count: {len(agents_used)}")

            if len(agents_used) > 1:
                print("✅ MULTI-AGENT WORKFLOW DETECTED")
            else:
                print("ℹ️  Single agent workflow")

        # Check for workflow results and data flow
        if "results" in result:
            print(f"\nWorkflow Results Available: {len(result['results'])} steps")
            for step_name, step_result in result["results"].items():
                if isinstance(step_result, dict):
                    status = step_result.get("status", "unknown")
                    print(f"  {step_name}: {status}")

                    # Check for data flow between steps
                    if "data" in step_result and step_result["data"]:
                        data_keys = (
                            list(step_result["data"].keys())
                            if isinstance(step_result["data"], dict)
                            else ["data_present"]
                        )
                        print(f"    Data passed: {data_keys}")

        # Display response preview
        response = result.get("response", "")
        if response:
            print(f"\nResponse Preview:")
            print(f"{response[:300]}...")

            # Check if PDF was mentioned/created
            if "pdf" in response.lower():
                print("✅ PDF generation mentioned in response")
            else:
                print("⚠️ No PDF generation detected")

        # Workflow summary
        if "workflow_summary" in result:
            print(f"\nWorkflow Summary: {result['workflow_summary']}")

        return result

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


async def validate_data_flow_quality(result):
    """Validate the quality of data flow between agents"""

    if not result or result.get("status") != "success":
        print("\n❌ Cannot validate data flow - workflow failed")
        return False

    print("\nDATA FLOW VALIDATION:")
    print("=" * 40)

    validation_checks = {
        "multi_agent_workflow": False,
        "data_enrichment": False,
        "sequential_processing": False,
        "proper_output_format": False,
    }

    # Check 1: Multi-agent workflow
    workflow_info = result.get("workflow", {})
    if isinstance(workflow_info, dict):
        agents_used = workflow_info.get("agents", [])
        if len(agents_used) > 1:
            validation_checks["multi_agent_workflow"] = True
            print(f"✅ Multi-agent workflow: {len(agents_used)} agents")
        else:
            print(f"⚠️ Single agent workflow: {agents_used}")

    # Check 2: Data enrichment between steps
    if "results" in result and len(result["results"]) > 1:
        step_names = list(result["results"].keys())
        for i, step_name in enumerate(step_names[1:], 1):
            step_result = result["results"][step_name]
            if isinstance(step_result, dict) and "data" in step_result:
                validation_checks["data_enrichment"] = True
                print(f"✅ Data enrichment detected in step: {step_name}")
                break

        validation_checks["sequential_processing"] = True
        print(f"✅ Sequential processing: {len(step_names)} steps")

    # Check 3: Proper output format
    response = result.get("response", "")
    if response and len(response) > 100:
        validation_checks["proper_output_format"] = True
        print("✅ Comprehensive output generated")

    # Summary
    passed_checks = sum(validation_checks.values())
    total_checks = len(validation_checks)

    print(f"\nValidation Summary: {passed_checks}/{total_checks} checks passed")

    if passed_checks >= 3:
        print("✅ DATA FLOW VALIDATION: PASSED")
        return True
    else:
        print("⚠️ DATA FLOW VALIDATION: NEEDS IMPROVEMENT")
        return False


async def cleanup_test_files():
    """Clean up test files"""
    test_files = ["test_sales_data.csv"]

    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Cleaned up: {file}")


async def main():
    """Run complete data flow test"""

    print("Starting Multi-Agent Data Flow Test...")
    print("This test validates data passing between agents in sequential workflows")
    print()

    try:
        # Run the main test
        result = await test_multi_agent_data_flow()

        if result:
            # Validate data flow quality
            flow_valid = await validate_data_flow_quality(result)

            print("\n" + "=" * 60)
            print("TEST SUMMARY:")
            print("=" * 60)

            if flow_valid:
                print("✅ OVERALL RESULT: PASSED")
                print("   Data flow between agents is working correctly")
                print("   Multi-agent coordination is functional")
            else:
                print("⚠️ OVERALL RESULT: NEEDS WORK")
                print("   Data flow validation found issues")
                print("   Multi-agent coordination needs improvement")

        else:
            print("\n❌ OVERALL RESULT: FAILED")
            print("   Workflow execution failed")

    finally:
        # Clean up
        await cleanup_test_files()


if __name__ == "__main__":
    asyncio.run(main())
