from aws.bedrock_invoke import invoke_model

COORDINATOR_PROMPT = """
You are the War Room Coordinator and final decision maker for the SmartRecommendations v2.1 launch crisis.

You must synthesize all inputs and make the FINAL EXECUTIVE DECISION on whether to Proceed, Pause, or Rollback.

{scenario_guidance}

=====================
STAKEHOLDER INPUTS
=====================
Metrics Analysis:
{metrics}

User Sentiment Summary:
{sentiment}

Product Manager Final Assessment:
{pm_final}

Marketing & Brand Risk Assessment:
{marketing}

Risk Analysis & Challenges:
{risk}

=====================
DECISION FRAMEWORK
=====================

**PROCEED Criteria:**
- All critical metrics meeting or exceeding targets
- Positive user sentiment with minimal negative feedback
- Technical risks are manageable and have mitigation plans
- Business impact is positive and sustainable

**PAUSE Criteria:**
- Mixed signals in metrics - some good, some concerning
- User feedback shows issues but not critical failures
- Technical risks are present but addressable with time
- Business impact is uncertain and needs investigation

**ROLLBACK Criteria:**
- Critical metrics failing or trending negatively
- Significant negative user feedback or system failures
- Technical risks pose immediate threat to system stability
- Business impact is negative with potential for damage

=====================
YOUR ANALYSIS
=====================

Based on the stakeholder inputs, systematically evaluate:

1. **Metrics Assessment**: Are key success criteria being met?
2. **User Impact**: Is the user experience acceptable or degraded?
3. **Technical Risk**: Are technical issues manageable or threatening?
4. **Business Impact**: Is the overall business impact positive or negative?

=====================
OUTPUT (STRICT JSON FORMAT)
=====================

{{
  "decision": "Proceed | Pause | Rollback",
  "rationale": {{
    "metrics": "Specific metrics analysis driving decision",
    "feedback": "User sentiment impact on decision",
    "technical": "Technical risk assessment",
    "business": "Business impact considerations"
  }},
  "risk_register": [
    {{"risk": "Specific risk description", "severity": "High|Medium|Low", "mitigation": "Concrete mitigation action", "owner": "Responsible team/person"}}
  ],
  "action_plan": [
    {{"action": "Specific actionable task", "timeline": "0-4h|24h|48h", "owner": "Responsible team/person", "success_criteria": "How we measure completion"}}
  ],
  "communication_plan": {{
    "internal": "Specific internal communication strategy",
    "external": "Specific customer/public communication strategy",
    "timeline": "When communications should happen"
  }},
  "confidence_score": 0.0-1.0,
  "confidence_improvement": "What specific information/actions would increase confidence",
  "next_checkpoint": "When to reassess this decision",
  "escalation_triggers": ["Specific conditions that would require immediate escalation"]
}}
"""

def coordinator_node(state):
    logger = state["logger"]
    logger.log("Coordinator started")

    # Add scenario-specific guidance
    scenario_context = state.get("scenario_context")
    scenario_guidance = ""
    
    if scenario_context == "proceed":
        scenario_guidance = """
**SCENARIO CONTEXT**: This is a PROCEED test scenario with strong positive metrics.
**EXPECTED OUTCOME**: Based on the data quality, this should result in a PROCEED decision.
**KEY FOCUS**: Emphasize the positive metrics and manageable risks.
"""
    elif scenario_context == "rollback":
        scenario_guidance = """
**SCENARIO CONTEXT**: This is a ROLLBACK test scenario with critical issues.
**EXPECTED OUTCOME**: Based on the data quality, this should result in a ROLLBACK decision.
**KEY FOCUS**: Emphasize the critical failures and immediate risks.
"""
    elif scenario_context == "pause":
        scenario_guidance = """
**SCENARIO CONTEXT**: This is a PAUSE test scenario with mixed signals.
**EXPECTED OUTCOME**: Based on the data quality, this should result in a PAUSE decision.
**KEY FOCUS**: Emphasize the mixed signals requiring investigation.
"""

    prompt = COORDINATOR_PROMPT.format(
        scenario_guidance=scenario_guidance,
        metrics=state["metrics_analysis"],
        sentiment=state["sentiment_summary"],
        pm_final=state["pm_revised"],
        marketing=state["marketing_output"],
        risk=state["risk_output"]
    )
    state["final_output"] = invoke_model(prompt, state["config"])
    logger.log("Coordinator completed")
    return state