#!/usr/bin/env python3
"""
Enhanced End-to-End Test - Shows complete pipeline including AI-generated response
"""

import asyncio
import pandas as pd
from datetime import datetime
import sys
import os
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from core.simplified_orchestrator import SimplifiedOrchestrator


async def test_complete_end_to_end_pipeline():
    """Test the complete execution pipeline with AI response synthesis"""

    print("🔬 COMPLETE END-TO-END PIPELINE TEST")
    print("=" * 60)

    orchestrator = SimplifiedOrchestrator()

    # Create comprehensive test data
    test_data = create_comprehensive_sales_data()

    print("📊 INPUT DATA SUMMARY:")
    print(f"   File: {test_data['name']}")
    print(f"   Records: {test_data['content']['total_rows']}")
    print(f"   Columns: {test_data['content']['columns']}")
    print(
        f"   Total Revenue: ${test_data['content']['summary_stats']['total_revenue']:,}"
    )
    print(f"   Top Region: {test_data['content']['summary_stats']['top_region']}")

    # User request
    request = "Analyze this sales data for performance trends and generate a comprehensive summary report with insights and recommendations"

    print(f"\n📝 USER REQUEST:")
    print(f"   '{request}'")

    print(f"\n🚀 EXECUTING WORKFLOW...")

    try:
        # Execute complete workflow
        result = await orchestrator.process_request(request, [test_data])

        print(f"\n✅ WORKFLOW EXECUTION SUMMARY:")
        print(f"   Status: {result.get('status')}")
        print(f"   Execution Time: {result.get('execution_time', 0):.2f}s")
        print(f"   Scenario: {result.get('metadata', {}).get('scenario', 'generic')}")
        print(
            f"   Agents Created: {result.get('metadata', {}).get('dynamic_agents_created', 0)}"
        )

        # ============================================================
        # HIGHLIGHT: AI-GENERATED FINAL RESPONSE
        # ============================================================
        ai_response = result.get("response", "No response generated")
        print(f"\n🎯 AI-GENERATED NATURAL LANGUAGE RESPONSE:")
        print("=" * 60)
        print(ai_response)
        print("=" * 60)

        # Show agent execution details
        workflow_results = result.get("results", {})
        print(f"\n🤖 AGENT EXECUTION BREAKDOWN:")

        success_count = 0
        total_count = len(workflow_results)

        for agent_name, agent_result in workflow_results.items():
            if isinstance(agent_result, dict):
                status = agent_result.get("status", "unknown")
                if status == "success":
                    success_count += 1
                    print(f"   ✅ {agent_name}: SUCCESS")

                    # Show actual data content
                    data = agent_result.get("data", {})
                    if isinstance(data, dict):
                        print(f"      📊 Data fields: {list(data.keys())}")

                        # Show specific content based on agent type
                        if agent_name == "read_csv":
                            show_csv_agent_output(data)
                        elif "insight" in agent_name or "analyzer" in agent_name:
                            show_analysis_agent_output(data)
                        elif "pdf" in agent_name or "report" in agent_name:
                            show_report_agent_output(data)
                        else:
                            show_generic_agent_output(data)
                    else:
                        print(f"      📄 Content: {str(data)[:100]}...")
                else:
                    print(f"   ❌ {agent_name}: {status}")
                    error = agent_result.get("error", "No error info")
                    print(f"      Error: {error}")
            else:
                print(f"   ⚠️  {agent_name}: Non-dict result - {type(agent_result)}")

        # Show workflow metadata
        print(f"\n📋 WORKFLOW INTELLIGENCE:")
        metadata = result.get("metadata", {})
        if metadata.get("ai_response_generated"):
            print(f"   🧠 AI Response: Generated using Claude synthesis")
        if metadata.get("innovation_demonstrated"):
            print(f"   🚀 Innovation: Dynamic agent creation demonstrated")

        workflow = result.get("workflow", {})
        if workflow.get("confidence"):
            print(f"   📈 Confidence: {workflow.get('confidence', 0):.0%}")

        # Final assessment
        print(f"\n🏆 PIPELINE ASSESSMENT:")
        print(f"   Agents Executed: {total_count}")
        print(f"   Successful: {success_count}")
        print(
            f"   Success Rate: {(success_count/total_count)*100:.1f}%"
            if total_count > 0
            else "No agents executed"
        )

        # Check for AI response quality
        ai_response_quality = assess_ai_response_quality(
            ai_response, request, test_data
        )
        print(f"   AI Response Quality: {ai_response_quality}")

        # Determine overall success
        pipeline_success = (
            success_count >= 2
            and result.get("status") == "success"
            and len(ai_response) > 100
            and ai_response_quality in ["Excellent", "Good"]
        )

        if pipeline_success:
            print(f"\n🎉 COMPLETE END-TO-END SUCCESS!")
            print(f"   ✅ Data processed successfully")
            print(f"   ✅ Agents executed and coordinated")
            print(f"   ✅ Natural language response generated")
            print(f"   ✅ Business insights delivered")
            print(f"   🚀 READY FOR PRODUCTION DEMO!")
            return True
        else:
            print(f"\n⚠️  PARTIAL SUCCESS - Pipeline needs refinement")
            if success_count < 2:
                print(f"   🔧 Agent execution issues")
            if len(ai_response) <= 100:
                print(f"   🔧 AI response too brief")
            return False

    except Exception as e:
        print(f"\n❌ PIPELINE EXECUTION FAILED: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def show_csv_agent_output(data):
    """Show CSV processing results"""
    if "processed_text" in data:
        print(f"         📊 Processed: {data.get('processed_text', '')[:50]}...")
    if "length" in data:
        print(f"         📏 Data Length: {data.get('length')} characters")


def show_analysis_agent_output(data):
    """Show analysis results"""
    # Look for key analysis fields
    analysis_fields = [
        "insights",
        "executive_summary",
        "recommendations",
        "analysis",
        "trends",
        "metrics",
    ]

    for field in analysis_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str):
                print(f"         💡 {field.title()}: {value[:80]}...")
            elif isinstance(value, list) and value:
                print(f"         💡 {field.title()}: {len(value)} items")
                for i, item in enumerate(value[:2]):  # Show first 2 items
                    print(f"            {i+1}. {str(item)[:60]}...")
            elif isinstance(value, dict):
                print(f"         💡 {field.title()}: {list(value.keys())}")


def show_report_agent_output(data):
    """Show report generation results"""
    report_fields = [
        "pdf_structure",
        "report_summary",
        "content",
        "sections",
        "pdf_content",
    ]

    for field in report_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str):
                print(f"         📄 {field.title()}: {value[:80]}...")
            elif isinstance(value, dict):
                print(f"         📄 {field.title()}: {list(value.keys())}")


def show_generic_agent_output(data):
    """Show generic agent output"""
    if "result" in data:
        print(f"         🔧 Result: {str(data['result'])[:80]}...")
    if "processing_completed" in data:
        print(f"         ✅ Processing: {data['processing_completed']}")


def assess_ai_response_quality(response, original_request, test_data):
    """Assess the quality of the AI-generated response"""

    if not response or len(response) < 50:
        return "Poor - Too brief"

    # Check if response addresses the request
    request_words = original_request.lower().split()
    key_terms = ["sales", "analysis", "trends", "performance", "insights", "report"]

    response_lower = response.lower()
    terms_addressed = sum(1 for term in key_terms if term in response_lower)

    # Check if response mentions data specifics
    data_specifics = ["revenue", "region", "product", "north", "south", "east", "west"]
    specifics_mentioned = sum(1 for spec in data_specifics if spec in response_lower)

    # Check length and detail
    if len(response) > 300 and terms_addressed >= 4 and specifics_mentioned >= 2:
        return "Excellent"
    elif len(response) > 200 and terms_addressed >= 3:
        return "Good"
    elif len(response) > 100 and terms_addressed >= 2:
        return "Fair"
    else:
        return "Poor"


def create_comprehensive_sales_data():
    """Create detailed test sales data with realistic patterns"""

    sales_data = [
        {
            "date": "2025-01-01",
            "region": "North",
            "sales_rep": "Alice Johnson",
            "revenue": 15000,
            "units_sold": 150,
            "product": "Widget A",
            "customer_type": "Enterprise",
        },
        {
            "date": "2025-01-02",
            "region": "South",
            "sales_rep": "Bob Smith",
            "revenue": 22000,
            "units_sold": 220,
            "product": "Widget B",
            "customer_type": "SMB",
        },
        {
            "date": "2025-01-03",
            "region": "East",
            "sales_rep": "Carol Davis",
            "revenue": 18000,
            "units_sold": 180,
            "product": "Widget A",
            "customer_type": "Enterprise",
        },
        {
            "date": "2025-01-04",
            "region": "West",
            "sales_rep": "David Wilson",
            "revenue": 25000,
            "units_sold": 250,
            "product": "Widget C",
            "customer_type": "Enterprise",
        },
        {
            "date": "2025-01-05",
            "region": "North",
            "sales_rep": "Alice Johnson",
            "revenue": 12000,
            "units_sold": 120,
            "product": "Widget B",
            "customer_type": "SMB",
        },
        {
            "date": "2025-01-06",
            "region": "South",
            "sales_rep": "Bob Smith",
            "revenue": 28000,
            "units_sold": 280,
            "product": "Widget A",
            "customer_type": "Enterprise",
        },
        {
            "date": "2025-01-07",
            "region": "East",
            "sales_rep": "Carol Davis",
            "revenue": 16000,
            "units_sold": 160,
            "product": "Widget C",
            "customer_type": "SMB",
        },
        {
            "date": "2025-01-08",
            "region": "West",
            "sales_rep": "David Wilson",
            "revenue": 21000,
            "units_sold": 210,
            "product": "Widget B",
            "customer_type": "Enterprise",
        },
        {
            "date": "2025-01-09",
            "region": "North",
            "sales_rep": "Alice Johnson",
            "revenue": 19000,
            "units_sold": 190,
            "product": "Widget C",
            "customer_type": "SMB",
        },
        {
            "date": "2025-01-10",
            "region": "South",
            "sales_rep": "Bob Smith",
            "revenue": 24000,
            "units_sold": 240,
            "product": "Widget A",
            "customer_type": "Enterprise",
        },
    ]

    df = pd.DataFrame(sales_data)

    # Calculate summary statistics
    region_totals = df.groupby("region")["revenue"].sum()
    product_totals = df.groupby("product")["revenue"].sum()

    return {
        "name": "comprehensive_sales_data.csv",
        "type": "csv",
        "structure": "tabular",
        "content": {
            "columns": df.columns.tolist(),
            "first_10_rows": df.to_dict("records"),
            "total_rows": len(df),
            "summary_stats": {
                "total_revenue": df["revenue"].sum(),
                "avg_revenue": df["revenue"].mean(),
                "total_units": df["units_sold"].sum(),
                "top_region": region_totals.idxmax(),
                "top_product": product_totals.idxmax(),
                "date_range": f"{df['date'].min()} to {df['date'].max()}",
            },
        },
        "read_success": True,
        "original_name": "comprehensive_sales_data.csv",
    }


async def main():
    """Run the complete end-to-end test"""

    print("🚀 Starting Complete End-to-End Pipeline Test")

    try:
        success = await test_complete_end_to_end_pipeline()

        if success:
            print("\n" + "=" * 60)
            print("🎉 COMPLETE PIPELINE SUCCESS!")
            print("✅ Input → Processing → Analysis → AI Response")
            print("✅ End-to-end workflow validated")
            print("✅ Natural language output generated")
            print("🚀 READY FOR STAKEHOLDER DEMO!")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("⚠️  PIPELINE NEEDS REFINEMENT")
            print("🔧 Check issues above and iterate")
            print("=" * 60)
            return 1

    except Exception as e:
        print(f"\n❌ Test runner failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
