"""
Nexus Shopkeeper - Antigravity Concierge Agent
Orchestrates the intelligent agent loop that handles customer greetings,
real-time segment personalization, product recommendations, and custom retail actions.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
try:
    from google.antigravity import Agent, LocalAgentConfig
except ImportError:
    # Fallback mock classes for environments without the Google Antigravity SDK (e.g. instructor's PC)
    class LocalAgentConfig:
        def __init__(self, *args, **kwargs):
            pass

    class MockAgentResponse:
        def __init__(self, text_val: str):
            self._text_val = text_val
        async def text(self) -> str:
            return self._text_val

    class Agent:
        def __init__(self, *args, **kwargs):
            pass
        async def chat(self, prompt: str) -> MockAgentResponse:
            import re
            # Extract customer name and segment to build a realistic mock greeting
            name_match = re.search(r"customer '([^']+)'", prompt)
            seg_match = re.search(r"'([^']+)' segment", prompt)
            name = name_match.group(1) if name_match else "Customer"
            seg = seg_match.group(1) if seg_match else "Valued Shopper"
            
            greetings = {
                "Ultra-Luxury Spender": f"Welcome back, {name}! We are honored to serve you today. We have configured your premium checkout line and our concierge team is at your disposal. Explore our luxury arrivals in Aisles A & B!",
                "Strict Budget Spender": f"Assalam-o-Alaikum, {name}! Welcome to Nexus Shopkeeper. We have loaded our special discounted bundles for you today. Don't forget to check Aisle E for maximum savings!",
                "Strategic Deal-Hunter": f"Hello, {name}! Welcome. We've highlighted all items eligible for coupon discounts and bulk deals today. Enjoy your smart shopping!",
                "Mid-Tier Consistent": f"Welcome back, {name}! Great to see you again. We've applied your loyalty check-in bonus to your account.",
                "Essential Bulk Buyer": f"Welcome, {name}! Ready for bulk stocking? Check Aisle D and E for wholesale selections.",
                "High-Value Impulse": f"Hello, {name}! Check out our flash deals of the day on the main kiosks!"
            }
            res_text = greetings.get(seg, f"Assalam-o-Alaikum, {name}! Welcome to Nexus Shopkeeper. How can I help you today?")
            return MockAgentResponse(res_text)

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.core.store_credit_engine import StoreCreditEngine


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
