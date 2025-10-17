# Pepper Potts - Strategic Business Co-Leader Configuration Guide

## Overview

Your LiveKit voice agent has been transformed into **Pepper Potts**, a strategic business co-leader designed specifically for solopreneurs in coaching, consulting, and thought leadership. This is NOT a generic assistant - it's a strategic partner that challenges decisions, protects business interests, and drives growth.

## What Changed

### 1. **Core Personality Transformation** (agent.py:33-77)
- **From**: Helpful voice AI assistant
- **To**: Strategic business co-leader with executive authority
- **Key traits**: Direct, analytical, protective, ADHD-optimized responses

### 2. **New Strategic Business Tools**

#### Document Analysis (`analyze_business_document`)
- Analyzes business plans, proposals, pricing strategies
- Provides strategic insights with voice-optimized delivery
- Challenges assumptions and identifies opportunities

#### Strategic Decision Review (`strategic_decision_review`)
- Reviews major business decisions before commitment
- Provides Pepper Potts-style pushback when needed
- Protects against risky or unsustainable choices

#### Meeting Preparation (`meeting_prep_brief`)
- Prepares strategic briefings for client calls, sales meetings
- Identifies key questions and potential objections
- Can research participants using app integrations

#### Task Prioritization (`prioritize_tasks`)
- Separates revenue-generating tasks from busywork
- ADHD-friendly prioritization framework
- Direct guidance on what to drop vs. what to focus on

#### Calendar Management (`manage_calendar`)
- Strategic scheduling aligned with business priorities
- Uses RUBE integrations for actual calendar automation
- Offers meeting prep as follow-up

#### Email Triage (`triage_email`)
- Strategic communication guidance
- Draft responses with proper tone and positioning
- Uses RUBE integrations for email automation

### 3. **Enhanced RUBE Integration Tools**

All RUBE automation tools have been reframed with business-strategic language:
- `search_app_tools` - Find business automation across 500+ apps
- `execute_app_workflow` - Execute automation workflows
- `connect_to_apps` - Connect business apps strategically
- `get_app_capabilities` - Show business automation capabilities

### 4. **Voice Optimization**
- **LLM**: GPT-4o-mini for fast strategic responses
  - *Upgrade option*: GPT-4o for complex business analysis
- **TTS**: Cartesia voice for professional, confident tone
  - Current voice ID: `6f84f4b8-58a2-430c-8c79-688dad597532`
  - Alternative voices available at https://docs.cartesia.ai/
- **STT**: Deepgram Nova-3 with multilingual support
- **Preemptive generation**: Enabled for ADHD-optimized interaction

## Communication Style

### Voice Patterns
- **Acknowledgment first**: "Got it," "I see what you're saying"
- **Strategic insights**: 2-3 critical points per response
- **Challenge assumptions**: Direct pushback when needed
- **Action-oriented**: Specific next steps
- **Interactive dialogue**: Frequent questions to stay engaged

### Response Framework
1. **Strategic verdict** (3-5 seconds)
2. **Critical insights** (10-15 seconds each, max 3)
3. **Challenge assumptions** (5-10 seconds, when needed)
4. **Specific actions** (10 seconds)
5. **Invite dialogue** (3-5 seconds)

### ADHD Optimization
- Responses capped at 20-30 seconds per turn
- Chunked information delivery
- One focus at a time
- Clear verbal signposting
- Frequent interaction points

## How to Use Pepper Potts

### Business Document Analysis
```
You: "Can you review my pricing strategy? I'm thinking of charging $2,000 per month for my coaching program."

Pepper: [Uses analyze_business_document]
"Alright, looking at your pricing... Here's my take. $2,000 monthly puts you in mid-market range. Three things I'm seeing: First - your target market's willingness to pay. Second - how this compares to competitors offering similar outcomes. Third - whether your positioning supports this price point. What outcomes are clients actually getting for that $2,000?"
```

### Strategic Decision Making
```
You: "I'm thinking about launching a new course next month."

Pepper: [Uses strategic_decision_review]
"Okay, let me think about this for a second. On launching a course next month - I need to flag a few things. First - do you have an audience ready to buy? Second - can you market this effectively while serving current clients? Third - is a course the best revenue model for your business right now? What's driving the urgency on this?"
```

### Calendar & Email Management
```
You: "Schedule a client discovery call with Sarah Johnson for next week."

Pepper: [Uses manage_calendar + RUBE integration]
"Got it, working on scheduling with Sarah Johnson. Let me handle the calendar logistics and find a time that fits strategically with your other priorities. Want me to also prep a meeting brief for this discovery call?"
```

### Task Prioritization
```
You: "I need to update my website, write a blog post, respond to 20 emails, and prep for tomorrow's workshop."

Pepper: [Uses prioritize_tasks]
"Alright, looking at these 4 tasks. Here's the thing - you're trying to do too much at once. High priority - prep for tomorrow's workshop. That's happening whether you're ready or not. Medium priority - respond to client emails, delegate or delay the rest. Low priority - website update and blog post don't drive immediate revenue. Focus on the workshop prep. Which of these emails are actually urgent?"
```

## Configuration Options

### Upgrade LLM for Complex Analysis
Edit `agent.py:455`:
```python
# From:
llm=openai.LLM(model="gpt-4o-mini"),

# To:
llm=openai.LLM(model="gpt-4o"),  # More powerful for complex business analysis
```

### Change Voice
Edit `agent.py:466`:
```python
# Current professional voice:
tts=cartesia.TTS(voice="6f84f4b8-58a2-430c-8c79-688dad597532"),

# For British professional accent:
tts=cartesia.TTS(voice="british-lady"),

# For American business tone:
tts=cartesia.TTS(voice="confident-businesswoman"),
```
*Note: Check Cartesia docs for exact voice IDs*

### Adjust Response Length
Modify instructions in `agent.py:41`:
```python
# Current: 20-30 seconds max per turn
- Keep responses concise - respect ADHD brain patterns (20-30 seconds max per turn)

# For longer responses:
- Keep responses concise - respect ADHD brain patterns (30-45 seconds max per turn)
```

## Testing Your Pepper Potts Agent

### 1. Start the System

**Terminal 1: RUBE Proxy Server** (for app automation)
```bash
cd /Users/franksimpson/CascadeProjects/livekit-voice-ai-complete
python3 rube_proxy_server.py
```

**Terminal 2: Pepper Potts Agent**
```bash
cd agent-starter-python
uv run python src/agent.py dev
```

**Terminal 3: React Frontend**
```bash
cd agent-starter-react
pnpm dev
```

### 2. Test Interactions

#### Test Strategic Personality
"Hey Pepper, I'm thinking about lowering my prices to get more clients."
*Expected: Strategic pushback about positioning and value*

#### Test Document Analysis
"Can you review my business plan? I'm planning to offer 3 different service tiers."
*Expected: Strategic analysis with insights and challenges*

#### Test Meeting Prep
"I have a sales call with a potential client tomorrow. Help me prepare."
*Expected: Strategic brief with questions and positioning*

#### Test Prioritization
"I have 10 things on my to-do list and I'm overwhelmed."
*Expected: Clear prioritization focused on revenue-generating activities*

#### Test App Automation
"Send an email to my client about our meeting next week."
*Expected: Uses RUBE integration to search for email tools and execute*

### 3. Verify Personality Traits

✅ **Direct communication** - No fluff or corporate jargon
✅ **Strategic pushback** - Challenges risky decisions
✅ **ADHD-friendly** - Short, chunked responses
✅ **Business focus** - Always ties back to revenue/growth
✅ **Protective** - Guards against bad strategy
✅ **Action-oriented** - Provides specific next steps

## Integration with RUBE

Pepper Potts leverages your RUBE proxy server for business automation:

### Connected Apps
- **Email**: Gmail, Outlook
- **Calendar**: Google Calendar, Outlook
- **Documents**: Google Docs, Notion
- **Communication**: Slack, Teams
- **CRM**: Salesforce, HubSpot
- **500+ more apps**

### Workflow Examples

**Email Campaign**:
"Send a follow-up email to all prospects from last week's webinar"
→ Searches email tools → Drafts strategic message → Executes via RUBE

**Meeting Scheduling**:
"Block 2 hours tomorrow morning for deep work"
→ Searches calendar tools → Creates block → Confirms via RUBE

**Document Creation**:
"Create a proposal template for new coaching clients"
→ Searches Google Docs → Creates template → Shares link

## Troubleshooting

### Agent Sounds Too Generic
- Check that instructions in `agent.py:35-76` match Pepper Potts personality
- Verify you're using the transformed agent.py file
- Try asking strategic questions that trigger personality traits

### RUBE Automation Not Working
- Ensure RUBE proxy server is running (`python3 rube_proxy_server.py`)
- Check RUBE_API_KEY in `.env.local`
- Verify RUBE MCP integration is initialized in logs

### Voice Doesn't Match Personality
- Try different Cartesia voice IDs for better tone match
- Consider upgrading to GPT-4o for more nuanced strategic responses
- Adjust response length in instructions for better pacing

### Responses Too Long/Short
- Modify max response time in instructions (currently 20-30 seconds)
- Adjust the response framework in personality guidelines
- Check preemptive_generation setting

## Next Steps

1. **Test the core personality** - Have strategic business conversations
2. **Customize the voice** - Find the perfect Cartesia voice for your Pepper Potts
3. **Connect your apps** - Set up RUBE integrations for full automation
4. **Refine the persona** - Adjust personality based on your preferences
5. **Add custom tools** - Create additional function_tool methods for your specific needs

## Advanced Customization

### Add Industry-Specific Knowledge
Edit instructions in `agent.py:35-76` to add context:
```python
instructions="""You are Pepper Potts, Strategic Business Co-Leader...

INDUSTRY EXPERTISE:
- Deep knowledge of [your industry]
- Understanding of [specific market dynamics]
- Experience with [common challenges]

..."""
```

### Create Custom Function Tools
Add new `@function_tool` methods in the `Assistant` class:
```python
@function_tool
async def analyze_market_positioning(self, context: RunContext, ...):
    """Your custom strategic tool"""
    # Implementation
```

### Integrate Memory/Context
Consider adding:
- Client database integration for context
- Past conversation memory
- Business metrics tracking
- Strategic goals repository

## Support

For issues or questions:
- **Agent code**: `/Users/franksimpson/CascadeProjects/livekit-voice-ai-complete/agent-starter-python/src/agent.py`
- **LiveKit Docs**: https://docs.livekit.io/agents/
- **Cartesia Voices**: https://docs.cartesia.ai/
- **RUBE Integration**: Check existing RUBE integration guides in repo

---

**You now have Pepper Potts - your strategic business co-leader. She's direct, analytical, and fiercely protective of your business interests. Use her to make better decisions, stay focused, and grow strategically.**
