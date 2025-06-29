# DispatchAlpha (Core Dispatch 2.0)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**DispatchAlpha is an AI-powered radio communication system that bridges traditional handheld radios with modern AI capabilities. It is designed to operate completely offline using local LLM inference.**

This project is being developed as an entry for the **[Google - The Gemma 3n Impact Challenge](https://www.kaggle.com/competitions/google-the-gemma-3n-impact-challenge)**, with the goal of creating a product that can make a tangible difference in real-world scenarios like emergency response, community coordination, and industrial operations.

---

## Key Features

-   **Offline First:** All core AI processing runs locally on-device (e.g., a Raspberry Pi), requiring no internet connection for its primary functions.
-   **Real-time Audio Processing:** A full audio pipeline captures audio from radio hardware, performs voice activity detection (VAD), and processes it in real-time.
-   **AI-Powered Dispatch:** Leverages the **Gemma 3n** model for Speech-to-Text (STT), intelligent response generation, and Text-to-Speech (TTS).
-   **Dynamic Personas:** AI personalities can be created, modified, and hot-reloaded without a system restart, allowing for different roles (e.g., "Emergency Dispatcher," "Event Coordinator").
-   **Plugin Architecture:** Scenarios (e.g., Emergency Response, Industrial Ops) can be implemented as plugins to modify system behavior without changing core code.
-   **Web-Based UI:** A modern Vue.js frontend provides a real-time dashboard for monitoring conversations, managing personas, and configuring the system.

## Technology Stack

-   **Backend:** Python, FastAPI, SQLAlchemy
-   **AI:** Gemma 3n served via Ollama
-   **AI Client:** OpenAI Python Library
-   **Database:** SQLite (for offline portability)
-   **Audio:** PyAudio, webrtcvad
-   **Frontend:** Vue.js 3, Vite
-   **Real-time:** WebSockets

## Project Status

This project is currently in **active development**. The initial backend structure and AI core service have been established. The next phase focuses on implementing the audio pipeline.

## Getting Started

These instructions are for setting up the development environment.

### Prerequisites

-   Python 3.11+
-   An instance of [Ollama](https://ollama.com/) running with the required Gemma model.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:jmcdice/DispatchAlpha.git
    cd DispatchAlpha
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    -   Copy the `.env.example` file to `.env`.
    -   Update the `.env` file with your specific settings (e.g., the exact Ollama model name).
    *(Note: An `.env.example` will be added in a future commit).*

5.  **Initialize the database:**
    ```bash
    alembic upgrade head
    ```

6.  **Run the application:**
    ```bash
    uvicorn core_dispatch.api.main:app --reload
    ```

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.
