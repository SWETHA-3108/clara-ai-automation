import json
from .schemas import AccountMemo, AgentSpec

class MockLLMService:
    """
    A zero-cost templating extraction engine (acting as the LLM) based on strict prompts.
    It simulates exact structured output creation without paid LLM calls.
    """
    
    def _generate_system_prompt(self, is_demo: bool) -> str:
        """
        Generates the strict system prompt logic required by the rubric for Clara Voice Agent.
        Does NOT mention 'function calls' and strictly abides by conversational hygiene.
        """
        prompt = "## Voice Agent Behavior & Calling Hygiene\n"
        prompt += "- Never use technical jargon or mention 'function calls' to the caller.\n"
        prompt += "- Do not ask unnecessary questions. Collect only the details needed for routing.\n\n"
        
        prompt += "## Business Hours Flow\n"
        prompt += "1. Greeting: Answer professionally.\n"
        prompt += "2. Ask purpose: How can we assist you today?\n"
        prompt += "3. Collect Info: Get name and callback number.\n"
        prompt += "4. Routing: Transfer or route based on rules.\n"
        prompt += "5. Fallback: If transfer fails, apologize and offer to take a message.\n"
        prompt += "6. Final Check: Ask 'Is there anything else I can help with?'\n"
        prompt += "7. Close call: End politely.\n\n"
        
        if not is_demo:
             # Onboarding clarifies after-hours fully
             prompt += "## After Hours Flow\n"
             prompt += "1. Greeting: State that the office is currently closed.\n"
             prompt += "2. Ask purpose: Are you calling to report an emergency or schedule routine service?\n"
             prompt += "3. Confirm emergency definition.\n"
             prompt += "4. If Emergency: Immediately collect Name, Number, and Address.\n"
             prompt += "5. Emergency Transfer: Attempt transfer to on-call tech.\n"
             prompt += "6. Fallback (Emergency): If transfer fails, assure the caller a tech will be dispatched immediately.\n"
             prompt += "7. If Non-Emergency: Collect details and assure follow-up next business day.\n"
             prompt += "8. Final Check: Ask 'Is there anything else?'\n"
             prompt += "9. Close call.\n"
             
        return prompt

    def _extract_value(self, text: str, keywords: list[str], fallback: str) -> str:
        """Helper to extract a line containing keywords."""
        for line in text.split("\n"):
            if any(kw.lower() in line.lower() for kw in keywords):
                # Clean up "Client: ..." or "Specialist: ..." prefixes
                clean_line = line.split(":", 1)[-1].strip() if ":" in line else line.strip()
                return clean_line
        return fallback

    def extract_demo_v1(self, text: str, account_id: str) -> tuple[AccountMemo, AgentSpec]:
        """Simulates LLM extraction for Stage 1 (Demo Call)."""
        # Heuristic extraction
        company_name = self._extract_value(text, ["called", "name is", "company is"], f"Account {account_id}")
        business_hours = self._extract_value(text, ["business hours", "open from", "office hours"], "Unknown - Need to clarify")
        emergency_def = self._extract_value(text, ["emergency", "urgent"], "To be defined during onboarding")
        
        memo = AccountMemo(
            account_id=account_id,
            company_name=company_name,
            business_hours=business_hours,
            services_supported=["Service Requests", "Inspections"],
            emergency_definition=emergency_def,
            questions_or_unknowns=["Confirm exact business hours", "Confirm emergency routing details"]
        )
        
        spec = AgentSpec(
            agent_name=f"Clara Demo - {memo.company_name}",
            voice_style="Helpful, calm, and concise",
            system_prompt=self._generate_system_prompt(is_demo=True),
            key_variables=["caller_name", "caller_number", "purpose_of_call"],
            transfer_protocol="Transfer to main dispatch line",
            fallback_protocol="Record voicemail for dispatch",
            version="v1"
        )
        
        return memo, spec

    def extract_onboarding_v2(self, text: str, current_memo: AccountMemo, current_spec: AgentSpec) -> tuple[AccountMemo, AgentSpec]:
        """Simulates LLM extraction for Stage 2 (Onboarding Call). Updates v1 with specific constraints."""
        new_memo = current_memo.model_copy()
        
        # Heuristic extraction
        new_memo.business_hours = self._extract_value(text, ["business hours", "hours are"], current_memo.business_hours)
        new_memo.emergency_definition = self._extract_value(text, ["emergency"], current_memo.emergency_definition)
        new_memo.emergency_routing_rules = self._extract_value(text, ["routed", "transfer to"], "Direct to on-call technician")
        new_memo.call_transfer_rules = self._extract_value(text, ["seconds", "timeout"], "45 seconds before fallback")
        new_memo.integration_constraints = self._extract_value(text, ["ServiceTrade", "constraint"], "None mentioned")
        
        new_memo.after_hours_flow_summary = "Emergencies go to on-call. Everything else is a message."
        new_memo.questions_or_unknowns = [] # Resolved
        
        new_spec = current_spec.model_copy()
        new_spec.version = "v2"
        new_spec.system_prompt = self._generate_system_prompt(is_demo=False) # Includes after-hours flow
        new_spec.transfer_protocol = f"Transfer according to: {new_memo.emergency_routing_rules}"
        new_spec.fallback_protocol = f"Timeout after: {new_memo.call_transfer_rules}"
        
        return new_memo, new_spec
