from agentpress.tool import ToolResult, openapi_schema, usage_example, Tool
from agentpress.thread_manager import ThreadManager
from services.supabase import DBConnection
from utils.logger import logger
from typing import Optional
import json

class AgentDiscoveryTool(Tool):
    """
    Tool for discovering and listing available agents and their workflows.
    
    Allows agents to discover other agents in the same account and view their capabilities.
    This enables agent-to-agent communication and coordination within the platform.
    """

    def __init__(self, project_id: str, thread_manager: ThreadManager, account_id: str):
        super().__init__()
        self.project_id = project_id
        self.thread_manager = thread_manager
        self.account_id = account_id
        # Create direct database connection like MCP layer
        self.db = DBConnection()

    @openapi_schema({
        "type": "function",
        "function": {
            "name": "discover_agents",
            "description": "Discover available agents and their workflows. Returns agent IDs, names, descriptions, and available workflows with workflow IDs.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    })
    @usage_example('''
        <function_calls>
        <invoke name="discover_agents">
        </invoke>
        </function_calls>
        ''')
    async def discover_agents(self) -> ToolResult:
        """Discover all available agents and their workflows."""
        try:
            client = await self.db.client
            
            # Get all agents in the account
            agents_result = await client.table('agents').select('agent_id, name, description').eq("account_id", self.account_id).order('created_at', desc=True).execute()
            
            if not agents_result.data:
                return self.success_response([])
            
            # TODO: Fix N+1 Database Query Problem - Currently making separate query for each agent's workflows
            # Should use JOIN query or batch fetch all workflows at once, then group by agent_id
            # Performance impact: 100 agents = 101 database calls instead of 2
            
            agents = []
            for agent in agents_result.data:
                agent_id = agent['agent_id']
                
                # Skip current agent
                if agent_id == getattr(self.thread_manager, 'current_agent_id', None):
                    continue
                
                # Get workflows for this agent with error handling
                workflows = []
                try:
                    workflows_result = await client.table('agent_workflows').select('id, name, description').eq('agent_id', agent_id).execute()
                    
                    if workflows_result.data:
                        for workflow in workflows_result.data:
                            workflows.append({
                                "workflow_id": workflow['id'],
                                "name": workflow['name'],
                                "description": workflow.get('description')
                            })
                except Exception as e:
                    logger.warning(f"Failed to fetch workflows for agent {agent_id}: {str(e)}")
                    # Continue with empty workflows array - don't fail the entire discovery
                
                agents.append({
                    "agent_id": agent_id,
                    "name": agent['name'],
                    "description": agent.get('description'),
                    "workflows": workflows
                })
            
            return self.success_response(agents)
            
        except Exception as e:
            logger.error(f"Error in discover_agents: {str(e)}")
            return self.fail_response(f"Error discovering agents: {str(e)}")