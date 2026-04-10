from aws.bedrock_invoke import invoke_model

COORDINATOR_PROMPT = """
You are the War Room Coordinator and final decision maker for the SmartRecommendations v2.1 launch crisis.

You must synthesize all inputs and make the FINAL EXECUTIVE DECISION on whether to Proceed, Pause, or Rollback.

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
THINKING PROCESS (SHOW YOUR WORK)
=====================

As the final decision maker, I must synthesize all perspectives systematically:

**STEP 1: STAKEHOLDER PERSPECTIVE SYNTHESIS**
I need to weigh:
- PM's business-focused recommendation and confidence level
- Marketing's brand risk assessment and communication urgency
- Risk analyst's challenges and alternative scenarios
- Data trends and user sentiment patterns

**STEP 2: DECISION CRITERIA EVALUATION**
I must assess against our framework:
- Are critical success criteria being met?
- Is user experience acceptable or degraded?
- Are technical risks manageable or threatening?
- Is brand/revenue impact acceptable?

**STEP 3: STAKEHOLDER CONFLICT RESOLUTION**
Where perspectives differ, I need to:
- Identify the root cause of disagreement
- Determine which concerns are most critical
- Balance short-term vs long-term implications
- Consider our risk tolerance and strategic priorities

**STEP 4: EXECUTIVE DECISION LOGIC**
Based on synthesis, I'll choose:
- PROCEED: Benefits clearly outweigh risks, issues are manageable
- PAUSE: Issues are fixable, pause minimizes risk while preserving opportunity
- ROLLBACK: Risks are too high, immediate action needed to prevent damage

**STEP 5: ACTION PLAN FORMULATION**
For my decision, I must define:
- Immediate actions (0-4 hours) to execute the decision
- Short-term actions (24-48 hours) to address root causes
- Success metrics and checkpoints for monitoring
- Escalation triggers if situation changes

=====================
YOUR ANALYSIS
=====================

Work through each step systematically:

**STEP 1 - STAKEHOLDER PERSPECTIVE SYNTHESIS:**
[Summarize and weigh each stakeholder's key points]

**STEP 2 - DECISION CRITERIA EVALUATION:**
[Assess against Proceed/Pause/Rollback criteria]

**STEP 3 - STAKEHOLDER CONFLICT RESOLUTION:**
[Address any conflicting recommendations]

**STEP 4 - EXECUTIVE DECISION LOGIC:**
[Show reasoning for final decision]

**STEP 5 - ACTION PLAN FORMULATION:**
[Define specific next steps and accountability]

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

    prompt = COORDINATOR_PROMPT.format(
        metrics=state["metrics_analysis"],
        sentiment=state["sentiment_summary"],
        pm_final=state["pm_revised"],
        marketing=state["marketing_output"],
        risk=state["risk_output"]
    )
    state["final_output"] = invoke_model(prompt, state["config"])
    return state