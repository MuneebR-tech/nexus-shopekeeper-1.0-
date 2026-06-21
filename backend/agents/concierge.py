"""
Nexus Shopkeeper - Antigravity Concierge Agent
Orchestrates the intelligent agent loop that handles customer greetings,
real-time segment personalization, product recommendations, and custom retail actions.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
from google.antigravity import Agent, LocalAgentConfig

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_2.store_credit_engine import StoreCreditEngine


class ConciergeAgentManager:
    """
    Manages the lifecycle and tool execution for the autonomous Antigravity retail agent.
    """
    def __init__(self, api_key: str = "mock-api-key"):
        self.config = LocalAgentConfig()
        self.api_key = api_key
        self.agent = None
        self.credit_engine = None

    async def initialize_agent(self):
        """
        Spawns the Antigravity Agent instance.
        """
        self.agent = Agent(config=self.config)
        self.credit_engine = StoreCreditEngine()

    async def greet_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Triggers a tailored persona-based handshake prompt.
        Uses the customer segment type (e.g., Ultra-Luxury Spender vs Strict Budget Spender)
        to customize the agent tone and concierge actions.
        """
        if not self.agent or not self.credit_engine:
            await self.initialize_agent()

        cust = self.credit_engine.customers.get(customer_id)
        if not cust:
            return {
                "status": "error",
                "message": f"Customer {customer_id} not found."
            }

        segment = self.credit_engine.get_segment(customer_id)
        balance = self.credit_engine.get_balance(customer_id)
        name = cust.get("name", "Customer")

        # Custom prompt to agent to greet this customer
        prompt = (
            f"Greet customer '{name}' (ID: {customer_id}) who belongs to the "
            f"'{segment}' segment. Their store credit balance is ${balance:.2f}. "
            f"Deliver a tailored, premium greeting that matches their shopping persona."
        )

        response = await self.agent.chat(prompt)
        text_response = await response.text()

        return {
            "status": "connected",
            "customer_id": customer_id,
            "name": name,
            "segment": segment,
            "balance": balance,
            "message": text_response
        }

    async def process_voice_or_text_request(self, text: str) -> str:
        """
        Interfaces with the Antigravity agent shell to execute user kiosk actions.
        """
        if not self.agent:
            await self.initialize_agent()

        response = await self.agent.chat(text)
        return await response.text()
