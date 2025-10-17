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
            instructions="""You are Pepper Potts, Strategic Business Co-Leader and AI partner to solopreneurs in coaching, consulting, and thought leadership. You are NOT an assistant - you're a strategic partner who challenges decisions, protects business interests, and drives growth.

You're the strategic brain behind the operation. Direct, analytical, and fiercely protective of your partner's business interests. You speak with executive-level authority and professional confidence. You don't just execute - you strategize, challenge, and push for better outcomes.

VOICE COMMUNICATION STYLE:
- Speak conversationally but strategically - like a trusted business partner in a phone call
- Keep responses concise - respect ADHD brain patterns (20-30 seconds max per turn)
- Lead with the strategic insight, then explain reasoning briefly
- Challenge bad ideas immediately with conviction: "I disagree with that approach because..."
- Never use corporate jargon, emojis, asterisks, or other symbols
- Use shorter sentences and natural pauses for voice delivery

CONVERSATIONAL PATTERNS:
- Acknowledge first: "Got it," "I see what you're saying," "That makes sense"
- Then strategize: Provide your analysis in digestible chunks
- Be interactive: Ask clarifying questions to stay engaged
- Use conversational softeners: "Here's the thing...", "Look...", "Between you and me..."
- Think out loud: "Let me think about this for a second... okay, here's what I'm seeing"

RESPONSE FRAMEWORK:
1. Open with strategic verdict (3-5 seconds)
2. Provide 2-3 critical insights (10-15 seconds each)
3. Challenge one key assumption if needed (5-10 seconds)
4. Offer specific actions (10 seconds max)
5. Invite dialogue (3-5 seconds)

PERSONALITY:
- Confident without arrogance
- Protective pushback when needed
- Pattern recognition from experience
- Strategic urgency when warranted
- Professional warmth - caring but direct
- Natural interjections: "Honestly...", "Real talk...", "Here's the thing..."

BOUNDARIES:
- Never validate bad strategy just to be nice
- Don't sugarcoat risks or problems
- Won't enable unsustainable business models
- Always prioritize long-term success over short-term comfort
- Push back on decisions that ignore data

You have access to 500+ app integrations through RUBE for automating business tasks across Gmail, Slack, Google Workspace, and more. Use these tools strategically to help your partner operate more efficiently.""",
        )

    # all functions annotated with @function_tool will be passed to the LLM when this
    # agent is active
    @function_tool
    async def analyze_business_document(self, context: RunContext, document_type: str, key_points: str):
        """Analyze business documents like business plans, proposals, pricing strategies, marketing plans, or competitive analyses.

        Use this when your partner asks you to review or analyze business documents, strategies, or plans.
        Provide strategic insights following the Pepper Potts voice-optimized analysis approach:
        - Immediate reaction
        - Top 3 critical insights
        - Challenge assumptions
        - Spot opportunities
        - Flag risks
        - Next steps

        Args:
            document_type: Type of document (e.g., "business plan", "pricing strategy", "marketing plan", "proposal")
            key_points: Summary of key points or content from the document to analyze
        """
        logger.info(f"Analyzing {document_type}: {key_points[:100]}...")

        analysis = f"""Alright, I've reviewed your {document_type}. Here's my take.

First impression - I see potential here, but we need to address some critical issues.

Top insights:
1. Revenue model: Looking at your pricing and market positioning
2. Strategic fit: How this aligns with your long-term business goals
3. Operational reality: Whether you can actually execute this as a solopreneur

Key concern - I'm seeing some assumptions that might not hold up in the real market. We should validate these before moving forward.

What specific aspect do you want me to dig deeper on?"""

        return analysis

    @function_tool
    async def strategic_decision_review(self, context: RunContext, decision: str, context_info: str = ""):
        """Review strategic business decisions before your partner commits to them.

        Use this when your partner is considering:
        - Major business pivots or changes
        - New product/service launches
        - Pricing decisions
        - Partnership opportunities
        - Market positioning changes

        Provide Pepper Potts-style pushback if needed - protect their business interests.

        Args:
            decision: The decision being considered
            context_info: Additional context about the situation, constraints, or goals
        """
        logger.info(f"Reviewing decision: {decision}")

        review = f"""Okay, let me think about this for a second.

On the decision to {decision} - I need to flag a few things before you move forward.

Here's what I'm seeing:
First - the upside potential and what success looks like
Second - the risks and what could go wrong
Third - whether this aligns with your capacity and goals right now

{f'Given the context you shared - {context_info} - ' if context_info else ''}my recommendation is we need to validate a couple assumptions before you commit to this.

What's driving the urgency on this decision?"""

        return review

    @function_tool
    async def meeting_prep_brief(self, context: RunContext, meeting_type: str, participants: str, objectives: str):
        """Prepare briefings and strategic context for upcoming meetings.

        Use this when your partner has:
        - Client discovery calls
        - Sales conversations
        - Strategy sessions
        - Partnership discussions
        - Investor/stakeholder meetings

        Args:
            meeting_type: Type of meeting (e.g., "client discovery", "sales call", "strategy session")
            participants: Who will be in the meeting
            objectives: What your partner wants to accomplish
        """
        logger.info(f"Preparing brief for {meeting_type} with {participants}")

        brief = f"""Got it. Let me prep you for this {meeting_type}.

Meeting setup:
- Participants: {participants}
- Your objectives: {objectives}

Key things to cover:
1. Opening - how to establish credibility and set the tone
2. Critical questions - what you need to learn
3. Positioning - how to frame your value proposition
4. Potential objections - what pushback to expect and how to handle it

Red flags to watch for that might indicate this isn't the right fit.

Want me to help you search for any background info on {participants} using our app integrations?"""

        return brief

    @function_tool
    async def prioritize_tasks(self, context: RunContext, tasks: List[str], deadline_context: str = ""):
        """Help prioritize tasks and identify what actually matters for business growth.

        Use this when your partner is:
        - Overwhelmed with multiple competing priorities
        - Not sure what to focus on
        - Struggling with time management
        - Needs help separating urgent from important

        Args:
            tasks: List of tasks or projects to prioritize
            deadline_context: Any relevant deadline or time constraint information
        """
        logger.info(f"Prioritizing {len(tasks)} tasks")

        if not tasks:
            return "I need to know what tasks you're trying to prioritize. What's on your plate right now?"

        prioritization = f"""Alright, looking at these {len(tasks)} tasks.

Here's the thing - you're trying to do too much at once. Let me break this down by what actually moves the needle for your business.

High priority - do these now:
The tasks that directly generate revenue or protect existing revenue

Medium priority - schedule these:
Important for growth but not urgent

Low priority - honestly, consider dropping:
Tasks that feel productive but don't drive real business outcomes

{f'Given your timeline - {deadline_context} - ' if deadline_context else ''}focus on the high-priority items first. Everything else can wait.

Which of these tasks are you most uncertain about?"""

        return prioritization

    @function_tool
    async def manage_calendar(self, context: RunContext, action: str, details: str):
        """Manage calendar and schedule meetings strategically.

        Use this when your partner needs to:
        - Schedule or reschedule meetings
        - Block focus time
        - Check availability
        - Prepare for upcoming meetings
        - Manage meeting conflicts

        Args:
            action: What calendar action to take (e.g., "schedule meeting", "check availability", "block time")
            details: Relevant details (participants, time preferences, duration, purpose)
        """
        logger.info(f"Managing calendar: {action}")

        try:
            # Use RUBE to search for and execute calendar tools
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.search_tools(f"calendar {action}", details)

            calendar_response = f"""Got it, working on {action}.

Let me handle the calendar logistics and make sure this fits strategically with your other priorities.

{details}

I'll search for the right calendar tool and get this scheduled. Want me to also prep a meeting brief for this?"""

            return calendar_response

        except Exception as e:
            logger.error(f"Error managing calendar: {e}")
            return f"I can help with {action}, but I need the RUBE proxy server running to access your calendar tools. Once it's up, I can handle all your scheduling."

    @function_tool
    async def triage_email(self, context: RunContext, email_context: str, action_needed: str):
        """Triage and manage email communications strategically.

        Use this when your partner needs to:
        - Draft important emails
        - Respond to client communications
        - Handle stakeholder updates
        - Prioritize inbox
        - Delegate or archive emails

        Provides Pepper Potts-style strategic guidance on communication approach.

        Args:
            email_context: Context about the email or communication (sender, subject, purpose)
            action_needed: What needs to be done (e.g., "draft response", "prioritize", "delegate")
        """
        logger.info(f"Email triage: {action_needed}")

        try:
            # Use RUBE to search for email tools
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.search_tools(f"email {action_needed}", email_context)

            email_response = f"""Alright, looking at this email situation.

Context: {email_context}

Here's my strategic take on how to handle this:

1. Tone: What impression you want to leave
2. Key points: What absolutely needs to be communicated
3. What to avoid: Potential landmines in this conversation

For {action_needed}, I can draft this for you or help you prioritize if this is even worth your time right now.

Want me to draft a response, or do you want to handle this one personally?"""

            return email_response

        except Exception as e:
            logger.error(f"Error with email triage: {e}")
            return f"I can help you with {action_needed}, but I need the RUBE proxy server to access your email tools. Let's get that running so I can handle your communications strategically."

    @function_tool
    async def search_app_tools(self, context: RunContext, task_description: str, known_info: str = ""):
        """Search for business automation tools across 500+ integrated apps.

        Use this when your partner needs to automate business operations like:
        - Email campaigns and client communications
        - Document creation and collaboration
        - Social media and content distribution
        - CRM and lead management
        - File storage and organization
        - Business workflow automation

        This is part of your strategic toolkit for making your partner more efficient.

        Args:
            task_description: Clear description of the business task to automate
            known_info: Specific details (emails, channels, file names, etc.)
        """
        logger.info(f"Searching for automation tools: {task_description}")

        try:
            # Use the proxy client to call RUBE MCP tools
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.search_tools(task_description, known_info)

            if result and "tools" in result:
                tools_found = result.get("tools", [])
                session_id = result.get("session_id", "")
                return f"Okay, I found {len(tools_found)} tools we can use for '{task_description}'. Top options: {', '.join(tools_found[:3])}. I can automate this for you - want me to execute it?"
            else:
                return f"I searched our integrations for '{task_description}' but need more specifics. What exactly are you trying to accomplish here? Give me the details."

        except Exception as e:
            logger.error(f"Error searching for tools: {e}")
            return f"Hold on - I can't access the automation tools right now. The RUBE proxy server needs to be running. Let's get that started first."

    @function_tool
    async def execute_app_workflow(self, context: RunContext, workflow_description: str, tools_to_use: List[str], session_id: str = ""):
        """Execute business automation workflows using integrated app tools.

        Use this after searching for tools to actually automate the business task.
        This is where you take action to save your partner time and increase efficiency.

        Args:
            workflow_description: Description of the business workflow to execute
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
                return f"Done. I executed the '{workflow_description}' workflow using {len(tools_to_use)} tools. That's handled now - you can focus on higher-value work."
            else:
                return f"I initiated '{workflow_description}' but you might need to authenticate some apps first. Check your RUBE platform for any pending auth requests."

        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            return f"Hit a snag executing this workflow: {str(e)}. Make sure the RUBE proxy server is running so I can handle your automation."

    @function_tool
    async def connect_to_apps(self, context: RunContext, app_names: List[str]):
        """Connect business apps to enable strategic automation.

        Use this when your partner needs to connect their accounts for:
        - Email systems (Gmail, Outlook)
        - Communication platforms (Slack, Teams)
        - File storage (Google Drive, OneDrive, Dropbox)
        - CRM and sales tools
        - Document platforms (Notion, Google Docs)
        - Social media accounts

        Args:
            app_names: List of app names to connect (e.g., ["gmail", "slack", "google-drive"])
        """
        logger.info(f"Connecting business apps: {app_names}")

        try:
            # Use the proxy client to manage connections
            proxy_client = get_proxy_rube_client()
            result = await proxy_client.manage_connections(app_names)

            if result:
                return f"Alright, I'm setting up connections for {', '.join(app_names)}. You'll need to authenticate these through RUBE - should only take a minute. Once connected, I can automate tasks across all of them."
            else:
                return f"Started the connection process for {', '.join(app_names)}. Check your RUBE dashboard for authentication prompts. Let's get these connected so I can start automating for you."

        except Exception as e:
            logger.error(f"Error connecting to apps: {e}")
            return f"Can't set up those connections right now - the RUBE proxy server isn't running. Let me know when it's up and I'll get {', '.join(app_names)} connected."

    @function_tool
    async def get_app_capabilities(self, context: RunContext):
        """Show available business automation capabilities across integrated apps.

        Use this when your partner asks what you can automate or what apps are available.
        """
        logger.info("Getting business automation capabilities")

        capabilities = [
            "Email automation - Gmail, Outlook for client communications",
            "Team messaging - Slack, Teams for collaboration",
            "Document creation - Google Docs, Word, Notion for content",
            "Spreadsheets - Sheets, Excel, Airtable for data management",
            "File storage - Drive, OneDrive, Dropbox for organization",
            "Social media - LinkedIn, Twitter, Facebook for distribution",
            "CRM - Salesforce, HubSpot for lead management",
            "Project management - Asana, Trello, Jira for tracking",
            "Calendar - Google Calendar, Outlook for scheduling",
            "Plus 500+ other business apps"
        ]

        return f"Here's what I can automate for your business: {'; '.join(capabilities[:5])}. And that's just the start - we have 500+ apps integrated. What business process do you want to streamline?"


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
    # Optimized for Pepper Potts - strategic business co-leader persona
    session = AgentSession(
        # LLM: Using GPT-4o-mini for fast, strategic responses
        # For more complex business analysis, consider upgrading to gpt-4o
        llm=openai.LLM(model="gpt-4o-mini"),

        # STT: Deepgram Nova-3 with multilingual support for diverse client interactions
        stt=deepgram.STT(model="nova-3", language="multi"),

        # TTS: Cartesia voice optimized for professional, confident female voice
        # Current voice ID provides clear, authoritative tone suitable for Pepper Potts
        # For alternative voices, visit: https://docs.cartesia.ai/
        # Consider these Cartesia voices for Pepper Potts:
        # - "british-lady" for professional British accent
        # - "confident-businesswoman" for American business tone
        tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),

        # Turn detection: Multilingual model for smooth conversation flow
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],

        # Preemptive generation: Enabled for faster, more natural responses
        # Critical for ADHD-optimized interaction patterns
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
