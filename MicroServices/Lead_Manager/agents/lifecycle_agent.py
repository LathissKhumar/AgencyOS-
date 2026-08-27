from typing import Any

from ..domain.lead import Lead
from ..domain.stage import LeadStage
from .llm_factory import LLMClient


class LifecycleAgent:
    def __init__(self, llm_client: LLMClient | None = None):
        self.llm = llm_client or LLMClient()

    async def recommend_next_action(
        self, lead: Lead, context: dict[str, Any]
    ) -> dict[str, Any]:
        match lead.stage:
            case LeadStage.DISCOVERED | LeadStage.QUALIFIED:
                return {"next_step": "AUDIT_WEBSITE", "delegated_service": "SDR"}
            case LeadStage.OPPORTUNITY_IDENTIFIED:
                return {"next_step": "GENERATE_PROPOSAL", "delegated_service": "SDR"}
            case LeadStage.PROPOSAL_READY:
                return {"next_step": "HUMAN_APPROVAL", "delegated_service": "UI"}
            case LeadStage.CONTACT_READY:
                return {
                    "next_step": "SEND_EMAIL",
                    "delegated_service": "CommunicationService",
                }
            case LeadStage.MEETING_REQUESTED:
                return {
                    "next_step": "SCHEDULE_CALENDAR",
                    "delegated_service": "SchedulingAgent",
                }
            case _:
                return {"next_step": "MONITOR", "delegated_service": "LifecycleAgent"}
