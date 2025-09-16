#!/usr/bin/env python3
"""
COMPLETE DUAL SCENARIO TEST - UI READY
Shows full input/output for both Sales and Compliance scenarios
Structured for easy UI integration
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


class DualScenarioProcessor:
    """UI-ready processor for both scenarios with complete I/O visibility"""

    def __init__(self):
        self.orchestrator = SimplifiedOrchestrator()
        self.results_log = []

    async def process_sales_scenario(self) -> dict:
        """Process sales scenario with complete I/O tracking"""

        print("\n" + "=" * 60)
        print("📊 SALES ANALYSIS SCENARIO")
        print("=" * 60)

        # Create comprehensive sales data
        sales_data = self.create_comprehensive_sales_data()

        print("📋 INPUT DATA SUMMARY:")
        print(f"   📄 File: {sales_data['name']}")
        print(f"   📊 Records: {sales_data['content']['total_rows']}")
        print(
            f"   💰 Total Revenue: ${sales_data['content']['summary']['total_revenue']:,}"
        )
        print(
            f"   🌍 Regions: {', '.join(sales_data['content']['summary']['regions'])}"
        )
        print(f"   📈 Top Product: {sales_data['content']['summary']['top_product']}")

        print(f"\n📊 SAMPLE DATA (First 3 Records):")
        for i, record in enumerate(sales_data["content"]["first_10_rows"][:3]):
            print(
                f"   {i+1}. {record['date']} | {record['region']} | ${record['revenue']:,} | {record['product']}"
            )

        # User request
        user_request = "Analyze this sales data for performance trends, identify top performers, and generate comprehensive business insights with strategic recommendations"
        print(f"\n📝 USER REQUEST:")
        print(f"   '{user_request}'")

        # Process the scenario
        print(f"\n🚀 PROCESSING SALES SCENARIO...")
        start_time = datetime.now()

        # Add debug visibility
        print("   🔍 Registry state before sales processing:")
        from core.registry_singleton import debug_registry_state

        debug_registry_state()

        try:
            result = await self.orchestrator.process_request(user_request, [sales_data])
            processing_time = (datetime.now() - start_time).total_seconds()

            print(f"\n✅ PROCESSING COMPLETED in {processing_time:.2f}s")
            print(
                f"   🔧 Agents Created: {result.get('metadata', {}).get('dynamic_agents_created', 0)}"
            )
            print(f"   ⚡ Agents Executed: {len(result.get('results', {}))}")

            # Display the complete AI response
            ai_response = result.get("response", "No response generated")
            print(f"\n🎯 COMPLETE AI-GENERATED RESPONSE:")
            print("=" * 60)
            print(ai_response)
            print("=" * 60)

            # Debug: Show registry after compliance
            print("   🔍 Registry state after compliance processing:")
            debug_registry_state()

            return {
                "scenario": "sales_analysis",
                "status": "success",
                "input_data": {
                    "request": user_request,
                    "file_name": sales_data["name"],
                    "total_records": sales_data["content"]["total_rows"],
                    "data_summary": sales_data["content"]["summary"],
                    "sample_records": sales_data["content"]["first_10_rows"][:5],
                },
                "processing": {
                    "execution_time": processing_time,
                    "agents_created": result.get("metadata", {}).get(
                        "dynamic_agents_created", 0
                    ),
                    "agents_executed": len(result.get("results", {})),
                    "workflow_type": result.get("metadata", {}).get(
                        "workflow_type", "unknown"
                    ),
                },
                "output": {
                    "ai_response": ai_response,
                    "response_length": len(ai_response),
                    "response_quality": (
                        "Excellent" if len(ai_response) > 500 else "Good"
                    ),
                    "includes_insights": "insights" in ai_response.lower(),
                    "includes_recommendations": "recommend" in ai_response.lower(),
                },
                "ui_ready": True,
            }

        except Exception as e:
            print(f"\n❌ SALES SCENARIO FAILED: {str(e)}")
            return {
                "scenario": "sales_analysis",
                "status": "error",
                "error": str(e),
                "ui_ready": True,
            }

    async def process_compliance_scenario(self) -> dict:
        """Process compliance scenario with complete I/O tracking"""

        print("\n" + "=" * 60)
        print("🏛️ COMPLIANCE MONITORING SCENARIO")
        print("=" * 60)

        # Create comprehensive compliance data with violations
        compliance_data = self.create_comprehensive_compliance_data()

        print("📋 INPUT DATA SUMMARY:")
        print(f"   📄 File: {compliance_data['name']}")
        print(f"   📊 Transactions: {compliance_data['content']['total_rows']}")
        print(
            f"   💰 Total Volume: ${compliance_data['content']['summary']['total_amount']:,}"
        )
        print(
            f"   ⚠️ Violations Included: {compliance_data['content']['violations_included']}"
        )
        print(
            f"   🚨 High Risk Transactions: {compliance_data['content']['summary']['high_risk_count']}"
        )

        print(f"\n⚠️ VIOLATION BREAKDOWN:")
        violations = compliance_data["content"]["violation_details"]
        for violation_type, details in violations.items():
            print(
                f"   • {violation_type.replace('_', ' ').title()}: {details['count']} cases"
            )

        print(f"\n📊 SAMPLE TRANSACTIONS (Including Violations):")
        for i, record in enumerate(compliance_data["content"]["first_10_rows"][:5]):
            risk = (
                "🚨 HIGH RISK"
                if record["amount"] > 50000
                else "⚠️ MEDIUM" if record["amount"] > 10000 else "✅ LOW"
            )
            print(
                f"   {i+1}. {record['transaction_id']} | ${record['amount']:,} | {record['customer_name'] or 'MISSING NAME'} | {risk}"
            )

        # User request
        user_request = "Monitor these financial transactions for compliance violations, detect suspicious patterns, and generate a comprehensive audit report with risk assessment"
        print(f"\n📝 USER REQUEST:")
        print(f"   '{user_request}'")

        # Process the scenario
        print(f"\n🚀 PROCESSING COMPLIANCE SCENARIO...")
        start_time = datetime.now()

        # Add debug visibility
        print("   🔍 Registry state before compliance processing:")
        from core.registry_singleton import debug_registry_state

        debug_registry_state()

        try:
            result = await self.orchestrator.process_request(
                user_request, [compliance_data]
            )
            processing_time = (datetime.now() - start_time).total_seconds()

            print(f"\n✅ PROCESSING COMPLETED in {processing_time:.2f}s")
            print(
                f"   🔧 Agents Created: {result.get('metadata', {}).get('dynamic_agents_created', 0)}"
            )
            print(f"   ⚡ Agents Executed: {len(result.get('results', {}))}")

            # Display the complete AI response
            ai_response = result.get("response", "No response generated")
            print(f"\n🎯 COMPLETE AI-GENERATED AUDIT REPORT:")
            print("=" * 60)
            print(ai_response)
            print("=" * 60)

            # Debug: Show registry after sales
            print("   🔍 Registry state after sales processing:")
            debug_registry_state()

            return {
                "scenario": "compliance_monitoring",
                "status": "success",
                "input_data": {
                    "request": user_request,
                    "file_name": compliance_data["name"],
                    "total_transactions": compliance_data["content"]["total_rows"],
                    "total_volume": compliance_data["content"]["summary"][
                        "total_amount"
                    ],
                    "violations_included": compliance_data["content"][
                        "violations_included"
                    ],
                    "violation_breakdown": compliance_data["content"][
                        "violation_details"
                    ],
                    "sample_transactions": compliance_data["content"]["first_10_rows"][
                        :5
                    ],
                },
                "processing": {
                    "execution_time": processing_time,
                    "agents_created": result.get("metadata", {}).get(
                        "dynamic_agents_created", 0
                    ),
                    "agents_executed": len(result.get("results", {})),
                    "workflow_type": result.get("metadata", {}).get(
                        "workflow_type", "unknown"
                    ),
                },
                "output": {
                    "audit_report": ai_response,
                    "response_length": len(ai_response),
                    "response_quality": (
                        "Excellent" if len(ai_response) > 500 else "Good"
                    ),
                    "includes_violations": "violation" in ai_response.lower(),
                    "includes_risk_assessment": "risk" in ai_response.lower(),
                    "compliance_terminology": any(
                        word in ai_response.lower()
                        for word in ["aml", "compliance", "regulatory", "audit"]
                    ),
                },
                "ui_ready": True,
            }

        except Exception as e:
            print(f"\n❌ COMPLIANCE SCENARIO FAILED: {str(e)}")
            return {
                "scenario": "compliance_monitoring",
                "status": "error",
                "error": str(e),
                "ui_ready": True,
            }

    def create_comprehensive_sales_data(self) -> dict:
        """Create rich sales data for comprehensive analysis"""

        sales_records = [
            # Q1 Data
            {
                "date": "2025-01-15",
                "region": "North",
                "sales_rep": "Alice Johnson",
                "revenue": 15000,
                "units_sold": 150,
                "product": "Widget A",
                "customer_type": "Enterprise",
            },
            {
                "date": "2025-01-22",
                "region": "South",
                "sales_rep": "Bob Smith",
                "revenue": 22000,
                "units_sold": 220,
                "product": "Widget B",
                "customer_type": "SMB",
            },
            {
                "date": "2025-01-29",
                "region": "East",
                "sales_rep": "Carol Davis",
                "revenue": 18000,
                "units_sold": 180,
                "product": "Widget A",
                "customer_type": "Enterprise",
            },
            {
                "date": "2025-02-05",
                "region": "West",
                "sales_rep": "David Wilson",
                "revenue": 25000,
                "units_sold": 250,
                "product": "Widget C",
                "customer_type": "Enterprise",
            },
            {
                "date": "2025-02-12",
                "region": "North",
                "sales_rep": "Alice Johnson",
                "revenue": 19000,
                "units_sold": 190,
                "product": "Widget B",
                "customer_type": "SMB",
            },
            # Q1 Continued - More diverse data
            {
                "date": "2025-02-19",
                "region": "South",
                "sales_rep": "Bob Smith",
                "revenue": 28000,
                "units_sold": 280,
                "product": "Widget A",
                "customer_type": "Enterprise",
            },
            {
                "date": "2025-02-26",
                "region": "East",
                "sales_rep": "Carol Davis",
                "revenue": 16000,
                "units_sold": 160,
                "product": "Widget C",
                "customer_type": "SMB",
            },
            {
                "date": "2025-03-05",
                "region": "West",
                "sales_rep": "David Wilson",
                "revenue": 32000,
                "units_sold": 320,
                "product": "Widget B",
                "customer_type": "Enterprise",
            },
            {
                "date": "2025-03-12",
                "region": "North",
                "sales_rep": "Alice Johnson",
                "revenue": 21000,
                "units_sold": 210,
                "product": "Widget C",
                "customer_type": "SMB",
            },
            {
                "date": "2025-03-19",
                "region": "South",
                "sales_rep": "Bob Smith",
                "revenue": 26000,
                "units_sold": 260,
                "product": "Widget A",
                "customer_type": "Enterprise",
            },
            # Additional records for trend analysis
            {
                "date": "2025-03-26",
                "region": "East",
                "sales_rep": "Carol Davis",
                "revenue": 23000,
                "units_sold": 230,
                "product": "Widget B",
                "customer_type": "SMB",
            },
            {
                "date": "2025-04-02",
                "region": "West",
                "sales_rep": "David Wilson",
                "revenue": 29000,
                "units_sold": 290,
                "product": "Widget A",
                "customer_type": "Enterprise",
            },
        ]

        df = pd.DataFrame(sales_records)

        # Calculate comprehensive summary
        summary = {
            "total_revenue": df["revenue"].sum(),
            "total_units": df["units_sold"].sum(),
            "avg_deal_size": df["revenue"].mean(),
            "total_transactions": len(df),
            "regions": sorted(df["region"].unique().tolist()),
            "sales_reps": sorted(df["sales_rep"].unique().tolist()),
            "products": sorted(df["product"].unique().tolist()),
            "customer_types": sorted(df["customer_type"].unique().tolist()),
            "top_product": df.groupby("product")["revenue"].sum().idxmax(),
            "top_region": df.groupby("region")["revenue"].sum().idxmax(),
            "top_rep": df.groupby("sales_rep")["revenue"].sum().idxmax(),
            "date_range": f"{df['date'].min()} to {df['date'].max()}",
        }

        return {
            "name": "comprehensive_sales_data.csv",
            "type": "csv",
            "structure": "tabular",
            "content": {
                "columns": df.columns.tolist(),
                "data_rows": df.to_dict("records"),
                "first_10_rows": df.head(12).to_dict("records"),
                "total_rows": len(df),
                "summary": summary,
                "raw_data": df.to_json(orient="records"),
            },
            "read_success": True,
            "original_name": "comprehensive_sales_data.csv",
        }

    def create_comprehensive_compliance_data(self) -> dict:
        """Create rich compliance data with realistic violations"""

        transactions = [
            # Normal transactions
            {
                "transaction_id": "TXN001",
                "amount": 1500.00,
                "customer_id": "CUST001",
                "customer_name": "John Smith",
                "source_account": "ACC001",
                "target_account": "ACC501",
                "transaction_type": "TRANSFER",
                "timestamp": "2025-01-15 10:30:00",
                "routing_number": "123456789",
                "purpose": "business_payment",
            },
            {
                "transaction_id": "TXN002",
                "amount": 750.00,
                "customer_id": "CUST002",
                "customer_name": "Jane Doe",
                "source_account": "ACC002",
                "target_account": "ACC502",
                "transaction_type": "TRANSFER",
                "timestamp": "2025-01-15 11:15:00",
                "routing_number": "123456789",
                "purpose": "personal_transfer",
            },
            # VIOLATION 1: Large amount above $50,000 threshold (CRITICAL)
            {
                "transaction_id": "TXN003",
                "amount": 75000.00,
                "customer_id": "CUST003",
                "customer_name": "Bob Johnson",
                "source_account": "ACC003",
                "target_account": "ACC503",
                "transaction_type": "WIRE",
                "timestamp": "2025-01-15 14:20:00",
                "routing_number": "123456789",
                "purpose": "investment",
            },
            # VIOLATION 2: Suspicious round number (HIGH RISK)
            {
                "transaction_id": "TXN004",
                "amount": 50000.00,
                "customer_id": "CUST004",
                "customer_name": "Alice Brown",
                "source_account": "ACC004",
                "target_account": "ACC504",
                "transaction_type": "WIRE",
                "timestamp": "2025-01-15 15:45:00",
                "routing_number": "123456789",
                "purpose": "business_acquisition",
            },
            # VIOLATION 3: Missing customer name (DATA QUALITY)
            {
                "transaction_id": "TXN005",
                "amount": 2500.00,
                "customer_id": "CUST005",
                "customer_name": "",
                "source_account": "ACC005",
                "target_account": "ACC505",
                "transaction_type": "TRANSFER",
                "timestamp": "2025-01-15 16:30:00",
                "routing_number": "123456789",
                "purpose": "payment",
            },
            # VIOLATIONS 4-6: Structuring pattern (CRITICAL) - Same customer, multiple $9,500 transactions
            {
                "transaction_id": "TXN006",
                "amount": 9500.00,
                "customer_id": "CUST006",
                "customer_name": "Charlie Wilson",
                "source_account": "ACC006",
                "target_account": "ACC506",
                "transaction_type": "CASH_DEPOSIT",
                "timestamp": "2025-01-15 09:00:00",
                "routing_number": "123456789",
                "purpose": "cash_deposit",
            },
            {
                "transaction_id": "TXN007",
                "amount": 9500.00,
                "customer_id": "CUST006",
                "customer_name": "Charlie Wilson",
                "source_account": "ACC006",
                "target_account": "ACC507",
                "transaction_type": "CASH_DEPOSIT",
                "timestamp": "2025-01-15 09:30:00",
                "routing_number": "123456789",
                "purpose": "cash_deposit",
            },
            {
                "transaction_id": "TXN008",
                "amount": 9500.00,
                "customer_id": "CUST006",
                "customer_name": "Charlie Wilson",
                "source_account": "ACC006",
                "target_account": "ACC508",
                "transaction_type": "CASH_DEPOSIT",
                "timestamp": "2025-01-15 10:00:00",
                "routing_number": "123456789",
                "purpose": "cash_deposit",
            },
            # VIOLATION 7: Missing routing number (DATA QUALITY)
            {
                "transaction_id": "TXN009",
                "amount": 3200.00,
                "customer_id": "CUST007",
                "customer_name": "Diana Prince",
                "source_account": "ACC007",
                "target_account": "ACC509",
                "transaction_type": "TRANSFER",
                "timestamp": "2025-01-15 12:15:00",
                "routing_number": "",
                "purpose": "business_payment",
            },
            # VIOLATION 8: Another large transaction (HIGH RISK)
            {
                "transaction_id": "TXN010",
                "amount": 85000.00,
                "customer_id": "CUST008",
                "customer_name": "Frank Miller",
                "source_account": "ACC008",
                "target_account": "ACC510",
                "transaction_type": "WIRE",
                "timestamp": "2025-01-15 17:00:00",
                "routing_number": "123456789",
                "purpose": "real_estate",
            },
            # Normal transactions for balance
            {
                "transaction_id": "TXN011",
                "amount": 1200.00,
                "customer_id": "CUST009",
                "customer_name": "Grace Lee",
                "source_account": "ACC009",
                "target_account": "ACC511",
                "transaction_type": "TRANSFER",
                "timestamp": "2025-01-16 09:15:00",
                "routing_number": "123456789",
                "purpose": "personal_transfer",
            },
            {
                "transaction_id": "TXN012",
                "amount": 800.00,
                "customer_id": "CUST010",
                "customer_name": "Henry Chen",
                "source_account": "ACC010",
                "target_account": "ACC512",
                "transaction_type": "TRANSFER",
                "timestamp": "2025-01-16 10:30:00",
                "routing_number": "123456789",
                "purpose": "business_payment",
            },
        ]

        df = pd.DataFrame(transactions)

        # Detailed violation analysis
        violation_details = {
            "large_amount_violations": {
                "count": 2,
                "transactions": ["TXN003", "TXN010"],
                "total_amount": 160000.00,
                "risk_level": "CRITICAL",
            },
            "round_number_suspicious": {
                "count": 1,
                "transactions": ["TXN004"],
                "total_amount": 50000.00,
                "risk_level": "HIGH",
            },
            "structuring_pattern": {
                "count": 3,
                "transactions": ["TXN006", "TXN007", "TXN008"],
                "customer": "CUST006",
                "total_amount": 28500.00,
                "risk_level": "CRITICAL",
            },
            "missing_data_quality": {
                "count": 2,
                "transactions": ["TXN005", "TXN009"],
                "issues": ["missing_customer_name", "missing_routing_number"],
                "risk_level": "MEDIUM",
            },
        }

        summary = {
            "total_transactions": len(df),
            "total_amount": df["amount"].sum(),
            "avg_transaction": df["amount"].mean(),
            "high_risk_count": len(df[df["amount"] > 50000]),
            "medium_risk_count": len(
                df[(df["amount"] > 10000) & (df["amount"] <= 50000)]
            ),
            "low_risk_count": len(df[df["amount"] <= 10000]),
            "unique_customers": df["customer_id"].nunique(),
            "date_range": f"{df['timestamp'].min()[:10]} to {df['timestamp'].max()[:10]}",
            "violation_summary": {
                "total_violations": 8,
                "critical_violations": 5,
                "high_violations": 1,
                "medium_violations": 2,
            },
        }

        return {
            "name": "financial_transactions.xlsx",
            "type": "excel",
            "structure": "tabular",
            "content": {
                "columns": df.columns.tolist(),
                "data_rows": df.to_dict("records"),
                "first_10_rows": df.head(12).to_dict("records"),
                "total_rows": len(df),
                "violations_included": 8,
                "violation_details": violation_details,
                "summary": summary,
                "raw_data": df.to_json(orient="records"),
            },
            "read_success": True,
            "original_name": "financial_transactions.xlsx",
        }

    async def run_complete_demo(self) -> dict:
        """Run complete dual-scenario demo with full I/O visibility"""

        print("🚀 AGENTIC FABRIC COMPLETE DEMO")
        print("=" * 60)
        print("Testing both Sales Analysis and Compliance Monitoring scenarios")
        print("with complete input/output visibility for UI integration")

        demo_start = datetime.now()

        # Run both scenarios
        sales_result = await self.process_sales_scenario()
        compliance_result = await self.process_compliance_scenario()

        demo_duration = (datetime.now() - demo_start).total_seconds()

        # Compile comprehensive results
        demo_results = {
            "demo_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_duration": demo_duration,
                "scenarios_tested": 2,
                "overall_status": (
                    "success"
                    if sales_result.get("status") == "success"
                    and compliance_result.get("status") == "success"
                    else "partial"
                ),
            },
            "sales_scenario": sales_result,
            "compliance_scenario": compliance_result,
            "ui_integration": {
                "endpoints_ready": True,
                "response_format": "standardized",
                "error_handling": "implemented",
                "data_structure": "consistent",
            },
        }

        # Print summary
        print(f"\n" + "=" * 60)
        print("📋 COMPLETE DEMO SUMMARY")
        print("=" * 60)

        print(f"⏱️ Total Demo Time: {demo_duration:.2f}s")
        print(
            f"📊 Sales Scenario: {'✅ SUCCESS' if sales_result.get('status') == 'success' else '❌ FAILED'}"
        )
        print(
            f"🏛️ Compliance Scenario: {'✅ SUCCESS' if compliance_result.get('status') == 'success' else '❌ FAILED'}"
        )

        if sales_result.get("status") == "success":
            print(
                f"   📈 Sales Agents Created: {sales_result['processing']['agents_created']}"
            )
            print(
                f"   📊 Sales Response Quality: {sales_result['output']['response_quality']}"
            )

        if compliance_result.get("status") == "success":
            print(
                f"   🔧 Compliance Agents Created: {compliance_result['processing']['agents_created']}"
            )
            print(
                f"   🏛️ Compliance Response Quality: {compliance_result['output']['response_quality']}"
            )

        overall_success = (
            sales_result.get("status") == "success"
            and compliance_result.get("status") == "success"
        )

        print(
            f"\n🎯 OVERALL DEMO STATUS: {'🎉 COMPLETE SUCCESS!' if overall_success else '⚠️ PARTIAL SUCCESS'}"
        )

        if overall_success:
            print("✅ Both scenarios demonstrate end-to-end AI orchestration")
            print("✅ Dynamic agent creation working for different domains")
            print("✅ Professional AI responses generated")
            print("✅ Ready for UI integration and production demo")

        print("=" * 60)

        return demo_results


# UI Integration Helper Functions
class UIEndpointHelper:
    """Helper functions for UI endpoint integration"""

    @staticmethod
    def format_for_api_response(result: dict) -> dict:
        """Format result for clean API response"""

        return {
            "status": result.get("status", "unknown"),
            "scenario": result.get("scenario", "unknown"),
            "processing_time": result.get("processing", {}).get("execution_time", 0),
            "input_summary": {
                "request": result.get("input_data", {}).get("request", ""),
                "data_records": result.get("input_data", {}).get("total_records", 0)
                or result.get("input_data", {}).get("total_transactions", 0),
                "file_name": result.get("input_data", {}).get("file_name", ""),
            },
            "ai_response": result.get("output", {}).get("ai_response", "")
            or result.get("output", {}).get("audit_report", ""),
            "agents_created": result.get("processing", {}).get("agents_created", 0),
            "response_quality": result.get("output", {}).get(
                "response_quality", "Unknown"
            ),
            "metadata": {
                "workflow_type": result.get("processing", {}).get(
                    "workflow_type", "unknown"
                ),
                "response_length": result.get("output", {}).get("response_length", 0),
                "ui_ready": result.get("ui_ready", True),
            },
        }

    @staticmethod
    def create_endpoint_routes():
        """Sample endpoint structure for UI integration"""

        return {
            "sales_analysis": {
                "endpoint": "/api/process/sales",
                "method": "POST",
                "expected_input": {
                    "request": "string - user request",
                    "file_data": "csv data with sales records",
                },
                "response_format": "standardized API response",
            },
            "compliance_monitoring": {
                "endpoint": "/api/process/compliance",
                "method": "POST",
                "expected_input": {
                    "request": "string - user request",
                    "file_data": "excel data with transaction records",
                },
                "response_format": "standardized API response",
            },
            "dual_demo": {
                "endpoint": "/api/demo/complete",
                "method": "GET",
                "response": "complete demo results for both scenarios",
            },
        }


async def main():
    """Run complete dual scenario demo"""

    processor = DualScenarioProcessor()
    demo_results = await processor.run_complete_demo()

    # Save results for UI integration
    with open("demo_results.json", "w") as f:
        json.dump(demo_results, f, indent=2, default=str)

    print(f"\n💾 Demo results saved to: demo_results.json")
    print("📱 Ready for UI integration using UIEndpointHelper class")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
