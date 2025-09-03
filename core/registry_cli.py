"""
Registry CLI - Test the registry system
"""

from registry import RegistryManager


def test_registry():
    """Test registry operations."""
    registry = RegistryManager()

    print("\n" + "=" * 50)
    print("REGISTRY SYSTEM TEST")
    print("=" * 50)

    # Test tool registration
    print("\nTesting Tool Registration...")

    sample_tool_code = '''def extract_emails(text):
    """Extract email addresses from text."""
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return list(set(emails))  # Remove duplicates
'''

    registry.register_tool(
        name="extract_emails",
        description="Extracts email addresses from text using regex",
        code=sample_tool_code,
        tags=["text-processing", "extraction", "email"],
    )

    # Test agent registration
    print("\nTesting Agent Registration...")

    sample_agent_code = '''def email_extractor_agent(state):
    """Agent that extracts emails from text."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from generated.tools.extract_emails import extract_emails
    
    try:
        # Get input
        text = state.get('current_data', {}).get('text', '')
        
        # Use tool
        emails = extract_emails(text)
        
        # Format output
        result = {
            "status": "success",
            "data": {
                "emails": emails,
                "count": len(emails)
            },
            "metadata": {
                "agent": "email_extractor",
                "tools_used": ["extract_emails"],
                "execution_time": 0.1
            }
        }
        
        # Update state
        state['results']['email_extractor'] = result
        state['current_data'] = result['data']
        state['execution_path'].append('email_extractor')
        
    except Exception as e:
        state['errors'].append({
            "agent": "email_extractor",
            "error": str(e)
        })
    
    return state
'''

    registry.register_agent(
        name="email_extractor",
        description="Extracts email addresses from provided text",
        code=sample_agent_code,
        uses_tools=["extract_emails"],
        input_schema={"text": "string"},
        output_schema={"emails": "array", "count": "integer"},
        tags=["extraction", "email", "text-processing"],
    )

    # Test retrieval
    print("\nTesting Retrieval...")

    agent = registry.get_agent("email_extractor")
    if agent:
        print(f"  Found agent: {agent['description']}")
        print(f"  Uses tools: {agent['uses_tools']}")
        print(f"  Location: {agent['location']}")

    tool = registry.get_tool("extract_emails")
    if tool:
        print(f"  Found tool: {tool['description']}")
        print(f"  Used by: {tool['used_by_agents']}")

    # Test dependencies
    print("\nTesting Dependencies...")
    deps = registry.get_agent_dependencies("email_extractor")
    print(f"  Agent dependencies: {deps}")

    usage = registry.get_tool_usage("extract_emails")
    print(f"  Tool usage: {usage}")

    # Test search
    print("\nTesting Search...")
    results = registry.search_agents("email")
    print(f"  Found {len(results)} agents matching 'email'")

    results = registry.search_tools("extract")
    print(f"  Found {len(results)} tools matching 'extract'")

    # Test statistics
    print("\nRegistry Statistics:")
    stats = registry.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nRegistry test completed successfully!")

    # Test listing
    print("\nCurrent Registry Contents:")
    print(f"  Agents: {[a['name'] for a in registry.list_agents()]}")
    print(f"  Tools: {[t['name'] for t in registry.list_tools()]}")


if __name__ == "__main__":
    test_registry()
