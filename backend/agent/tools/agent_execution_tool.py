from agentpress.tool import ToolResult, openapi_schema, usage_example, Tool
from agentpress.thread_manager import ThreadManager
from services.supabase import DBConnection
from utils.logger import logger
from typing import Optional
import json
import asyncio
import uuid
from datetime import datetime, timezone, timedelta

class AgentExecutionTool(Tool):
    """
    Tool for executing other agents with prompts or workflows.
    
    Enables agent-to-agent communication by allowing one agent to call another
    and receive the results. Supports both custom prompt execution and workflow execution.
    """

    def __init__(self, project_id: str, thread_manager: ThreadManager, account_id: str):
        super().__init__()
        self.project_id = project_id
        self.thread_manager = thread_manager
        self.account_id = account_id
        # Create direct database connection like MCP layer
        self.db = DBConnection()

    def _extract_last_message(self, full_output: str) -> str:
        """Extract the last meaningful message from agent output."""
        if not full_output.strip():
            return "No output received"
        
        lines = full_output.strip().split('\n')
        
        # Look for the last substantial message
        for line in reversed(lines):
            if line.strip() and not line.startswith('#') and not line.startswith('```'):
                try:
                    line_index = lines.index(line)
                    start_index = max(0, line_index - 3)
                    return '\n'.join(lines[start_index:]).strip()
                except ValueError:
                    return line.strip()
        
        # Fallback: return last 20% of the output
        return full_output[-len(full_output)//5:].strip() if len(full_output) > 100 else full_output

    def _truncate_from_end(self, text: str, max_tokens: int) -> str:
        """Truncate text from the beginning, keeping the end."""
        if max_tokens <= 0:
            return ""
        
        max_chars = max_tokens * 4  # Rough token estimation
        
        if len(text) <= max_chars:
            return text
        
        truncated = text[-max_chars:]
        return f"...[truncated {len(text) - max_chars} characters]...\n{truncated}"

    def _get_fallback_model(self, requested_model: Optional[str] = None) -> str:
        """Get a reliable model with fallback logic."""
        if requested_model:
            # Validate the requested model is reasonable
            if any(provider in requested_model.lower() for provider in ['openrouter', 'anthropic', 'openai', 'google']):
                return requested_model
        
        # Use a reliable free-tier model as fallback
        fallback_model = "openrouter/google/gemini-2.5-flash"
        if requested_model and requested_model != fallback_model:
            logger.info(f"Model {requested_model} not validated, using fallback: {fallback_model}")
        
        return fallback_model

    @openapi_schema({
        "type": "function",
        "function": {
            "name": "call_agent",
            "description": "Execute another agent with a custom prompt or workflow. This allows inter-agent communication and delegation of tasks to specialized agents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "The ID of the agent to call"
                    },
                    "message": {
                        "type": "string",
                        "description": "The message/prompt to send to the agent"
                    },
                    "execution_mode": {
                        "type": "string",
                        "enum": ["prompt", "workflow"],
                        "description": "Either 'prompt' for custom prompt execution or 'workflow' for workflow execution",
                        "default": "prompt"
                    },
                    "workflow_id": {
                        "type": "string",
                        "description": "Required when execution_mode is 'workflow' - the ID of the workflow to run"
                    },
                    "model_name": {
                        "type": "string",
                        "description": "Model to use for the agent execution. If not specified, uses the agent's configured model or fallback."
                    },
                    "timeout": {
                        "type": "integer", 
                        "description": "Maximum time to wait for agent response in seconds",
                        "default": 300,
                        "minimum": 60,
                        "maximum": 1800
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens in response",
                        "default": 1000,
                        "minimum": 100,
                        "maximum": 4000
                    },
                    "output_mode": {
                        "type": "string",
                        "enum": ["last_message", "full"],
                        "description": "How to format output: 'last_message' (default) extracts key results, 'full' returns complete output",
                        "default": "last_message"
                    }
                },
                "required": ["agent_id", "message"]
            }
        }
    })
    @usage_example('''
        <function_calls>
        <invoke name="call_agent">
        <parameter name="agent_id">data_analyst_agent_123</parameter>
        <parameter name="message">Analyze the sales data from Q3 and provide key insights</parameter>
        <parameter name="execution_mode">prompt</parameter>
        <parameter name="timeout">600</parameter>
        </invoke>
        </function_calls>
        
        <!-- Example with workflow -->
        <function_calls>
        <invoke name="call_agent">
        <parameter name="agent_id">report_generator_456</parameter>
        <parameter name="message">Generate monthly report with latest metrics</parameter>
        <parameter name="execution_mode">workflow</parameter>
        <parameter name="workflow_id">monthly_report_workflow_789</parameter>
        </invoke>
        </function_calls>
        ''')
    async def call_agent(
        self, 
        agent_id: str, 
        message: str, 
        execution_mode: str = "prompt",
        workflow_id: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout: int = 300,
        max_tokens: int = 1000,
        output_mode: str = "last_message"
    ) -> ToolResult:
        """Execute another agent and return the results."""
        try:
            # Validate execution mode and workflow parameters
            if execution_mode not in ["prompt", "workflow"]:
                return self.fail_response("Error: execution_mode must be either 'prompt' or 'workflow'")
            
            if execution_mode == "workflow" and not workflow_id:
                return self.fail_response("Error: workflow_id is required when execution_mode is 'workflow'")
            
            # Verify agent access
            await self._verify_agent_access(agent_id)
            
            # Apply model fallback logic
            model_name = self._get_fallback_model(model_name)
            
            # Validate parameters
            timeout = max(60, min(1800, timeout))  # Clamp between 1 minute and 30 minutes
            max_tokens = max(100, min(4000, max_tokens))  # Clamp between 100 and 4000 tokens
            
            # Validate output mode
            if output_mode not in ["last_message", "full"]:
                output_mode = "last_message"
            
            logger.info(f"Calling agent {agent_id} in {execution_mode} mode with timeout {timeout}s")
            
            if execution_mode == "workflow":
                # Execute workflow
                raw_result = await self._execute_agent_workflow(agent_id, workflow_id, message, model_name, timeout)
            else:
                # Execute agent with prompt
                raw_result = await self._execute_agent_prompt(agent_id, message, model_name, timeout)
            
            # Process the result based on output mode
            if "Error:" in raw_result:
                # Handle error cases
                response_data = {
                    "agent_id": agent_id,
                    "execution_mode": execution_mode,
                    "workflow_id": workflow_id if execution_mode == "workflow" else None,
                    "model_used": model_name,
                    "output_mode": output_mode,
                    "max_tokens": max_tokens,
                    "status": "failed",
                    "result": raw_result,
                    "timestamp": datetime.now().isoformat()
                }
                logger.error(f"Agent call failed for agent {agent_id}: {raw_result}")
                return self.fail_response(response_data)
            else:
                # Handle successful execution
                if output_mode == "last_message":
                    # Extract the meaningful response from the raw result
                    processed_result = self._extract_last_message(raw_result)
                elif output_mode == "full":
                    # Return full output but truncate if necessary
                    processed_result = self._truncate_from_end(raw_result, max_tokens)
                else:
                    processed_result = raw_result
                
                response_data = {
                    "agent_id": agent_id,
                    "execution_mode": execution_mode,
                    "workflow_id": workflow_id if execution_mode == "workflow" else None,
                    "model_used": model_name,
                    "output_mode": output_mode,
                    "max_tokens": max_tokens,
                    "status": "completed",
                    "result": processed_result,
                    "raw_result": raw_result if output_mode == "last_message" else None,  # Include raw result for debugging
                    "timestamp": datetime.now().isoformat()
                }
                
                logger.info(f"Agent call completed successfully for agent {agent_id} in {execution_mode} mode")
                return self.success_response(response_data)
            
        except Exception as e:
            logger.error(f"Error calling agent {agent_id}: {str(e)}")
            return self.fail_response(f"Error calling agent: {str(e)}")

    async def _execute_agent_workflow(self, agent_id: str, workflow_id: str, message: str, model_name: str, timeout: int) -> str:
        """Execute an agent workflow."""
        try:
            client = await self.db.client
            
            # Verify workflow exists and is active
            workflow_result = await client.table('agent_workflows').select('*').eq('id', workflow_id).eq('agent_id', agent_id).execute()
            if not workflow_result.data:
                return f"Error: Workflow {workflow_id} not found for agent {agent_id}"
            
            workflow = workflow_result.data[0]
            if workflow.get('status') != 'active':
                return f"Error: Workflow {workflow['name']} is not active (status: {workflow.get('status')})"
            
            # Execute workflow through the execution service
            try:
                from triggers.execution_service import execute_workflow
                
                # Execute the workflow with the provided message
                execution_result = await execute_workflow(
                    workflow_id=workflow_id,
                    agent_id=agent_id,
                    input_data={"message": message},
                    user_id=self.account_id
                )
                
                if execution_result.get('success'):
                    return execution_result.get('output', f"Workflow '{workflow['name']}' executed successfully")
                else:
                    return f"Workflow execution failed: {execution_result.get('error', 'Unknown error')}"
                    
            except ImportError:
                logger.warning("Execution service not available, using fallback workflow execution")
                # Fallback: Create a thread and run the agent with workflow context
                return await self._execute_agent_with_thread(agent_id, message, model_name, timeout, workflow)
        
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
            return f"Error executing workflow: {str(e)}"

    async def _execute_agent_prompt(self, agent_id: str, message: str, model_name: str, timeout: int) -> str:
        """Execute an agent with a custom prompt."""
        try:
            return await self._execute_agent_with_thread(agent_id, message, model_name, timeout)
        except Exception as e:
            logger.error(f"Error executing agent prompt: {str(e)}")
            return f"Error executing agent: {str(e)}"

    async def _execute_agent_with_thread(self, agent_id: str, message: str, model_name: str, timeout: int, workflow: Optional[dict] = None) -> str:
        """Execute agent using direct database operations with proper timeout handling."""
        try:
            client = await self.db.client
            
            # Create thread name based on execution type
            thread_name = f"Workflow: {workflow['name']}" if workflow else "Agent-to-Agent Call"
            
            # Create a new thread directly in database
            thread_id = str(uuid.uuid4())
            thread_data = {
                'thread_id': thread_id,
                'account_id': self.account_id,
                'project_id': self.project_id,
                'is_public': False,
                'metadata': {
                    'agent_execution_tool': True,
                    'workflow_execution': workflow is not None,
                    'workflow_name': workflow.get('name') if workflow else None,
                    'timeout': timeout
                }
            }
            await client.table('threads').insert(thread_data).execute()
            
            # Prepare message with workflow context if needed
            final_message = message
            if workflow:
                workflow_context = f"Executing workflow '{workflow['name']}'"
                if workflow.get('description'):
                    workflow_context += f": {workflow['description']}"
                final_message = f"{workflow_context}\n\nUser message: {message}"
            
            # Add the message to the thread directly
            message_data = {
                'message_id': str(uuid.uuid4()),
                'thread_id': thread_id,
                'content': json.dumps({
                    'role': 'user',
                    'content': final_message
                }),
                'type': 'user',
                'is_llm_message': False,
                'agent_id': agent_id,
                'metadata': {
                    'agent_execution_tool': True
                }
            }
            await client.table('messages').insert(message_data).execute()
            
            # Create agent run record directly (let database auto-generate 'id')
            agent_run_data = {
                'thread_id': thread_id,
                'agent_id': agent_id,
                'status': 'running',
                'started_at': datetime.now(timezone.utc).isoformat(),
                'metadata': {
                    'model_name': model_name,
                    'enable_thinking': False,
                    'reasoning_effort': 'low',
                    'enable_context_manager': True,
                    'agent_execution_tool': True,
                    'workflow_execution': workflow is not None,
                    'timeout': timeout
                }
            }
            result = await client.table('agent_runs').insert(agent_run_data).execute()
            agent_run_id = result.data[0]['id']  # Use auto-generated primary key
            
            # Trigger agent execution through the background task system
            try:
                from run_agent_background import run_agent_background
                
                # Get agent config for the agent
                agent_result = await client.table('agents').select('*').eq('agent_id', agent_id).execute()
                if not agent_result.data:
                    return f"Error: Agent {agent_id} not found"
                
                agent_config = agent_result.data[0]
                
                # Get current version config if needed
                if agent_config.get('current_version_id'):
                    version_result = await client.table('agent_versions').select('*').eq('version_id', agent_config['current_version_id']).execute()
                    if version_result.data:
                        agent_config['current_version'] = version_result.data[0]
                
                # Run agent in background and wait for completion with timeout
                background_task = asyncio.create_task(run_agent_background(
                    agent_run_id=agent_run_id,
                    thread_id=thread_id,
                    instance_id="agent_execution_tool",
                    project_id=self.project_id,
                    model_name=model_name,
                    enable_thinking=False,
                    reasoning_effort='low',
                    stream=False,
                    enable_context_manager=True,
                    agent_config=agent_config
                ))
                
                logger.info(f"Started agent {agent_id} with run ID {agent_run_id}, waiting up to {timeout}s for completion")
                
                # Wait for agent completion with timeout
                try:
                    await asyncio.wait_for(background_task, timeout=timeout)
                    
                    # Agent completed, get the final result
                    return await self._get_agent_execution_result(agent_run_id, thread_id, timeout=10)
                    
                except asyncio.TimeoutError:
                    logger.warning(f"Agent {agent_id} execution timed out after {timeout}s, cancelling task")
                    
                    # Cancel the background task
                    background_task.cancel()
                    
                    # Mark agent run as failed due to timeout
                    await self._mark_agent_run_as_failed(agent_run_id, "Execution timed out")
                    
                    return f"Error: Agent execution timed out after {timeout} seconds. The agent may be stuck or taking too long to respond."
                
            except ImportError:
                # Fallback if run_agent_background is not available
                logger.error("Background agent execution not available")
                return "Error: Agent execution service unavailable"
            
        except Exception as e:
            logger.error(f"Error executing agent with thread: {str(e)}")
            return f"Error executing agent: {str(e)}"

    async def _get_agent_execution_result(self, agent_run_id: str, thread_id: str, timeout: int = 10) -> str:
        """Get the final result from an agent execution."""
        try:
            client = await self.db.client
            
            # First check if agent run completed successfully
            agent_run_result = await client.table('agent_runs').select('status, completed_at, error_message').eq('id', agent_run_id).execute()
            
            if not agent_run_result.data:
                return "Error: Could not find agent run record"
            
            agent_run = agent_run_result.data[0]
            
            if agent_run['status'] == 'failed':
                error_msg = agent_run.get('error_message', 'Unknown error')
                return f"Agent execution failed: {error_msg}"
            elif agent_run['status'] != 'completed':
                return f"Agent execution incomplete (status: {agent_run['status']})"
            
            # Get the assistant messages from the thread (the agent's responses)
            messages_result = await client.table('messages').select('content, created_at').eq('thread_id', thread_id).eq('type', 'assistant').order('created_at').execute()
            
            if not messages_result.data:
                return "Agent completed but no response messages found"
            
            # Get the last assistant message as the final result
            last_message = messages_result.data[-1]
            try:
                message_content = json.loads(last_message['content'])
                if isinstance(message_content, dict) and 'content' in message_content:
                    result = message_content['content']
                else:
                    result = str(message_content)
            except (json.JSONDecodeError, KeyError):
                result = str(last_message['content'])
            
            # Truncate result if too long
            if len(result) > 2000:
                result = result[:1900] + "\n\n[... response truncated for brevity ...]"
            
            return f"Agent execution completed successfully:\n\n{result}"
            
        except Exception as e:
            logger.error(f"Error getting agent execution result: {str(e)}")
            return f"Error retrieving agent result: {str(e)}"

    async def _mark_agent_run_as_failed(self, agent_run_id: str, error_message: str) -> None:
        """Mark an agent run as failed with an error message."""
        try:
            client = await self.db.client
            await client.table('agent_runs').update({
                'status': 'failed',
                'error_message': error_message,
                'completed_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', agent_run_id).execute()
            
            logger.info(f"Marked agent run {agent_run_id} as failed: {error_message}")
        except Exception as e:
            logger.error(f"Error marking agent run as failed: {str(e)}")

    async def cleanup_stuck_agent_run(self, agent_run_id: str) -> bool:
        """Clean up a stuck agent run by marking it as failed and cancelling any background tasks."""
        try:
            client = await self.db.client
            
            # Check if agent run exists and is still running
            agent_run_result = await client.table('agent_runs').select('status, thread_id').eq('id', agent_run_id).execute()
            
            if not agent_run_result.data:
                logger.warning(f"Agent run {agent_run_id} not found for cleanup")
                return False
            
            agent_run = agent_run_result.data[0]
            
            if agent_run['status'] in ['completed', 'failed']:
                logger.info(f"Agent run {agent_run_id} already finished with status: {agent_run['status']}")
                return True
            
            # Mark as failed due to being stuck
            await self._mark_agent_run_as_failed(agent_run_id, "Agent run was stuck and cleaned up")
            
            # Try to cancel any Redis streams or background tasks
            try:
                # You could add Redis cleanup here if needed
                pass
            except Exception as e:
                logger.warning(f"Could not clean up Redis streams for {agent_run_id}: {str(e)}")
            
            logger.info(f"Successfully cleaned up stuck agent run {agent_run_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up stuck agent run {agent_run_id}: {str(e)}")
            return False

    @classmethod
    async def cleanup_stuck_agent_runs_by_timeout(cls, account_id: str, timeout_minutes: int = 30) -> int:
        """Class method to clean up all agent runs that have been stuck for more than the specified timeout."""
        try:
            from services.supabase import DBConnection
            db = DBConnection()
            client = await db.client
            
            # Calculate cutoff time
            cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)
            cutoff_time_str = cutoff_time.isoformat()
            
            # Find stuck agent runs (running for too long)
            stuck_runs_result = await client.table('agent_runs').select('id, agent_id, thread_id, started_at').eq('account_id', account_id).eq('status', 'running').lt('started_at', cutoff_time_str).execute()
            
            if not stuck_runs_result.data:
                logger.info(f"No stuck agent runs found for account {account_id}")
                return 0
            
            cleanup_count = 0
            for run in stuck_runs_result.data:
                try:
                    # Mark as failed due to timeout
                    await client.table('agent_runs').update({
                        'status': 'failed',
                        'error_message': f'Agent run timed out after {timeout_minutes} minutes',
                        'completed_at': datetime.now(timezone.utc).isoformat()
                    }).eq('id', run['id']).execute()
                    
                    cleanup_count += 1
                    logger.info(f"Cleaned up stuck agent run {run['id']} (agent: {run['agent_id']})")
                    
                except Exception as e:
                    logger.error(f"Failed to clean up stuck agent run {run['id']}: {str(e)}")
            
            logger.info(f"Cleaned up {cleanup_count} stuck agent runs for account {account_id}")
            return cleanup_count
            
        except Exception as e:
            logger.error(f"Error during bulk cleanup of stuck agent runs: {str(e)}")
            return 0

    async def _verify_agent_access(self, agent_id: str):
        """Verify account has access to the agent."""
        try:
            client = await self.db.client
            result = await client.table('agents').select('agent_id').eq('agent_id', agent_id).eq('account_id', self.account_id).execute()
            
            if not result.data:
                raise ValueError("Agent not found or access denied")
        except ValueError:
            # Re-raise ValueError for proper error messages
            raise
        except Exception as e:
            logger.error(f"Database error in verify_agent_access: {str(e)}")
            raise ValueError("Database connection error")