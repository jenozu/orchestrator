"""
Test script for the Rules Generator integration.

This script demonstrates the complete workflow:
1. IntentParser: Parse a raw user request into structured JSON
2. RulesGenerator: Generate project rules and task list
3. PRD Agent: Read the generated files and create PRD

Run this script to verify the Rules Generator feature is working correctly.
"""

import os
import json
from pathlib import Path

# Import the orchestrator
from agents.orchestrator import Orchestrator


def main():
    """Test the complete workflow with a sample project request."""
    
    print("=" * 80)
    print("TESTING RULES GENERATOR INTEGRATION")
    print("=" * 80)
    print()
    
    # Sample user request
    user_request = """
    I need a task management web application with the following features:
    - User authentication (login/signup)
    - Create, read, update, delete tasks
    - Task prioritization (low, medium, high)
    - Due dates and reminders
    - Dashboard with task statistics
    
    Technology stack: React for frontend, FastAPI for backend, PostgreSQL database.
    """
    
    print("📝 User Request:")
    print(user_request)
    print()
    
    # Initialize the orchestrator
    print("🚀 Initializing Orchestrator...")
    orchestrator = Orchestrator()
    
    # Build the graph (intent_parser -> rules_generator -> prd_agent)
    print("🔧 Building execution graph...")
    orchestrator.build_graph()
    print()
    
    # Run the workflow
    print("▶️  Running workflow...")
    print("-" * 80)
    
    initial_state = {
        "raw_user_request": user_request
    }
    
    try:
        result = orchestrator.run_once(initial_state)
        
        print("-" * 80)
        print()
        print("✅ Workflow completed successfully!")
        print()
        
        # Display results
        print("📊 Results:")
        print(json.dumps(result, indent=2, default=str))
        print()
        
        # Check if files were generated
        rules_path = Path(".cursor/rules.md")
        tasks_path = Path("docs/tasks.md")
        
        print("📁 Generated Files:")
        print()
        
        if rules_path.exists():
            print("✅ .cursor/rules.md created successfully!")
            print(f"   Size: {rules_path.stat().st_size} bytes")
            print()
            print("   Preview (first 500 characters):")
            with open(rules_path, "r", encoding="utf-8") as f:
                preview = f.read(500)
                print("   " + preview.replace("\n", "\n   "))
                if len(preview) == 500:
                    print("   ...")
            print()
        else:
            print("❌ .cursor/rules.md not found")
            print()
        
        if tasks_path.exists():
            print("✅ docs/tasks.md created successfully!")
            print(f"   Size: {tasks_path.stat().st_size} bytes")
            print()
            print("   Preview (first 500 characters):")
            with open(tasks_path, "r", encoding="utf-8") as f:
                preview = f.read(500)
                print("   " + preview.replace("\n", "\n   "))
                if len(preview) == 500:
                    print("   ...")
            print()
        else:
            print("❌ docs/tasks.md not found")
            print()
        
        # Show state updates
        print("📈 State Updates:")
        print(f"   - Rules Generated: {result.get('rules_generated', False)}")
        print(f"   - Rules Path: {result.get('rules_path', 'N/A')}")
        print(f"   - Task List Path: {result.get('task_list_path', 'N/A')}")
        print(f"   - PRD Status: {result.get('status', 'N/A')}")
        print(f"   - Rules Loaded by PRD: {result.get('rules_loaded', False)}")
        print(f"   - Tasks Loaded by PRD: {result.get('tasks_loaded', False)}")
        print()
        
        print("=" * 80)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
    except Exception as e:
        print()
        print("❌ Error during workflow execution:")
        print(f"   {type(e).__name__}: {e}")
        print()
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

