from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# ==========================================
# Schema for Stage 1 & 2 Output (Account Memo)
# ==========================================

class AccountMemo(BaseModel):
    account_id: str = Field(..., description="Unique ID for the account")
    company_name: Optional[str] = Field(None, description="Name of the company")
    business_hours: Optional[str] = Field(None, description="Operating hours of the business")
    office_address: Optional[str] = Field(None, description="Physical address of the office")
    services_supported: List[str] = Field(default_factory=list, description="List of services the company provides")
    emergency_definition: Optional[str] = Field(None, description="What constitutes an emergency")
    emergency_routing_rules: Optional[str] = Field(None, description="Rules for routing emergencies")
    non_emergency_routing_rules: Optional[str] = Field(None, description="Rules for routing non-emergencies")
    call_transfer_rules: Optional[str] = Field(None, description="General call transfer rules (timeouts, fallbacks)")
    integration_constraints: Optional[str] = Field(None, description="System integration constraints")
    after_hours_flow_summary: Optional[str] = Field(None, description="Summary of after-hours operations")
    office_hours_flow_summary: Optional[str] = Field(None, description="Summary of office-hours operations")
    questions_or_unknowns: List[str] = Field(default_factory=list, description="Missing information or questions for the client")
    notes: Optional[str] = Field(None, description="Extra notes")

# ==========================================
# Schema for Stage 1 & 2 Output (Agent Spec)
# ==========================================

class AgentSpec(BaseModel):
    agent_name: str = Field(..., description="Name of the voice agent")
    voice_style: str = Field(..., description="Tone and style of the voice agent")
    system_prompt: str = Field(..., description="The full system prompt defining the agent's behavior")
    key_variables: List[str] = Field(default_factory=list, description="Variables to collect (e.g., name, number)")
    transfer_protocol: str = Field(..., description="How transfers are handled")
    fallback_protocol: str = Field(..., description="What happens if a transfer fails")
    version: Literal["v1", "v2"] = Field(..., description="Version of the spec (v1 for demo, v2 for onboarding)")
