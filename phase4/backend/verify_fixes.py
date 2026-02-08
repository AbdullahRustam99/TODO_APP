#!/usr/bin/env python3
"""
Simple test to verify the ModelSettings fix in the AI agent
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def test_model_settings_fix():
    """Test that the ModelSettings configuration is fixed"""
    print("Testing ModelSettings configuration fix...")

    try:
        # Import the agent
        from ai.agents.todo_agent import todo_agent

        # Check that it exists and has proper configuration
        assert todo_agent is not None
        print("✓ AI Agent imported successfully")

        # If we reach this point, the ModelSettings issue is fixed
        print("✓ ModelSettings configuration is correct")
        return True

    except TypeError as e:
        if "model_settings must be a ModelSettings instance" in str(e):
            print(f"✗ ModelSettings configuration error still exists: {e}")
            return False
        else:
            print(f"✗ Unexpected error: {e}")
            return False
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_server_import():
    """Test that MCP server can be imported without experimental tasks error"""
    print("\nTesting MCP server import...")

    try:
        import importlib.util
        import sys

        # Load the server module dynamically to avoid import conflicts
        spec = importlib.util.spec_from_file_location("mcp_server",
                                                     "ai/mcp/server.py")
        mcp_module = importlib.util.module_from_spec(spec)

        # Check if the experimental tasks import exists in the file
        with open("ai/mcp/server.py", 'r') as f:
            content = f.read()

        if "from mcp.server.experimental.tasks import ServerTaskContext" in content:
            print("✓ Experimental tasks import exists in server")
        else:
            print("✓ Experimental tasks import not found (may have been fixed)")

        # Try importing the server module normally
        from ai.mcp import server
        print("✓ MCP server imported successfully")
        return True

    except ImportError as e:
        print(f"✗ MCP server import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Verifying AI chatbot MCP server fixes...\n")

    test1_passed = test_model_settings_fix()
    test2_passed = test_mcp_server_import()

    print(f"\nResults:")
    print(f"ModelSettings fix: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"MCP Server import: {'✓ PASSED' if test2_passed else '✗ FAILED'}")

    all_passed = test1_passed and test2_passed

    if all_passed:
        print("\n🎉 All verification tests passed!")
        print("The AI chatbot with MCP server fixes are working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the errors above.")

    exit(0 if all_passed else 1)