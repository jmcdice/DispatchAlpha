# Core Dispatch 2.0 - Architecture Document

## System Overview

Core Dispatch 2.0 is an AI-powered radio communication system that bridges traditional handheld radios with modern AI capabilities, designed to operate completely offline using local LLM inference. The system provides intelligent radio dispatch services for emergency response, community coordination, and industrial operations.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Raspberry Pi 5                                 │
│                                                                         │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │   Radio     │───▶│    Audio     │───▶│   Gemma 3n   │             │
│  │  Interface  │◀───│   Pipeline   │◀───│   AI Core    │             │
│  └─────────────┘    └──────────────┘    └──────────────┘             │
│         ▲                   │                    │                      │
│         │                   ▼                    ▼                      │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │   Hardware  │    │   Message    │    │   Storage    │             │
│  │   (USB/GPIO)│    │    Queue     │    │   (SQLite)   │             │
│  └─────────────┘    └──────────────┘    └──────────────┘             │
│                            │                    │                       │
│                            ▼                    ▼                       │
│                     ┌─────────────────────────────┐                    │
│                     │    FastAPI Backend          │                    │
│                     │  ┌─────────┐ ┌──────────┐  │                    │
│                     │  │REST API │ │WebSockets│  │                    │
│                     │  └─────────┘ └──────────┘  │                    │
│                     └─────────────────────────────┘                    │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
                              ┌─────────────────┐
                              │   Vue.js Web UI │
                              │  (Browser-based) │
                              └─────────────────┘
```

## Core Components

### 1. Audio Pipeline

The audio pipeline handles bidirectional audio flow between radio hardware and the AI system.

#### Receiver Flow
```
Radio RX → USB Audio Input → Audio Receiver →
Voice Activity Detection → Audio Buffer →
Gemma 3n (STT) → Text Transcription → Message Queue
```

#### Transmitter Flow
```
Message Queue → Text Response → Gemma 3n (TTS) →
Audio Buffer → USB Audio Output → Radio TX (VOX)
```

#### Key Features
- Continuous audio monitoring with configurable thresholds
- Silence detection for automatic segmentation
- Pre/post-roll buffering for complete capture
- Lock mechanism to prevent feedback loops
- Support for multiple audio formats (WAV, MP3)

### 2. AI Core (Gemma 3n Integration)

The AI core leverages Gemma 3n's multimodal capabilities for all intelligence features.

#### Components
- **Transcription Service**: Converts audio to text using Gemma 3n's audio understanding
- **Conversation Manager**: Maintains context and manages multi-turn conversations
- **Persona Engine**: Loads and applies persona-specific prompts and behaviors
- **Response Generator**: Creates contextually appropriate responses
- **Synthesis Service**: Converts text responses to natural speech

#### Gemma 3n Specific Features
- **Mix'n'match capability**: Dynamically switch between 4B/2B models based on load
- **Multimodal processing**: Handle audio, text, and future image inputs
- **Offline operation**: All inference runs locally
- **Multilingual support**: Built-in support for multiple languages

### 3. Plugin System for Scenarios

The plugin architecture allows for different operational modes without code changes.

#### Base Plugin Interface
```python
class ScenarioPlugin:
    def process_transcription(self, text: str) -> dict
    def select_persona(self, context: dict) -> str
    def enhance_response(self, response: str) -> str
    def get_tools(self) -> List[Tool]
    def get_ui_config(self) -> dict
```

#### Scenario Types
- **Emergency Response**: Dispatch protocols, incident tracking, resource allocation
- **Community Coordination**: Event management, volunteer coordination
- **Industrial Operations**: Safety protocols, equipment status, shift handovers

### 4. Message Queue System

Asynchronous message handling ensures smooth operation under varying loads.

#### Queue Types
- **Transcription Queue**: Incoming audio transcriptions
- **Response Queue**: Outgoing AI responses
- **Command Queue**: System control messages
- **Event Queue**: Real-time UI updates

#### Features
- Priority handling for emergency messages
- Persistence for recovery after crashes
- Rate limiting to prevent overload
- Dead letter queue for failed messages

### 5. Storage Layer

SQLite database for conversation history and system state.

#### Schema Design
```sql
-- Conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    transcription TEXT,
    response TEXT,
    persona TEXT,
    scenario TEXT,
    audio_file TEXT,
    metadata JSON
);

-- System events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    event_type TEXT,
    details JSON
);

-- Enhanced personas table
CREATE TABLE personas (
    id INTEGER PRIMARY KEY,
    name TEXT,
    scenario_type TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    is_active BOOLEAN,
    version INTEGER,
    parent_id INTEGER,
    config_json JSON
);

-- Persona versions table (for history)
CREATE TABLE persona_versions (
    id INTEGER PRIMARY KEY,
    persona_id INTEGER,
    version_number INTEGER,
    config_json JSON,
    created_at DATETIME,
    created_by TEXT,
    change_notes TEXT
);

-- Persona templates table
CREATE TABLE persona_templates (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    base_config JSON,
    category TEXT
);
```

### 6. Web API (FastAPI)

RESTful API with WebSocket support for real-time features.

#### REST Endpoints
- `/api/conversations` - CRUD for conversation history
- `/api/personas` - Complete persona management
- `/api/scenarios` - Scenario configuration
- `/api/system` - System status and control
- `/api/audio` - Audio device management

#### Persona Management Endpoints
```
/api/personas
  POST   /                  # Create new persona
  GET    /                  # List all personas
  GET    /{id}             # Get specific persona
  PUT    /{id}             # Update persona
  DELETE /{id}             # Delete persona
  POST   /{id}/activate    # Enable/disable persona
  POST   /{id}/duplicate   # Clone persona
  GET    /{id}/versions    # Get version history
  POST   /{id}/test        # Test persona response
  
/api/persona-templates
  GET    /                 # List available templates
```

#### WebSocket Events
- `transcription.new` - New transcription available
- `response.generated` - AI response ready
- `audio.level` - Real-time audio levels
- `system.status` - System health updates
- `persona.updated` - Persona configuration changed
- `persona.activated` - Persona activation event

### 7. Web UI (Vue.js)

Modern, responsive interface for monitoring and control.

#### Key Views
- **Dashboard**: Real-time system overview, active conversations
- **Monitor**: Live transcription feed, audio waveforms
- **Conversations**: Historical view with search and filters
- **Personas**: Create, edit, test, and manage personas
- **Settings**: System configuration, audio setup

#### Persona Management UI
```
web/src/components/personas/
├── PersonaEditor.vue       # Main editing interface
├── PromptBuilder.vue      # Visual prompt construction
├── VoiceSelector.vue      # Preview different voices
├── ActivationPhrases.vue  # Manage trigger phrases
├── PersonaTemplates.vue   # Start from templates
├── PersonaTester.vue      # Real-time testing
└── PersonaHistory.vue     # Version history viewer
```

#### Real-time Features
- Live transcription display
- Audio level meters
- System health indicators
- Active persona status
- Queue depth visualization
- Persona testing console

### 8. Dynamic Persona System

The persona system allows for real-time creation and modification of AI personalities.

#### Persona Configuration Structure
```json
{
  "id": "uuid",
  "name": "Emergency Dispatcher",
  "scenario": "emergency",
  "version": 3,
  "config": {
    "prompt": {
      "base": "You are an emergency dispatcher...",
      "components": [
        {"type": "tone", "value": "professional"},
        {"type": "context", "value": "radio_protocol"},
        {"type": "knowledge", "value": "emergency_procedures"}
      ]
    },
    "voices": {
      "primary": "shimmer",
      "fallback": "echo"
    },
    "activation": {
      "phrases": ["dispatch", "emergency"],
      "priority": 10,
      "context_required": false
    },
    "tools": ["weather_check", "unit_locator"],
    "behaviors": {
      "response_length": "concise",
      "use_radio_protocol": true,
      "confirm_understanding": true
    }
  },
  "metadata": {
    "created_by": "admin",
    "last_modified": "2024-01-20T10:30:00Z",
    "test_coverage": 85,
    "usage_stats": {
      "activations": 1523,
      "success_rate": 0.94
    }
  }
}
```

#### Features
- Hot-reload personas without system restart
- A/B testing with multiple versions
- Template library for quick setup
- Usage analytics and performance metrics
- Import/export for sharing configurations

## Data Flow

### Standard Communication Flow

1. **Audio Input**
   - Radio receives transmission
   - Audio captured via USB sound card
   - Voice activity detection triggers recording

2. **Transcription**
   - Audio buffer sent to Gemma 3n
   - Text transcription generated
   - Message queued with metadata

3. **Processing**
   - Scenario plugin processes transcription
   - Persona selected based on context/keywords
   - Conversation history updated

4. **Response Generation**
   - Gemma 3n generates contextual response
   - Scenario plugin enhances response
   - Response queued for transmission

5. **Audio Output**
   - Text converted to speech via Gemma 3n
   - Audio played through USB sound card
   - VOX triggers radio transmission

6. **UI Updates**
   - WebSocket broadcasts updates
   - UI reflects new messages
   - Logs and metrics updated

### Persona Management Flow

1. **Creation/Edit**
   - User modifies persona in web UI
   - Configuration validated
   - Saved to database with version

2. **Activation**
   - Persona marked as active
   - Loaded into memory
   - WebSocket notifies all clients

3. **Testing**
   - Test input processed
   - Response generated without transmission
   - Results displayed in UI

4. **Deployment**
   - Configuration pushed to AI core
   - Old version archived
   - Metrics tracking begins

## Deployment Architecture

### Hardware Requirements
- **Raspberry Pi 5** (8GB RAM recommended)
- **USB sound card**
- **3x handheld radios** (RX, TX, operator)
- **MicroSD card** (32GB minimum)

### Software Stack
- **OS**: Raspberry Pi OS Lite (64-bit)
- **Runtime**: Python 3.11+
- **Inference**: Gemma 3n via Ollama or native
- **Database**: SQLite 3
- **Web Server**: FastAPI + Uvicorn
- **Frontend**: Vue.js 3 + Vite

### Network Architecture
- System runs entirely on local network
- No internet dependency for core features
- Web UI accessible via Pi's IP address
- Optional internet for updates only

## Security Considerations

- **Privacy-first design**: All data stays local
- **Authentication**: Web UI requires authentication
- **Secure storage**: API keys stored securely
- **Data encryption**: Audio recordings encrypted at rest
- **Configurable retention**: Data retention policies
- **Audit logging**: Persona change audit logging

## Performance Optimization

- **Dynamic scaling**: Gemma 3n mix'n'match for dynamic scaling
- **Multi-threading**: Audio processing on separate thread
- **Async handling**: Message queues prevent blocking
- **Database optimization**: Efficient SQLite queries with indexes
- **Lazy loading**: Vue.js lazy loading for UI components
- **Connection pooling**: WebSocket connection pooling
- **Memory caching**: Persona configurations cached in memory

## Future Extensibility

- **Image processing**: Via web UI uploads
- **Multi-channel support**: Multi-radio channel support
- **External integrations**: External tool integrations
- **Cloud backup**: Optional cloud backup options
- **Mobile companion**: Mobile app companion
- **Hardware integration**: Hardware button integration via GPIO
- **Persona marketplace**: For sharing configurations
- **Internationalization**: Multi-language UI support

## System Requirements Summary

### Minimum Requirements
- Raspberry Pi 4 (4GB RAM)
- 32GB SD card
- USB sound card
- 3 handheld radios

### Recommended Requirements
- Raspberry Pi 5 (8GB RAM)
- 64GB SD card (high-speed)
- Quality USB sound card
- VOX-capable radios
- Stable power supply
