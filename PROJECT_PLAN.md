# Core Dispatch 2.0 - Project Plan

This document outlines the step-by-step plan for building the Core Dispatch 2.0 system. We will track our progress here, marking steps as complete and adding notes as we go.

## Phase 1: Core Backend & Project Setup

**Objective:** Establish the foundational project structure, database, and web server.

- [ ] **1.1: Project Scaffolding**
    - [ ] Create the main project directory (`core_dispatch`).
    - [ ] Set up a Python virtual environment.
    - [ ] Create subdirectories: `core_dispatch/api`, `core_dispatch/services`, `core_dispatch/models`, `core_dispatch/config`, `scripts`, `tests`.
    - [ ] Initialize a `git` repository.
    - [ ] Create a `.gitignore` file.
- [ ] **1.2: Initial Dependencies**
    - [ ] Create a `requirements.txt` file.
    - [ ] Add and install `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `pydantic`, `python-dotenv`.
- [ ] **1.3: Basic FastAPI App**
    - [ ] Create a `main.py` in the `api` directory.
    - [ ] Implement a basic "Hello World" endpoint to confirm the server runs.
- [ ] **1.4: Database Models**
    - [ ] Create `database.py` for SQLAlchemy setup (engine, session).
    - [ ] In `models/`, define the SQLAlchemy models for `conversations`, `events`, `personas`, `persona_versions`, and `persona_templates` as specified in the architecture.
- [ ] **1.5: Database Migrations**
    - [ ] Initialize `alembic` for database schema migrations.
    - [ ] Generate the initial migration to create all the tables.
    - [ ] Run the migration to create the initial `dispatch.db` SQLite database.

## Phase 2: Headless AI & Audio Core

**Objective:** Implement the core audio processing and AI interaction loop, capable of running without a UI. This mirrors the functionality you've already prototyped.

- [ ] **2.1: AI Service Stub**
    - [ ] Add `openai` to `requirements.txt`.
    - [ ] Create a `config` module for settings management.
    - [ ] Create an `ai_core` service that uses the `openai` library to connect to a local Ollama instance.
    - [ ] Implement a text-only generation function.
    - [ ] Configure it to use a Gemma model.
- [ ] **2.2: Audio Capture Service**
    - [ ] Create an `audio_service`.
    - [ ] Install `pyaudio`.
    - [ ] Implement a function to list and select audio input devices.
    - [ ] Implement a function to capture audio from the selected device.
- [ ] **2.3: Voice Activity Detection (VAD)**
    - [ ] Install a VAD library (e.g., `webrtcvad-wheels`).
    - [ ] Implement VAD to detect speech and silence in the audio stream, creating audio segments.
- [ ] **2.4: Speech-to-Text (STT)**
    - [ ] Integrate Gemma 3n's audio transcription capabilities into the `ai_core` service.
    - [ ] Create a function that takes an audio segment and returns a text transcription.
- [ ] **2.5: Text-to-Speech (TTS)**
    - [ ] Integrate Gemma 3n's TTS capabilities.
    - [ ] Create a function that takes text and returns a playable audio stream or file.
- [ ] **2.6: The Core Loop**
    - [ ] Create a `run_headless.py` script.
    - [ ] Stitch all the pieces together: `Audio Capture -> VAD -> STT -> AI Core (Text Gen) -> TTS -> Audio Output`.
    - [ ] Test the end-to-end flow by speaking into a microphone and hearing an AI-generated response.

## Phase 3: API and Real-time Communication

**Objective:** Expose the core functionality through a robust API and enable real-time UI updates.

- [ ] **3.1: Message Queue**
    - [ ] Implement a simple in-memory message queue system using Python's `queue` module.
    - [ ] Refactor the core loop to pass messages (transcriptions, responses) between components asynchronously.
- [ ] **3.2: WebSocket Service**
    - [ ] Implement a WebSocket endpoint in FastAPI (e.g., `/ws/updates`).
    - [ ] Broadcast events from the message queues (e.g., `new_transcription`, `new_response`) to connected clients.
- [ ] **3.3: Conversation API**
    - [ ] Create API endpoints (`/api/conversations`) for CRUD operations on the `conversations` table.
    - [ ] Ensure new conversations from the core loop are saved to the database.
- [ ] **3.4: Persona API (Basic)**
    - [ ] Create basic CRUD endpoints (`/api/personas`) for managing personas in the database.
- [ ] **3.5: System API**
    - [ ] Create an endpoint (`/api/system/status`) that provides health and status information.

## Phase 4: Vue.js Frontend

**Objective:** Build the web-based user interface for monitoring and control.

- [ ] **4.1: Frontend Project Setup**
    - [ ] Initialize a new Vue.js 3 project (using Vite) in a `web/` directory.
    - [ ] Install `axios` for API calls and a WebSocket client.
    - [ ] Set up basic project structure (views, components).
- [ ] **4.2: Live Monitor View**
    - [ ] Create a "Monitor" view.
    - [ ] Connect to the WebSocket and display real-time transcriptions and responses.
    - [ ] Add a simple audio level visualizer.
- [ ] **4.3: Conversation History View**
    - [ ] Create a "Conversations" view.
    - [ ] Fetch and display paginated conversation history from the API.
    - [ ] Add search and filtering capabilities.
- [ ] **4.4: Persona Management UI**
    - [ ] Create a "Personas" view.
    - [ ] List existing personas.
    - [ ] Build a form (`PersonaEditor.vue`) to create and edit personas.
- [ ] **4.5: Settings View**
    - [ ] Create a "Settings" view.
    - [ ] Display system status from the API.
    - [ ] Add controls for selecting audio devices.

## Phase 5: Advanced Features & Polish

**Objective:** Implement the advanced, dynamic features that make the system unique.

- [ ] **5.1: Dynamic Persona System**
    - [ ] Implement hot-reloading of persona configurations in the `ai_core` without a restart.
    - [ ] Implement the full persona versioning and templating system via the API.
- [ ] **5.2: Scenario Plugin Architecture**
    - [ ] Define the `ScenarioPlugin` base class.
    - [ ] Create a plugin loader in the `ai_core`.
    - [ ] Implement at least two sample plugins (e.g., "Default" and "Emergency Dispatch").
- [ ] **5.3: UI/UX Polish**
    - [ ] Refine the UI based on the full feature set (persona testing, version history).
    - [ ] Ensure the application is responsive and visually appealing.
- [ ] **5.4: Authentication**
    - [ ] Add a simple authentication layer to the web UI and API.

## Phase 6: Competition Submission

**Objective:** Package the project for the Gemma 3n Impact Challenge.

- [ ] **6.1: Story & Narrative**
    - [ ] Define the core "wow" factor and impact story for the video.
    - [ ] Script the 3-minute video demo.
- [ ] **6.2: Video Production**
    - [ ] Record screen captures of the UI in action.
    - [ ] Record footage of the system being used with handheld radios.
    - [ ] Edit the video to be engaging and impactful.
- [ ] **6.3: Technical Write-up**
    - [ ] Write the blog-style report detailing the architecture, use of Gemma 3n, and challenges.
- [ ] **6.4: Code Cleanup & Documentation**
    - [ ] Thoroughly comment and clean the codebase.
    - [ ] Write a comprehensive `README.md` for the public repository.
- [ ] **6.5: Final Submission**
    - [ ] Upload the video.
    - [ ] Publish the code repository.
    - [ ] Submit the project to the hackathon.
