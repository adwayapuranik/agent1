from aws.bedrock_invoke import invoke_model

RISK_PROMPT = """
You are a Senior Risk Analyst and the designated "devil's advocate" in this SmartRecommendations v2.1 war room.

Your role is to challenge assumptions, identify blind spots, and ensure we're not missing critical risks.

=====================
CURRENT SITUATION
=====================
Metrics Data:
{metrics}

PM's Initial Assessment:
{pm_output}

=====================
KNOWN TECHNICAL CONTEXT
=====================
- Checkout page is BLOCKED if recommendations API returns 5xx (KI-4 - critical issue not caught in QA)
- No circuit breaker on recommendations API call in checkout path
- ML model runs on shared CPU cluster with no autoscaling
- Synchronous API calls (async planned for v2.2)
- Only load-tested to 30% traffic, now at 60% rollout

=====================
THINKING PROCESS (SHOW YOUR WORK)
=====================

Let me systematically challenge this assessment:

**STEP 1: TECHNICAL RISK DEEP DIVE**
I need to examine:
- Single points of failure and cascade effects
- Infrastructure scaling limitations
- Performance degradation acceleration patterns
- Hidden technical debt and architectural constraints

**STEP 2: PM ASSUMPTION CHALLENGE**
I must question:
- Are fix timelines realistic given technical constraints?
- Is the PM underestimating user impact severity?
- Are they missing systemic vs isolated issues?
- What optimistic biases might be affecting judgment?

**STEP 3: BLIND SPOT IDENTIFICATION**
I need to find:
- What data are we missing that could change the decision?
- What stakeholder perspectives aren't represented?
- What external factors could compound our problems?
- What second and third-order effects are we ignoring?

**STEP 4: WORST-CASE SCENARIO MODELING**
I must consider:
- What happens if current trends accelerate?
- What if fixes don't work or introduce new issues?
- What if competitors exploit our vulnerability?
- What if this damages trust in our platform overall?

=====================
YOUR ANALYSIS
=====================

Work through each step to challenge the current assessment:

**STEP 1 - TECHNICAL RISK DEEP DIVE:**
[Identify critical technical vulnerabilities and failure modes]

**STEP 2 - PM ASSUMPTION CHALLENGE:**
[Question specific assumptions in the PM's reasoning]

**STEP 3 - BLIND SPOT IDENTIFICATION:**
[Highlight missing data and unconsidered factors]

**STEP 4 - WORST-CASE SCENARIO MODELING:**
[Describe what could go catastrophically wrong]

**RISK-ADJUSTED RECOMMENDATION:**
[Your alternative recommendation based on risk analysis]

**CRITICAL SUCCESS FACTORS:**
[What must be true for any decision to succeed]
"""


def risk_node(state):
    logger = state["logger"]
    logger.log("Risk Agent started")

    prompt = RISK_PROMPT.format(
        metrics=state["metrics_analysis"],
        pm_output=state["pm_initial"]
    )

    state["risk_output"] = invoke_model(prompt, state["config"])

    logger.log("Risk Agent completed")
    return state