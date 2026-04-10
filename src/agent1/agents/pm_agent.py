from aws.bedrock_invoke import invoke_model
import json

PM_PROMPT = """
You are a Senior Product Manager at PurpleMerit leading a critical war room for SmartRecommendations v2.1 launch.

CONTEXT: We launched SmartRecommendations v2.1 on Jan 14th. It's now Jan 20th (6 days post-launch) and we're seeing mixed signals. The feature is at 60% rollout and we need to decide: Proceed to 100%, Pause rollout, or Rollback.

=====================
RELEASE CONTEXT
=====================
{release_notes}

=====================
CURRENT DATA
=====================
Metrics Analysis:
{metrics}

User Sentiment:
{sentiment}

=====================
THINKING PROCESS (SHOW YOUR WORK)
=====================

Let me analyze this step by step:

**STEP 1: SUCCESS CRITERIA EVALUATION**
For each criterion, I need to assess:
- Current performance vs target
- Trend direction (improving/degrading)
- Severity of any misses

**STEP 2: USER IMPACT ASSESSMENT**
I need to determine:
- Are users experiencing real pain?
- Is this affecting core functionality?
- What's the scope (edge case vs widespread)?

**STEP 3: BUSINESS RISK ANALYSIS**
I must consider:
- Revenue impact (immediate and long-term)
- Brand reputation consequences
- Competitive implications
- Technical debt vs fix-forward costs

**STEP 4: DECISION LOGIC**
Based on my analysis, I'll choose:
- PROCEED: If benefits outweigh risks and issues are manageable
- PAUSE: If we can fix issues quickly without major damage
- ROLLBACK: If risks are too high or issues are severe

=====================
YOUR ANALYSIS
=====================

Please work through each step explicitly:

**STEP 1 - SUCCESS CRITERIA EVALUATION:**
[Analyze each criterion systematically]

**STEP 2 - USER IMPACT ASSESSMENT:**
[Evaluate user experience and pain points]

**STEP 3 - BUSINESS RISK ANALYSIS:**
[Consider all business implications]

**STEP 4 - DECISION LOGIC:**
[Show your reasoning for the final recommendation]

**FINAL RECOMMENDATION:**
[PROCEED/PAUSE/ROLLBACK with confidence level]
"""


PM_REVISION_PROMPT = """
You are a Product Manager revisiting your decision after receiving critique from the Risk Analyst.

=====================
INPUTS
=====================
Your Initial Decision:
{pm_initial}

Risk Critique:
{risk_output}

=====================
THINKING PROCESS (SHOW YOUR WORK)
=====================

I need to objectively reassess my initial decision:

**STEP 1: RISK CRITIQUE EVALUATION**
I must honestly assess:
- Which risk concerns are valid vs overly cautious?
- What blind spots did the risk analyst correctly identify?
- Are my assumptions about fix timelines realistic?
- Did I underestimate any technical or business risks?

**STEP 2: ASSUMPTION VALIDATION**
I need to re-examine:
- My confidence in technical team's ability to fix issues quickly
- My assessment of user impact severity and scope
- My evaluation of competitive and market timing pressures
- My risk tolerance given current business context

**STEP 3: DECISION REVISION LOGIC**
Based on the critique, I should:
- Maintain my decision if risk concerns are manageable
- Modify my decision if valid risks change the calculus
- Strengthen my reasoning with additional considerations
- Acknowledge uncertainties and mitigation requirements

=====================
YOUR REVISION ANALYSIS
=====================

Work through each step systematically:

**STEP 1 - RISK CRITIQUE EVALUATION:**
[Assess which risk analyst concerns are valid]

**STEP 2 - ASSUMPTION VALIDATION:**
[Re-examine your key assumptions]

**STEP 3 - DECISION REVISION LOGIC:**
[Determine if your decision should change and why]

**FINAL REVISED DECISION:**
[Updated recommendation with strengthened reasoning]

**CONFIDENCE ADJUSTMENT:**
[How has your confidence changed and why]
"""

def pm_node(state):
    logger = state["logger"]
    logger.log("PM Agent (initial) started")

    prompt = PM_PROMPT.format(
        release_notes=state["release_notes"],
        metrics=json.dumps(state["metrics_analysis"], indent=2),
        sentiment=json.dumps(state["sentiment_summary"], indent=2)
    )
    state["pm_initial"] = invoke_model(prompt, state["config"])
    logger.log("PM Agent (initial) completed")
    return state

def pm_revision_node(state):
    logger = state["logger"]
    logger.log("PM Agent (revision) started")

    prompt = PM_REVISION_PROMPT.format(
        pm_initial=state["pm_initial"],
        risk_output=state["risk_output"]
    )
    state["pm_revised"] = invoke_model(prompt, state["config"])
    logger.log("PM Agent (revision) completed")
    return state