"""
Simple test script to demonstrate the multi-agent system
without requiring FastAPI dependencies
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.matching_agent import MatchingAgent
from app.agents.optimization_agent import OptimizationAgent
from app.agents.fairness_agent import FairnessAgent
from app.agents.mediator import AgentMediator


async def test_matching_agent():
    print("=" * 60)
    print("TESTING MATCHING AGENT")
    print("=" * 60)
    
    agent = MatchingAgent()
    
    context = {
        "user_id": "user_001",
        "requested_skill": {
            "name": "Python",
            "level": "INTERMEDIATE",
            "category": "Technology"
        },
        "requester_skills": [
            {"name": "Java", "level": "ADVANCED", "category": "Technology"}
        ],
        "candidates": [
            {
                "id": "user_002",
                "offered_skills": [
                    {"name": "Python", "level": "EXPERT", "category": "Technology"}
                ],
                "requested_skills": [
                    {"name": "Java", "level": "INTERMEDIATE", "category": "Technology"}
                ],
                "trust_score": 85.0
            },
            {
                "id": "user_003",
                "offered_skills": [
                    {"name": "Python", "level": "BEGINNER", "category": "Technology"}
                ],
                "requested_skills": [],
                "trust_score": 60.0
            }
        ]
    }
    
    result = await agent.execute(context)
    
    print(f"\nAgent: {result['agent_name']}")
    print(f"Success: {result['success']}")
    print(f"Matches found: {len(result['result']['matches'])}")
    
    for i, match in enumerate(result['result']['matches'], 1):
        print(f"\n  Match {i}:")
        print(f"    User ID: {match['user_id']}")
        print(f"    Score: {match['score']:.2f}")
        print(f"    Type: {match['match_type']}")
        print(f"    Trust Score: {match['trust_score']}")
    
    print()


async def test_optimization_agent():
    print("=" * 60)
    print("TESTING OPTIMIZATION AGENT")
    print("=" * 60)
    
    agent = OptimizationAgent()
    
    context = {
        "user_id": "user_001",
        "requested_skill": {
            "name": "Design",
            "level": "ADVANCED"
        },
        "all_users": [
            {
                "id": "user_001",
                "offered_skills": [{"name": "Java", "level": "ADVANCED"}],
                "requested_skills": [{"name": "Design", "level": "ADVANCED"}],
                "trust_score": 75.0
            },
            {
                "id": "user_002",
                "offered_skills": [{"name": "Python", "level": "EXPERT"}],
                "requested_skills": [{"name": "Java", "level": "INTERMEDIATE"}],
                "trust_score": 85.0
            },
            {
                "id": "user_003",
                "offered_skills": [{"name": "Design", "level": "EXPERT"}],
                "requested_skills": [{"name": "Python", "level": "INTERMEDIATE"}],
                "trust_score": 90.0
            }
        ]
    }
    
    result = await agent.execute(context)
    
    print(f"\nAgent: {result['agent_name']}")
    print(f"Success: {result['success']}")
    print(f"Paths found: {len(result['result']['optimal_paths'])}")
    print(f"Recommendation: {result['result']['recommendation']}")
    
    for i, path in enumerate(result['result']['optimal_paths'], 1):
        print(f"\n  Path {i}:")
        print(f"    Route: {' → '.join(path['path'])}")
        print(f"    Hops: {path['hops']}")
        print(f"    Score: {path['score']:.2f}")
        print(f"    Estimated time: {path['estimated_time']} days")
    
    print()


async def test_fairness_agent():
    print("=" * 60)
    print("TESTING FAIRNESS AGENT")
    print("=" * 60)
    
    agent = FairnessAgent()
    
    context = {
        "exchange_type": "DIRECT_SWAP",
        "participants": [
            {"id": "user_001"},
            {"id": "user_002"}
        ],
        "offerings": {
            "user_001": {
                "name": "Java Programming",
                "level": "ADVANCED",
                "category": "Technology",
                "estimated_hours": 10
            },
            "user_002": {
                "name": "Python",
                "level": "INTERMEDIATE",
                "category": "Technology",
                "estimated_hours": 10
            }
        }
    }
    
    result = await agent.execute(context)
    
    print(f"\nAgent: {result['agent_name']}")
    print(f"Success: {result['success']}")
    print(f"Is Fair: {result['result']['is_fair']}")
    print(f"Fairness Score: {result['result']['fairness_score']:.2f}")
    print(f"Skill 1 Value: ${result['result']['skill1_value']:.2f}")
    print(f"Skill 2 Value: ${result['result']['skill2_value']:.2f}")
    print(f"Value Difference: ${result['result']['value_difference']:.2f}")
    print(f"Recommendation: {result['result']['recommendation']}")
    print()


async def test_mediator():
    print("=" * 60)
    print("TESTING AGENT MEDIATOR (Mediator Pattern)")
    print("=" * 60)
    
    mediator = AgentMediator()
    
    print(f"\nMediator initialized with {len(mediator.agents)} agents:")
    for agent_name in mediator.agents.keys():
        print(f"  - {agent_name}")
    
    context = {
        "user_id": "user_001",
        "requested_skill": {
            "name": "Python",
            "level": "INTERMEDIATE",
            "category": "Technology"
        },
        "offered_skill": {
            "name": "Java",
            "level": "ADVANCED",
            "category": "Technology"
        },
        "requester_skills": [
            {"name": "Java", "level": "ADVANCED", "category": "Technology"}
        ],
        "candidates": [
            {
                "id": "user_002",
                "offered_skills": [
                    {"name": "Python", "level": "EXPERT", "category": "Technology"}
                ],
                "requested_skills": [
                    {"name": "Java", "level": "INTERMEDIATE", "category": "Technology"}
                ],
                "trust_score": 85.0
            }
        ],
        "all_users": []
    }
    
    print("\nCoordinating agents to find optimal match...")
    result = await mediator.find_optimal_match(context)
    
    print(f"\nMediator Result:")
    print(f"  Success: {result['success']}")
    print(f"  Direct Matches: {len(result.get('direct_matches', []))}")
    print(f"  Multi-hop Paths: {len(result.get('multi_hop_paths', []))}")
    print(f"  Recommendation: {result.get('recommendation', 'N/A')}")
    
    # Get agent stats
    stats = mediator.get_agent_stats()
    print("\nAgent Execution Statistics:")
    for agent_name, agent_stats in stats.items():
        print(f"  {agent_stats['name']}:")
        print(f"    Executions: {agent_stats['execution_count']}")
    
    print()


async def main():
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ALTERIX - Multi-Agent AI System Demo".center(58) + "║")
    print("║" + "  FastAPI Backend (Python)".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Test individual agents
    await test_matching_agent()
    await test_optimization_agent()
    await test_fairness_agent()
    
    # Test mediator pattern
    await test_mediator()
    
    print("=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nMulti-Agent System Features Demonstrated:")
    print("  ✓ Matching Agent - Direct skill matching")
    print("  ✓ Optimization Agent - Multi-hop pathfinding")
    print("  ✓ Fairness Agent - Value balance validation")
    print("  ✓ Agent Mediator - Coordinated agent communication")
    print("\nDesign Pattern: MEDIATOR PATTERN")
    print("  The AgentMediator coordinates communication between")
    print("  multiple AI agents, orchestrating complex workflows.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
