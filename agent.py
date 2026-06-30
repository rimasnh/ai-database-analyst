import os
import sqlite3
from dotenv import load_dotenv
from google.adk import Agent

load_dotenv()

# ==========================================
# 1. THE DATA TOOL
# ==========================================
def query_database(sql_command: str) -> str:
    """Executes a read-only SQL command against the company database."""
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute(sql_command)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    except Exception as e:
        return f"Database Error: {str(e)}"

# ==========================================
# 2. THE SECURITY HOOK (GUARDRAIL)
# ==========================================
# ==========================================
# 2. THE SECURITY HOOK (GUARDRAIL)
# ==========================================
def security_bouncer(tool, args, **kwargs):
    """
    ADK 2.0 Lifecycle Hook. 
    ADK automatically passes:
      - tool: The actual Tool object (which has a .name attribute)
      - args: A dictionary of arguments being sent to the tool
    """
    # 1. Check the name attribute of the tool object
    if tool.name == "query_database":
        # 2. Extract the SQL command from the args dictionary
        sql = args.get("sql_command", "").upper()
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
        
        for keyword in forbidden_keywords:
            if keyword in sql:
                raise PermissionError(f"Security Alert: Destructive command '{keyword}' blocked!")

# ==========================================
# 3. THE AGENT INITIALIZATION
# ==========================================
root_agent = Agent(
    name="db_analyst",
    model="gemini-3.1-flash-lite",
    instruction="You are a data analyst helper. You have access to a database tool.",
    tools=[query_database],
    before_tool_callback=security_bouncer 
)

# Keep the file execution clean so the ADK runner can cleanly parse it
if __name__ == "__main__":
    print("Agent engine initialized successfully!")