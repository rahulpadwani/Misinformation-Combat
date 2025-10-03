from google.adk.agents import LlmAgent
from google.genai import types
from .tools import run_audit_tool, present_full_report_tool 
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "gemini-2.5-flash") 

# --- The Conversational Presenter (ROOT AGENT) ---
# This LlmAgent is the face of the FWA, managing the interactive dialogue flow.
financial_behavior_coach = LlmAgent(
    name="Financial_Behavior_Coach",
    model=MODEL_ID,
    description="The primary conversational interface for the Financial Wellness Auditor. Guides the user through a two-step verification process: summary first, then resources on demand.",
    instruction=(
        "You are the conversational Financial Behavior Coach. Your goal is to guide the user to the correct facts and resources over multiple turns. "
        
        "**ON THE FIRST TURN (User's Question):** You MUST call the 'run_audit_tool' with the user's entire claim. "
        "When the tool returns the summary, **YOU MUST** present the key verdict and score to the user in a single, clear line. "
        "For example: 'The verdict is True (85% match).' "
        "Then, ask the user: 'Would you like the full list of Tier 1/2 Resources and the Deep Explanation?' "
        
        "**ON SUBSEQUENT TURNS (User replies 'Yes' or 'show me'):** If the user confirms, you MUST call the 'present_full_report_tool' to retrieve the complete, four-part audit."
    ),
    # The LlmAgent uses these tools to manage the conversation state and presentation.
    tools=[run_audit_tool, present_full_report_tool], 
)

# ADK entry point
root_agent = financial_behavior_coach