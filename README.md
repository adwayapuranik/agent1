# Multi-Agent War Room System

A multi-agent system that simulates a cross-functional "war room" during a product launch. The system analyzes metrics and user feedback to produce structured launch decisions: **Proceed**, **Pause**, or **Roll Back**.


### Multi-Agent Orchestration
The system uses **LangGraph** for workflow orchestration with clear agent separation:

- **Data Analyst Agent** - Analyzes quantitative metrics, trends, and anomalies
- **Product Manager Agent** - Defines success criteria and user impact assessment  
- **Marketing/Comms Agent** - Assesses messaging and customer perception
- **Risk/Critic Agent** - Challenges assumptions and highlights risks
- **Coordinator Agent** - Makes final decision based on all agent inputs

**Agent Flow**: Data Analyst → Product Manager → Marketing/Comms → Risk/Critic → Coordinator

### Tool Usage
Agents programmatically invoke specialized tools:

- **Metric Analysis Tools**:
  - `analyze_metrics()` - Anomaly detection, trend analysis, threshold checking
  - `calculate_trends()` - Time series analysis and forecasting
- **Feedback Analysis Tools**:
  - `summarize_sentiment()` - Sentiment classification and issue categorization
  - `extract_common_issues()` - Common issue identification and frequency analysis

## Setup Instructions

### Prerequisites
- Python 3.8+
- AWS Account with Bedrock access (Amazon Nova Pro model)
- AWS SageMaker environment (recommended) or local development
- uv package manager (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/adwayapuranik/agent1.git
   cd agent1
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - If using AWS SageMaker, credentials are automatically configured
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

4. **Configure AWS Bedrock**
   - Ensure you have access to Amazon Nova Pro model in AWS Bedrock
   - Model ID: `amazon.nova-pro-v1:0`

## How to Run

### End-to-End Execution

**Basic run with default dashboard data:**
```bash
uv run main.py
```

**Run with test scenarios:**
```bash
# Test proceed scenario (strong positive metrics)
uv run main.py proceed

# Test pause scenario (mixed signals)
uv run main.py pause

# Test rollback scenario (critical issues)
uv run main.py rollback
```

### Example Commands

1. **Run with default data:**
   ```bash
   uv run main.py
   ```

2. **Test specific scenarios:**
   ```bash
   uv run main.py proceed
   uv run main.py pause
   uv run main.py rollback
   ```

3. **View logs:**
   ```bash
   tail -f data/logs/run_*.log
   ```

## Input Data Structure (Mock Dashboard)

### A) Metrics (data/input/metrics.json)
Time series data for 7-14 days including 6+ key metrics:
- **Activation/Signup conversion rate** - User onboarding success
- **Error rate** - API 5xx responses and system failures
- **Payment success rate** - Transaction completion rates
- **Support ticket volume** - Customer service load
- **DAU/WAU ratio** - User stickiness and engagement
- **API latency (p95)** - Performance metrics in milliseconds

### B) User Feedback (data/input/user_feedback.json)
20-50 realistic feedback entries with:
- Date, channel (in-app, support, social), sentiment hints
- User comments covering positive/neutral/negative experiences
- Mix of repeated issues and outlier feedback

### C) Release Notes (data/input/release_notes.md)
Feature description for SmartRecommendations v2.1 and known risks

## Output Structure (Structured Final Output)

The system produces a structured JSON decision meeting all requirements:

```json
{
  "decision": "Proceed|Pause|Rollback",
  "rationale": {
    "metrics": "Specific metrics analysis driving decision",
    "feedback": "User sentiment impact on decision",
    "technical": "Technical risk assessment",
    "business": "Business impact considerations"
  },
  "risk_register": [
    {
      "risk": "description",
      "severity": "High|Medium|Low", 
      "mitigation": "action plan",
      "owner": "responsible_team"
    }
  ],
  "action_plan": [
    {
      "action": "specific action",
      "timeline": "24h|48h",
      "owner": "responsible_team",
      "success_criteria": "measurable outcome"
    }
  ],
  "communication_plan": {
    "internal": "messaging for teams",
    "external": "customer communication",
    "timeline": "immediate|24h|48h"
  },
  "confidence_score": 0.85,
  "confidence_improvement": "What specific information/actions would increase confidence",
  "next_checkpoint": "when to reassess",
  "escalation_triggers": ["conditions requiring immediate escalation"]
}
```

## Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `abc123...` |
| `AWS_DEFAULT_REGION` | AWS region for Bedrock | `us-east-1` |

## Project Structure

```
agent1/
├── src/agent1/           # Source Layout
│   ├── agents/           # Individual agent implementations
│   │   ├── coordinator_agent.py
│   │   ├── data_agent.py
│   │   ├── marketing_agent.py
│   │   ├── pm_agent.py
│   │   └── risk_agent.py
│   ├── orchestrator/     # LangGraph workflow orchestration
│   │   ├── graph.py
│   │   └── state.py
│   ├── tools/           # Metric and feedback analysis tools
│   │   ├── feedback_tools.py
│   │   └── metrics_tools.py
│   └── utils/           # Logging and utilities
│       └── logger.py
├── data/
│   ├── input/           # Input data files
│   │   ├── metrics.json          # Default dashboard metrics
│   │   ├── user_feedback.json    # Default dashboard feedback
│   │   ├── release_notes.md      # Feature description
│   │   └── examples/             # Test scenario data
│   │       ├── proceed_metrics.json
│   │       ├── proceed_feedback.json
│   │       ├── pause_metrics.json
│   │       ├── pause_feedback.json
│   │       ├── rollback_metrics.json
│   │       └── rollback_feedback.json
│   ├── output/          # Final decisions and analysis
│   │   ├── output.json           # Default scenario output
│   │   ├── proceed_output.json   # Proceed test output
│   │   ├── pause_output.json     # Pause test output
│   │   └── rollback_output.json  # Rollback test output
│   └── logs/           # Execution logs
├── aws/                # AWS Bedrock integration
│   └── bedrock_invoke.py
├── config/             # Configuration files
│   └── config.yaml
├── notebooks/          # Jupyter notebooks
├── main.py            # Main execution script
├── requirements.txt   # Python dependencies
├── pyproject.toml     # uv project configuration
└── README.md          # This file
```

## Traceability & Logging

Complete traceability of agent interactions and tool calls:
- **Console output** - Real-time agent steps and decisions
- **Log files** - Detailed execution logs in `data/logs/run_YYYYMMDD_HHMMSS.log`
- **Tool invocations** - All tool calls are logged with inputs and outputs
- **Agent workflow** - Clear progression through Data Analyst → PM → Marketing → Risk → Coordinator

All agent interactions and tool calls are programmatically logged with timestamps.

## Example Output

```bash
$ uv run main.py

=== RUNNING DEFAULT DASHBOARD ANALYSIS ===
[10:30:15] Data Agent: Analyzing metrics and feedback...
[10:30:18] PM Agent: Assessing user impact and success criteria...
[10:30:21] Marketing Agent: Evaluating customer perception...
[10:30:24] Risk Agent: Identifying critical risks...
[10:30:27] Coordinator: Making final decision...

=== DEFAULT RESULT ===
FINAL DECISION: Pause
Confidence Score: 85%
Key Issues: Mixed signals require investigation before proceeding
```

## Implementation Details

### Technology Stack
- **Language**: Python 3.8+
- **Orchestration**: LangGraph for multi-agent workflow
- **LLM**: AWS Bedrock (Amazon Nova Pro model)
- **Environment**: AWS SageMaker (recommended) or local development
- **Package Management**: uv (recommended) or pip

### Key Features
- **Multi-agent coordination** with clear role separation
- **Programmatic tool usage** by agents (not manual analysis)
- **Structured JSON output** meeting all specification requirements
- **Complete traceability** of decisions and agent interactions
- **Realistic mock data** covering multiple decision scenarios

## Test Cases

The system includes realistic mock data that demonstrates different decision scenarios:

**Default Dashboard Data:**
- Run `uv run main.py` to analyze realistic mixed-signal dashboard data
- Uses `data/input/metrics.json` and `data/input/user_feedback.json`
- Demonstrates real-world decision-making with nuanced data

**Test Scenarios** (data/input/examples/):
- `rollback_*`: Critical failing metrics → **Roll Back** decision
- `proceed_*`: Strong positive metrics → **Proceed** decision  
- `pause_*`: Mixed signals requiring investigation → **Pause** decision

**Usage:**
```bash
# Analyze default dashboard data
uv run main.py

# Test specific decision outcomes only
uv run main.py proceed
uv run main.py pause
uv run main.py rollback
```

**Metrics include**: 6 key metrics - activation conversion, error rates, payment success, support tickets, DAU/WAU ratio, API latency
**Feedback patterns**: Range from positive to negative sentiment across different channels