# 🌌 Scrape the Verse (AgencyOS)

> **Autonomous Multi-Agent AI Sales Development Representative (SDR) & Agency Growth Operating System**  
> *Transforming raw local directory data into qualified, high-paying agency clients through closed-loop self-healing extraction, deep parallel SEO & business auditing, dynamic opportunity scoring, automated proposal generation, omnichannel outreach, deterministic CRM lifecycle tracking, and real-time autonomous voice calling.*

---

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 16](https://img.shields.io/badge/next.js-16.3-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![React 19](https://img.shields.io/badge/react-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF6F00?style=for-the-badge)](https://www.langchain.com/langgraph)
[![Playwright](https://img.shields.io/badge/Playwright-Stealth-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Tailwind CSS 4](https://img.shields.io/badge/Tailwind_CSS-v4.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Twilio Voice](https://img.shields.io/badge/Twilio-Telephony-F22F46?style=for-the-badge&logo=twilio&logoColor=white)](https://www.twilio.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

## 📖 Table of Contents

- [Executive Summary](#-executive-summary)
- [System Architecture & Topology](#-system-architecture--topology)
- [The 10-Layer Autonomous Pipeline](#-the-10-layer-autonomous-pipeline)
  - [Layer 1: Autonomous Lead Discovery & Self-Healing Scraper](#layer-1-autonomous-lead-discovery--self-healing-scraper-8000)
  - [Layer 2: In-Flight Data Normalization & Verification](#layer-2-in-flight-data-normalization--verification)
  - [Layer 3: Parallel Intelligence & Dual Auditing](#layer-3-parallel-intelligence--dual-auditing-8081)
  - [Layer 4: AI Prompt Generation & Sales Narrative](#layer-4-ai-prompt-generation--sales-narrative)
  - [Layer 5: Dynamic Opportunity Engine](#layer-5-dynamic-opportunity-engine)
  - [Layer 6: Proposal Studio & PDF Generator](#layer-6-proposal-studio--pdf-generator)
  - [Layer 7: Omnichannel Outreach Copywriter](#layer-7-omnichannel-outreach-copywriter)
  - [Layer 8: Lead Management CRM & Lifecycle Engine](#layer-8-lead-management-crm--lifecycle-engine-8082)
  - [Layer 9: Autonomous Voice Agent & Telephony Bot](#layer-9-autonomous-voice-agent--telephony-bot-8084)
  - [Layer 10: Unified Command Center Dashboard](#layer-10-unified-command-center-dashboard-3000)
  - [Complementary: Zero-Cloud Email Communication Service](#complementary-zero-cloud-email-communication-service-8083)
- [Microservices Network & Port Allocation](#-microservices-network--port-allocation)
- [Agent-to-Agent (A2A) Protocol Standard](#-agent-to-agent-a2a-protocol-standard)
- [Directory Structure](#-directory-structure)
- [Getting Started & Installation](#-getting-started--installation)
  - [Prerequisites](#prerequisites)
  - [Environment Configuration](#environment-configuration)
  - [Quick Start: Launching All Services](#quick-start-launching-all-services)
- [Running Individual Subsystems](#-running-individual-subsystems)
- [Automated Testing & Verification](#-automated-testing--verification)
- [Contributing](#-contributing)
- [License](#-license)

---

## ⚡ Executive Summary

Digital marketing, web design, and SEO agencies spend up to **70% of their business development hours** on repetitive manual tasks: sourcing local leads from directories, auditing outdated websites, analyzing competitors, drafting tailored sales pitch decks, dialing prospects, and updating CRM records.

**Scrape the Verse (AgencyOS)** completely automates this lifecycle through an orchestrated network of specialized AI microservices:

1. **Discovers** high-potential local businesses across Google Maps, Yelp, and YellowPages with autonomous self-healing scrapers.
2. **Normalizes** and verifies contact info, MX email records, SSL certificates, and deduplication hashes in-flight.
3. **Audits** both the prospect's technical website health (Core Web Vitals, Schema, on-page SEO, CTA conversion funnels) and their real-world market standing (live DuckDuckGo competitor research and sentiment analysis) concurrently.
4. **Synthesizes** findings into tailored agency service opportunities (`WEBSITE_REDESIGN`, `LOCAL_SEO`, `SPEED_PERFORMANCE`, `CONTENT_STRATEGY`, `AI_BOOKING_FUNNEL`) with quantifiable ROI metrics.
5. **Generates** complete, branded Markdown and PDF proposals alongside multi-touch omnichannel outreach packs (3-touch emails, branching cold call scripts, LinkedIn InMails, SMS teasers).
6. **Manages** prospect progression across a deterministic 17-stage CRM state machine with live Server-Sent Events (SSE).
7. **Dials & Qualifies** prospects autonomously via real-time streaming telephony voice agents with objection handling and instant RFC 5545 calendar meeting scheduling.

---

## 🏗️ System Architecture & Topology

```text
                               ┌────────────────────────────────────────┐
                               │             DATA SOURCES               │
                               │   (Google Maps, Yelp, YellowPages)     │
                               └───────────────────┬────────────────────┘
                                                   │
                                                   ▼
                               ┌────────────────────────────────────────┐
                               │      1. LEAD FINDER AGENT (:8000)      │
                               │   (Playwright Stealth + Self-Healing)  │
                               └───────────────────┬────────────────────┘
                                                   │
                                                   ▼
                               ┌────────────────────────────────────────┐
                               │       2. DATA NORMALIZATION LAYER      │
                               │      (Dedupe, Validate, Enrich)        │
                               └───────────────────┬────────────────────┘
                                                   │
                        ┌──────────────────────────┴──────────────────────────┐
                        │ (Website Present)                                   │ (No Website Found)
                        ▼                                                     ▼
         ┌─────────────────────────────┐                       ┌─────────────────────────────┐
         │ 3. PARALLEL ANALYSIS LAYER  │                       │ 9. VOICE AGENT / CALL BOT   │ :8084
         │ ┌─────────────────────────┐ │                       │ (Pitch Custom Web Build &   │
         │ │ Website/SEO Audit Agent │ │                       │  Local 3-Pack Optimization) │
         │ │ (LibreCrawl 6x Analyzers│ │                       │ ┌─────────────────────────┐ │
         │ │  + CTA Detector)        │ │                       │ │ A2A Invokable / Twilio  │ │
         │ └─────────────────────────┘ │                       │ │ Multi-turn State Engine │ │
         │ ┌─────────────────────────┐ │                       │ │ Transcript & Booking Gen│ │
         │ │ Business Analysis Agent │ │                       │ └────────────┬────────────┘ │
         │ │ (DuckDuckGo Live Search │ │                       └──────────────┼──────────────┘
         │ │  + Qwen3/Gemini Profile)│ │                                      │
         │ └─────────────────────────┘ │                                      │
         └──────────────┬──────────────┘                                      │
                        │                                                     │
                        ▼                                                     │
         ┌─────────────────────────────┐                                      │
         │ 4. PROMPT GENERATION LAYER  │                                      │
         │ (Sales Narrative & Angles)  │                                      │
         └──────────────┬──────────────┘                                      │
                        │                                                     │
                        ▼                                                     │
         ┌─────────────────────────────┐                                      │
         │ 5. OPPORTUNITY ENGINE       │                                      │
         │ (Agency Service Matching)   │                                      │
         └──────────────┬──────────────┘                                      │
                        │                                                     │
                        ▼                                                     │
         ┌─────────────────────────────┐                                      │
         │ 6. PROPOSAL GENERATOR       │                                      │
         │ (Markdown / PDF Studio)     │                                      │
         └──────────────┬──────────────┘                                      │
                        │                                                     │
                        ▼                                                     │
         ┌─────────────────────────────┐                                      │
         │ 7. OUTREACH PREPARATION     │                                      │
         │ (Emails, Script, LinkedIn)  │                                      │
         └──────────────┬──────────────┘                                      │
                        │                                                     │
                        ▼                                                     │
         ┌─────────────────────────────┐                                      │
         │ 8. LEAD MANAGEMENT CRM      │◄─────────────────────────────────────┘
         │ (17 Stages, Tasks, Timeline,│ :8082
         │  RFC 5545 .ics Scheduler)   │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │ 10. SDR DASHBOARD FRONTEND  │ :3000
         │ (Command Center UI & HITL)  │
         └─────────────────────────────┘
```

---

## 🧩 The 10-Layer Autonomous Pipeline

### Layer 1: Autonomous Lead Discovery & Self-Healing Scraper (`:8000`)
* **Package**: [`MicroServices/Lead_Finder/`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/Lead_Finder/) & [`MicroServices/leadfinder/`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/leadfinder/)
* **Capabilities**:
  * **Multi-Engine Ingestion**: Supports direct targeted scraping of Google Maps, Yelp, and YellowPages.
  * **Stealth Crawling & Anti-Bot Bypassing**: Uses Playwright with fingerprint rotation, headless evasion, realistic mouse movements, and dynamic scroll handling.
  * **6-Node Self-Healing LangGraph Loop**:
    1. *Planner Agent* (`Qwen3:8b` / Gemini)
    2. *Scraper Node* (Playwright DOM extraction)
    3. *Extraction Engine* (Cascading CSS, XPath, Table, and Semantic LLM extractors)
    4. *Validation Engine* (Calculates deterministic data health score $H$)
    5. *Diagnosis Agent* (Root-cause classification on broken selectors or layout shifts)
    6. *Healing Loop* (Action repair, canary verification across multiple pages, persistent patch memory).
  * **Cloud Fallback**: Integrated 2-Tier Bright Data Scraper Studio cloud pipeline for high-throughput B2B supplier extraction.

### Layer 2: In-Flight Data Normalization & Verification
* **Module**: [`MicroServices/SDR/normalizer.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/normalizer.py)
* **Capabilities**:
  * **Deduplication Engine**: Generates unique cryptographic SHA256 hashes based on normalized root domain or standardized E.164 phone numbers.
  * **Live Verification**: Asynchronous DNS MX record lookup to ensure inbox deliverability, SSL certificate validity checks, and HTTP status code probing.
  * **Standardization & Classification**: Normalizes business Name, Address, and Phone (NAP), parses geo-coordinates, and auto-classifies industry niches.

### Layer 3: Parallel Intelligence & Dual Auditing (`:8081`)
* **Module**: [`MicroServices/SDR/analysis_orchestrator.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/analysis_orchestrator.py)
* **Execution**: Concurrently executes two deep auditing agents via `asyncio.gather`:
  1. **Website & Technical SEO Agent**:
     * **LibreCrawl**: Deep DOM crawler extracting title tags, meta descriptions, headings hierarchy, open graph tags, and external scripts.
     * **6 Domain Analyzers**: `technical`, `onpage`, `content`, `schema`, `local`, and `performance` (Core Web Vitals LCP, FID, CLS estimation).
     * **CTA & Funnel Detector**: [`cta_detector.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/cta_detector.py) inspects HTML for conversion elements (phone `tel:` links, booking embed widgets, live chat, lead forms).
  2. **Business Intelligence Agent**:
     * **DuckDuckGo Live Search**: [`search_client.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/search_client.py) queries live search results for top local competitors, review sentiment, and digital presence.
     * **SWOT Synthesis**: Generates detailed company profiles, demographic target mapping, competitor differentiation, and operational weaknesses.

### Layer 4: AI Prompt Generation & Sales Narrative
* **Module**: [`MicroServices/SDR/prompt_generator.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/prompt_generator.py)
* **Capabilities**:
  * Merges technical SEO audit gaps with market analysis into a unified `PersonalizedPromptPack`.
  * Extracts **Company Context**, **Critical Pain Points**, **Value Angles**, **Proof Points**, and **Dynamic Objection Responses** (handling common pushbacks like *"We already have an agency"*, *"No budget"*, or *"We rely on word of mouth"*).

### Layer 5: Dynamic Opportunity Engine
* **Module**: [`MicroServices/SDR/opportunity_engine.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/opportunity_engine.py)
* **Capabilities**:
  * Evaluates prospect deficiencies against a structured **Agency Service Catalog**:
    | Service Code | Solution Description | Typical Investment | Target ROI Impact |
    |---|---|---|---|
    | `WEBSITE_REDESIGN` | Modern responsive UI/UX, mobile Core Web Vitals optimization | $1,500 – $3,500 | +40-80% conversion rate |
    | `LOCAL_SEO` | Google 3-Pack Schema injection, citations, review boosting | $750 / mo | +200% local map visibility |
    | `SPEED_PERFORMANCE` | Sub-1.8s load time, image compression, script tree-shaking | $500 | -35% bounce rate reduction |
    | `CONTENT_STRATEGY` | High-intent service landing pages, search intent copywriting | $900 / mo | +150% organic organic traffic |
    | `AI_BOOKING_FUNNEL` | Automated customer booking bot, 24/7 lead capture, CRM sync | $1,200 | +25% immediate appointment volume |
  * Quantifies **Impact Score (1-100)**, **Urgency Score (1-100)**, and revenue upside.

### Layer 6: Proposal Studio & PDF Generator
* **Module**: [`MicroServices/SDR/proposal_generator.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/proposal_generator.py)
* **Capabilities**:
  * Formats complete, professional client-ready proposals in both Markdown and HTML/PDF.
  * Structured into: **Executive Summary**, **Current State Audit Breakdown**, **Recommended Deliverables**, **Pricing & Investment Matrix**, **Implementation Timeline**, and **Next Steps**.

### Layer 7: Omnichannel Outreach Copywriter
* **Module**: [`MicroServices/SDR/outreach_preparer.py`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/SDR/outreach_preparer.py)
* **Capabilities**:
  * **3-Touch Cold Email Sequence**:
    * *Touch 1 (Day 1)*: Specific technical vulnerability hook + complimentary value offer.
    * *Touch 2 (Day 4)*: Niche case study with quantifiable ROI metrics.
    * *Touch 3 (Day 8)*: Soft breakup / permission to close the file.
  * **Dynamic Cold Call Script**: Gatekeeper bypass, 15-second executive hook, branching objection handlers, and meeting CTA.
  * **LinkedIn Outreach**: 300-character connection note + personalized follow-up InMail.
  * **SMS / WhatsApp Teaser**: Direct, mobile-friendly conversational hook.

### Layer 8: Lead Management CRM & Lifecycle Engine (`:8082`)
* **Package**: [`MicroServices/Lead_Manager/`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/Lead_Manager/)
* **Capabilities**:
  * **System of Record**: High-concurrency Async SQLite database running in WAL mode with support for **Twenty CRM** synchronization.
  * **17-Stage Deterministic Lifecycle**:
    ```text
    DISCOVERED ➔ QUALIFIED ➔ OPPORTUNITY_IDENTIFIED ➔ PROPOSAL_READY ➔ CONTACT_READY ➔
    CONTACTED ➔ ENGAGED ➔ MEETING_REQUESTED ➔ MEETING_SCHEDULED ➔ NEGOTIATION ➔ WON (or REJECTED / STALE)
    ```
  * **Event Bus & Real-Time Timeline**: Streams audit logs and status transitions over Server-Sent Events (SSE) at `GET /api/v1/timeline/stream`.
  * **Automated Task Generator & RFC 5545 Calendar Scheduler**: Auto-generates follow-up tasks and exports `.ics` calendar invites for booked discovery sessions.

### Layer 9: Autonomous Voice Agent & Telephony Bot (`:8084`)
* **Package**: [`MicroServices/Voice_Agent/`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/Voice_Agent/)
* **Capabilities**:
  * **Dual Operating Modes**:
    1. *No-Website Outbound Mode*: Dials local businesses that have no website, pitching modern web presence and Google Maps local optimization.
    2. *Website Inbound/Outbound Qualification*: Dials prospects based on identified audit weaknesses.
  * **Multi-Turn Conversational State Engine**:
    ```text
    OPENING ➔ PITCH ➔ FAQ_AND_OBJECTIONS ➔ MEETING_BOOKING ➔ CLOSING
    ```
  * **Telephony Stack**: Twilio Media Streams, WebRTC, Silero Voice Activity Detection (VAD), Microsoft Edge-TTS / ElevenLabs speech synthesis.
  * **Simulation Engine**: Local interactive CLI calling mode for rapid automated testing and evaluation.

### Layer 10: Unified Command Center Dashboard (`:3000`)
* **Package**: [`MicroServices/UI/frontend/`](file:///home/lathiss/Projects/Scrape_the_Verse/MicroServices/UI/frontend/)
* **Capabilities**:
  * **Modern Aesthetics**: Built with Next.js 16, React 19, Tailwind CSS 4, GSAP ScrollTrigger, Lenis smooth scrolling, and dark glassmorphic tokens.
  * **Lead Discovery Studio**: Interactive trigger for multi-source scraping jobs with live progress indicators.
  * **Pipeline Kanban**: Drag-and-drop 17-stage lead management with real-time SSE updates.
  * **Proposal & Outreach Studio**: Live Markdown/PDF preview and one-click edit/dispatch.
  * **Voice Agent Command Panel**: Interactive call simulation console, audio playback, and transcript inspector.

### Complementary: Zero-Cloud Email Communication Service (`:8083`)
* **Package**: [`services/gmail_pubsub_listener/`](file:///home/lathiss/Projects/Scrape_the_Verse/services/gmail_pubsub_listener/)
* **Capabilities**:
  * Replaces cloud message queues with lightweight **IMAP IDLE** and **Gmail SMTP over TLS**.
  * Auto-syncs inbound replies, extracts MIME body attachments, correlates threads with active CRM leads, and uses local Ollama `qwen3` models for intent and sentiment classification.

---

## 🌐 Microservices Network & Port Allocation

| Service | Port | Directory | Tech Stack | Primary Endpoints |
|---|---|---|---|---|
| **Lead Finder Agent** | `8000` | `MicroServices/Lead_Finder/` | FastAPI, Playwright, LangGraph | `POST /api/v1/scrape`<br>`POST /api/v1/pipeline/dispatch`<br>`GET /health` |
| **SDR Intelligence Orchestrator** | `8081` | `MicroServices/SDR/` | FastAPI, LibreCrawl, DuckDuckGo, Ollama/Gemini | `POST /api/v1/sdr/process`<br>`POST /api/v1/audit`<br>`GET /.well-known/agent.json`<br>`POST /a2a/invoke` |
| **Lead Manager CRM** | `8082` | `MicroServices/Lead_Manager/` | FastAPI, Async SQLite (WAL), Twenty Client | `POST /api/v1/leads`<br>`POST /api/v1/events`<br>`GET /api/v1/timeline/stream`<br>`POST /api/v1/meetings` |
| **Communication Service** | `8083` | `services/gmail_pubsub_listener/` | FastAPI, IMAPlib, smtplib, SQLite | `POST /api/v1/mail/sync`<br>`POST /api/v1/mail/send`<br>`GET /health` |
| **Voice Agent / Call Bot** | `8084` | `MicroServices/Voice_Agent/` | FastAPI, WebSockets, Twilio, Edge-TTS, VAD | `POST /api/v1/voice/simulate-call`<br>`POST /api/v1/voice/webhook`<br>`GET /.well-known/agent.json`<br>`POST /a2a/invoke` |
| **Command Center UI** | `3000` | `MicroServices/UI/frontend/` | Next.js 16, React 19, Tailwind CSS 4, GSAP | `GET /`<br>`GET /dashboard` |

---

## 🤖 Agent-to-Agent (A2A) Protocol Standard

AgencyOS implements the **Agent-to-Agent (A2A)** open protocol across all microservices:

1. **Discovery**: Every service exposes a standardized agent card at `GET /.well-known/agent.json`:
   ```json
   {
     "agent_id": "sdr-intelligence-agent",
     "name": "AgencyOS SDR Intelligence Agent",
     "version": "1.0.0",
     "capabilities": ["normalization", "seo_audit", "business_analysis", "opportunity_scoring", "proposal_generation", "outreach_preparation"],
     "endpoints": {
       "invoke": "/a2a/invoke"
     }
   }
   ```
2. **Invocation**: Services trigger peer agents using standardized JSON RPC payloads at `POST /a2a/invoke`:
   ```json
   {
     "action": "process_lead",
     "payload": {
       "company_name": "Horizon Dental Clinic",
       "website": "https://horizondental.example.com"
     }
   }
   ```

---

## 📁 Directory Structure

```text
Scrape_the_Verse/
├── .env                                  # Unified environment configuration
├── requirements.txt                      # Core Python dependencies
├── package.json                          # Root workspace package definitions
├── pytest.ini                            # Pytest test suite configuration
├── docker-compose.twenty.yml             # Self-hosted Twenty CRM container stack
├── scripts/
│   ├── start_all_microservices.sh        # One-click microservices launcher
│   ├── start_backend_services.py         # Supervisor process manager with live health checks
│   ├── run_e2e_full_pipeline.py          # 10-Layer end-to-end integration test
│   ├── live_voice_interactive.py         # Interactive CLI voice simulator
│   └── start_twenty_crm.sh               # Twenty CRM starter script
├── MicroServices/
│   ├── Lead_Finder/                      # Layer 1: Self-healing multi-directory scraping agent
│   │   ├── crawler/                      # Playwright crawler engine
│   │   ├── extraction/                   # Multi-strategy DOM extractors
│   │   ├── validation/                   # Deterministic data health validation
│   │   ├── diagnosis/                    # Root cause failure analysis
│   │   ├── healing/                      # Self-healing selector patch loop
│   │   └── brightdata/                   # 2-Tier cloud scraper studio pipeline
│   ├── SDR/                              # Layers 2 - 7: SDR Intelligence Orchestration
│   │   ├── normalizer.py                 # Layer 2: Deduplication, MX records, SSL verification
│   │   ├── analysis_orchestrator.py      # Layer 3: Parallel SEO + Business Intelligence
│   │   ├── business_analyzer.py          # Layer 3: DuckDuckGo live search & SWOT analyzer
│   │   ├── cta_detector.py               # Layer 3: Conversion funnel & CTA detector
│   │   ├── prompt_generator.py           # Layer 4: Personalized sales narrative generator
│   │   ├── opportunity_engine.py         # Layer 5: Agency service catalog matching & scoring
│   │   ├── proposal_generator.py         # Layer 6: Markdown & PDF proposal studio
│   │   ├── outreach_preparer.py          # Layer 7: Omnichannel email/call/LinkedIn packs
│   │   ├── orchestrator.py               # Master SDR pipeline orchestrator
│   │   └── server.py                     # SDR FastAPI service (:8081)
│   ├── Lead_Manager/                     # Layer 8: Lead Management CRM (:8082)
│   │   ├── domain/                       # Core domain models (Lead, Opportunity, Task, Meeting)
│   │   ├── policy/                       # 17-stage lifecycle state machine & transition rules
│   │   ├── repository/                   # Async SQLite database layer & query managers
│   │   ├── events/                       # Internal event bus & SSE timeline streaming
│   │   └── crm/                          # Twenty CRM bi-directional adapter
│   ├── Voice_Agent/                      # Layer 9: Autonomous Call Bot (:8084)
│   │   ├── state_machine.py              # Multi-turn conversational flow engine
│   │   ├── telephony_adapter.py          # Twilio / WebRTC / Simulation adapters
│   │   ├── voice_engine.py               # Audio synthesis & Edge-TTS streaming
│   │   ├── vad.py                        # Voice Activity Detection (Silero)
│   │   └── server.py                     # Voice Agent FastAPI service (:8084)
│   └── UI/                               # Layer 10: Next.js Frontend Dashboard (:3000)
│       └── frontend/                     # Next.js 16 App Router application
└── services/
    └── gmail_pubsub_listener/            # Zero-cloud IMAP IDLE / SMTP communication service (:8083)
```

---

## 🚀 Getting Started & Installation

### Prerequisites

- **Python**: Version `3.11` or newer
- **Node.js**: Version `18.x` or newer (along with `npm` $\ge 9$)
- **Ollama** (Optional, for 100% local offline AI inference): `ollama run qwen3:8b`
- **Google Gemini API Key** (Optional fallback / cloud LLM): [Google AI Studio](https://aistudio.google.com/)
- **Playwright System Dependencies**: Required for headless browser crawling

### Environment Configuration

Create a `.env` file in the root directory (or copy from `.env.example`):

```bash
# ------------------------------------------------------------------------------
# LLM & AI PROVIDERS
# ------------------------------------------------------------------------------
GEMINI_API_KEY="your_gemini_api_key_here"
OLLAMA_BASE_URL="http://localhost:11434"
DEFAULT_LLM_MODEL="gemini-2.0-flash"

# ------------------------------------------------------------------------------
# MICROSERVICE NETWORK PORTS
# ------------------------------------------------------------------------------
LEAD_FINDER_PORT=8000
SDR_PORT=8081
LEAD_MANAGER_PORT=8082
COMMUNICATION_PORT=8083
VOICE_AGENT_PORT=8084
FRONTEND_PORT=3000

# ------------------------------------------------------------------------------
# TWILIO TELEPHONY (OPTIONAL - FOR REAL PHONE CALLS)
# ------------------------------------------------------------------------------
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
TWILIO_PHONE_NUMBER=""

# ------------------------------------------------------------------------------
# EMAIL COMMUNICATION (OPTIONAL - FOR LIVE INBOX SYNC)
# ------------------------------------------------------------------------------
GMAIL_USER=""
GMAIL_APP_PASSWORD=""
```

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LathissKhumar/Scrape_the_Verse.git
   cd Scrape_the_Verse
   ```

2. **Set Up Python Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**:
   ```bash
   playwright install chromium
   ```

4. **Install Frontend Dependencies**:
   ```bash
   cd MicroServices/UI/frontend
   npm install
   cd ../../..
   ```

### Quick Start: Launching All Services

Launch the unified supervisor to start all 5 backend microservices with automatic port cleanup and health monitoring:

```bash
./scripts/start_all_microservices.sh
# or: python scripts/start_backend_services.py
```

In a separate terminal, launch the Next.js frontend command center:

```bash
npm run dev
```

Visit the frontend dashboard at **`http://localhost:3000`**.

---

## 🧪 Running Individual Subsystems

### 1. Run Full 10-Layer End-to-End Pipeline Demo
Execute an autonomous test demonstrating lead ingestion, normalization, parallel auditing, proposal generation, CRM dispatch, voice call simulation, and calendar meeting scheduling:

```bash
python scripts/run_e2e_full_pipeline.py
```

### 2. Run Interactive Voice Agent Simulator
Test the voice agent directly in your terminal with simulated speech turns and objection handling:

```bash
python scripts/live_voice_interactive.py
```

### 3. Launch Twenty CRM via Docker Compose
Run a production-grade, self-hosted open-source CRM connected directly to the Lead Manager:

```bash
docker compose -f docker-compose.twenty.yml up -d
```

---

## 🔬 Automated Testing & Verification

The repository includes a comprehensive unit and integration test suite covering all microservices, agents, domain policies, and API endpoints.

To run the complete test suite:

```bash
pytest -v
```

To run tests for a specific microservice:

```bash
# Test SDR Orchestrator & Analyzers
pytest MicroServices/SDR/tests/ -v

# Test Lead Manager CRM & State Machine
pytest MicroServices/Lead_Manager/tests/ -v

# Test Voice Agent State Machine & Simulation
pytest MicroServices/Voice_Agent/tests/ -v

# Test Lead Finder Scrapers & Validation
pytest MicroServices/Lead_Finder/tests/ -v
```

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'feat: add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Built with ❤️ by the Scrape the Verse / AgencyOS Team</b>
</p>
