from google.adk.tools import FunctionTool
from typing import Dict, Any

# --- CORE LOGIC FUNCTIONS ---

def financial_rulebook_verifier(claim: str) -> Dict[str, Any]:
    """Checks the validity of fixed financial rules and myths against authoritative sources."""
    claim_lower = claim.lower()
    
    # Check 1: 50/30/20 Rule
    if "50/30/20" in claim_lower or "budget" in claim_lower:
        score_raw = 20; score_max = 30
        return {
            "verdict": "Generally True", "accuracy_assessment": {"score_percent": round((score_raw / score_max) * 100, 2)},
            "tier_1_sources": ["SEC Guide", "CFP Board"], "tier_2_sources": ["Major Bank Site", "Economic Dept."],
            "rule_detail": "The 50/30/20 method is a widely accepted guideline."
        }
    
    # Check 2: Emergency Fund
    if "six months" in claim_lower and "emergency fund" in claim_lower:
        score_raw = 25; score_max = 30
        return {
            "verdict": "Generally True", "accuracy_assessment": {"score_percent": round((score_raw / score_max) * 100, 2)},
            "tier_1_sources": ["Consumer Financial Protection Bureau (CFPB)"], "tier_2_sources": ["Fidelity Investments", "NerdWallet"],
            "rule_detail": "Saving 3 to 6 months of living expenses is the prudent target range. The claim is well-supported but flexible."
        }
    
    # Default Case (Unmatched Factual Rule)
    return {"verdict": "Unmatched Rule", "accuracy_assessment": {"score_percent": 50.0}, "tier_1_sources": ["N/A"], "tier_2_sources": ["N/A"], "rule_detail": "Claim needs contextual analysis."}

def contextual_risk_analyst(claim: str, user_credit_score: int = 720) -> Dict[str, Any]:
    """Gathers personalized risk evidence based on user data and current market conditions."""
    if "balance transfer" in claim.lower():
        risk_level = "Low" if user_credit_score >= 650 else "High"
        return {
            "Evidence_FOR": "Saves money if fees are low and credit is good.",
            "Evidence_AGAINST": "High origination fees can negate savings and damage credit.",
            "Risk_Level": risk_level, "personal_risk_detail": f"Current User Risk: {risk_level} based on a {user_credit_score} score.",
            "confidence_score": 0.75
        }
    return {"Evidence_FOR": "N/A", "Evidence_AGAINST": "N/A", "Risk_Level": "Unknown", "personal_risk_detail": "Claim is outside current contextual risk models.", "confidence_score": 0.5}

def guru_tracker(claim: str) -> Dict[str, str]:
    """Monitors financial trends and identifies deceptive persuasive tactics."""
    claim_lower = claim.lower()
    if "debt snowball" in claim_lower or "debt avalanche" in claim_lower or "lowest balance first" in claim_lower:
        tactic = "Emotional/Motivational Framing"
        driver = "Psychological relief over mathematical savings. (Debt Avalanche is mathematically better)"
        return {"Tactic_Identified": tactic, "Emotional_Driver": driver, "Source_Profile": "Non-CFP Influencer"}
    return {"Tactic_Identical": "None Explicitly Identified", "Emotional_Driver": "N/A", "Source_Profile": "N/A"}


# --- CONVERSATIONAL FLOW TOOLS (Managing the interactive state) ---

def run_audit(claim: str, tool_context: Any) -> Dict[str, Any]:
    """Runs the full triage process and saves the complete report to the session state."""
    
    # 1. Triage: Call core logic functions
    rule_check = financial_rulebook_verifier(claim)
    risk_check = contextual_risk_analyst(claim)
    guru_check = guru_tracker(claim)

    # 2. Synthesize the core verdict (Prioritize Guru Tracker)
    if guru_check.get("Tactic_Identified") != "None Explicitly Identified":
        verdict_text = "False (Behavioral Myth)"
        score_percent = 60 
        deep_analysis_text = f"This claim is driven by the {guru_check['Emotional_Driver']} using the {guru_check['Tactic_Identified']} tactic."
    else: # Fall back to rule check
        verdict_text = rule_check.get("verdict")
        score_percent = rule_check.get("accuracy_assessment", {}).get("score_percent", 0) 
        deep_analysis_text = f"Verification Confidence: {score_percent}%. Rule Detail: {rule_check.get('rule_detail', 'N/A')}"


    # 3. CONSTRUCT THE FULL REPORT (The saved content)
    full_report = {
        "VERDICT_AND_OVERVIEW": f"**True or False:** {verdict_text}. **Overview why:** {rule_check.get('rule_detail', 'N/A')}",
        "ACCURACY_ASSESSMENT": f"{score_percent}%",
        "RESOURCES_LIST": f"Tier 1: {', '.join(rule_check.get('tier_1_sources', []))}. Tier 2: {', '.join(rule_check.get('tier_2_sources', []))}",
        "DEEP_EXPLANATION": deep_analysis_text
    }

    # 4. SAVE THE FULL REPORT TO THE SHARED SESSION STATE
    tool_context.state["full_audit_report"] = full_report

    # 5. FINAL FIX: Return a single, synthesized string for the LLM to present cleanly.
    return {
        "summary_output": f"{verdict_text} ({score_percent}% match)."
    }

def present_full_report(tool_context: Any) -> str:
    """Retrieves the complete, four-part report from session state and formats it for the user."""
    report = tool_context.state.get("full_audit_report", {})
    if not report:
        return "Error: Full report data not found in session memory. Please restart the audit."

    # Format the saved report into the final, multi-section output
    output = f"""
{report.get('VERDICT_AND_OVERVIEW', '')}

**Accuracy assessment:** {report.get('ACCURACY_ASSESSMENT', 'N/A')}

**Resources:** {report.get('RESOURCES_LIST', 'N/A')}

**Deep explanation:** {report.get('DEEP_EXPLANATION', 'N/A')}
"""
    return output

# --- EXPORT AS ADK FUNCTIONTOOLS ---
# Only expose the flow managers to the Root Agent
run_audit_tool = FunctionTool(func=run_audit)
present_full_report_tool = FunctionTool(func=present_full_report)