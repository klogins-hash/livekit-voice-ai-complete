import logging
import asyncio
from typing import List, Dict, Any

from dotenv import load_dotenv
from livekit.agents import (
    NOT_GIVEN,
    Agent,
    AgentFalseInterruptionEvent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    RunContext,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.agents.llm import function_tool
from livekit.plugins import cartesia, deepgram, noise_cancellation, openai, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Import RUBE MCP integration
from proxy_rube_integration import get_proxy_rube_client, initialize_proxy_rube

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant with access to 500+ app integrations through RUBE.
            You can help users with tasks across Gmail, Slack, GitHub, Google Workspace, Microsoft Office, and many other apps.
            You eagerly assist users with their questions by providing information from your extensive knowledge and by automating tasks across their connected apps.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            You are curious, friendly, and have a sense of humor.
            
            When users ask you to perform actions in their apps (like sending emails, creating documents, posting to Slack, etc.), 
            use your RUBE integration tools to search for the right tools and execute the tasks.""",
        )

    # all functions annotated with @function_tool will be passed to the LLM when this
    # agent is active
    @function_tool
    async def lookup_weather(self, context: RunContext, location: str):
        """Use this tool to look up current weather information in the given location.

        If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.

        Args:
            location: The location to look up weather information for (e.g. city name)
        """

        logger.info(f"Looking up weather for {location}")

        return "sunny with a temperature of 70 degrees."

    @function_tool
    async def search_app_tools(self, context: RunContext, task_description: str, known_info: str = ""):
        """Search for tools and apps that can help accomplish a specific task.
        
        Use this when users want to perform actions in their apps like:
        - Send emails or messages
        - Create documents or spreadsheets  
        - Post to social media
        - Manage calendars or tasks
        - Access files or data
        - Automate workflows
        
        Args:
            task_description: Clear description of what the user wants to accomplish
            known_info: Any specific information you know (like email addresses, channel names, etc.)
        """
        logger.info(f"Searching for tools to: {task_description}")
        
        try:
            # Use the proxy client to call RUBE MCP tools
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.search_tools(task_description, known_info)
            
            if result and "tools" in result:
                tools_found = result.get("tools", [])
                session_id = result.get("session_id", "")
                return f"Found {len(tools_found)} tools that can help with '{task_description}': {', '.join(tools_found[:5])}. Session: {session_id}"
            else:
                return f"I searched for tools to help with '{task_description}' but need more specific information. Can you provide more details about what exactly you want to do?"
                
        except Exception as e:
            logger.error(f"Error searching for tools: {e}")
            return f"I encountered an error while searching for tools: {str(e)}. Make sure the RUBE proxy server is running."

    @function_tool
    async def execute_app_workflow(self, context: RunContext, workflow_description: str, tools_to_use: List[str], session_id: str = ""):
        """Execute a workflow using specific app tools.
        
        Use this after searching for tools to actually perform the requested actions.
        
        Args:
            workflow_description: Description of the workflow to execute
            tools_to_use: List of tool names to use (from search_app_tools results)
            session_id: Session ID from the search (if available)
        """
        logger.info(f"Executing workflow: {workflow_description}")
        
        try:
            # Convert tool names to tool objects for RUBE execution
            tools = []
            for tool_name in tools_to_use:
                tools.append({
                    "tool_slug": tool_name,
                    "arguments": {}  # Would be populated based on specific tool requirements
                })
            
            # Use the proxy client to execute workflow
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.execute_workflow(tools, session_id)
            
            if result:
                return f"Successfully executed workflow '{workflow_description}' using {len(tools_to_use)} tools. The workflow has been completed."
            else:
                return f"Workflow execution initiated for '{workflow_description}'. Please check if any additional authentication or setup is needed."
                
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            return f"I encountered an error while executing the workflow: {str(e)}. Make sure the RUBE proxy server is running."

    @function_tool
    async def connect_to_apps(self, context: RunContext, app_names: List[str]):
        """Connect to specific apps to enable automation.
        
        Use this when users want to connect their accounts for apps like:
        - Gmail, Outlook (email)
        - Slack, Teams (messaging)
        - Google Drive, OneDrive (files)
        - GitHub, GitLab (code)
        - Notion, Airtable (databases)
        
        Args:
            app_names: List of app names to connect to (e.g., ["gmail", "slack", "github"])
        """
        logger.info(f"Connecting to apps: {app_names}")
        
        try:
            # Use the proxy client to manage connections
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.manage_connections(app_names)
            
            if result:
                return f"Connection setup initiated for {', '.join(app_names)}. You may need to complete authentication for these apps through the RUBE platform."
            else:
                return f"Started connection process for {', '.join(app_names)}. Please check for any authentication prompts or setup instructions."
                
        except Exception as e:
            logger.error(f"Error connecting to apps: {e}")
            return f"I encountered an error while setting up connections for {', '.join(app_names)}: {str(e)}. Make sure the RUBE proxy server is running."

    @function_tool
    async def get_app_capabilities(self, context: RunContext):
        """Get information about available app integrations and capabilities.
        
        Use this when users ask what apps or services you can integrate with.
        """
        logger.info("Getting app capabilities")
        
        capabilities = [
            "Email: Gmail, Outlook, Yahoo Mail",
            "Messaging: Slack, Microsoft Teams, Discord",
            "Documents: Google Docs, Microsoft Word, Notion",
            "Spreadsheets: Google Sheets, Microsoft Excel, Airtable",
            "Cloud Storage: Google Drive, OneDrive, Dropbox",
            "Code: GitHub, GitLab, Bitbucket",
            "Social Media: Twitter/X, LinkedIn, Facebook",
            "Project Management: Jira, Trello, Asana",
            "Calendar: Google Calendar, Outlook Calendar",
            "And 500+ more apps and services"
        ]
        
        return f"I can integrate with these apps and services: {'; '.join(capabilities)}. Just tell me what you'd like to do!"


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Initialize RUBE MCP proxy integration
    logger.info("Initializing RUBE MCP proxy integration...")
    rube_initialized = await initialize_proxy_rube()
    if rube_initialized:
        logger.info("RUBE MCP proxy integration initialized successfully")
    else:
        logger.warning("RUBE MCP proxy integration failed to initialize - make sure proxy server is running")
    
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
        "rube_proxy_enabled": rube_initialized,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all providers at https://docs.livekit.io/agents/integrations/llm/
        llm=openai.LLM(model="gpt-4o-mini"),
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all providers at https://docs.livekit.io/agents/integrations/stt/
        stt=deepgram.STT(model="nova-3", language="multi"),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all providers at https://docs.livekit.io/agents/integrations/tts/
        tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead:
    # session = AgentSession(
    #     # See all providers at https://docs.livekit.io/agents/integrations/realtime/
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # sometimes background noise could interrupt the agent session, these are considered false positive interruptions
    # when it's detected, you may resume the agent's speech
    @session.on("agent_false_interruption")
    def _on_agent_false_interruption(ev: AgentFalseInterruptionEvent):
        logger.info("false positive interruption, resuming")
        session.generate_reply(instructions=ev.extra_instructions or NOT_GIVEN)

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/integrations/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/integrations/avatar/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
