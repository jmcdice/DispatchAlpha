# Core Dispatch 2.0 - Technical Architecture

This document details the specific technology stack and architectural decisions for the Core Dispatch 2.0 project.

## 1. Backend

-   **Language:** Python 3.11+
    -   *Reasoning:* A mature ecosystem with excellent libraries for AI, audio processing, and web development.

-   **Web Framework:** FastAPI
    -   *Reasoning:* Provides a high-performance, modern framework for building RESTful APIs. Its automatic OpenAPI/Swagger documentation is invaluable for development and testing. It also has built-in support for asynchronous operations and WebSockets, which are critical for our real-time features.

-   **Web Server:** Uvicorn
    -   *Reasoning:* A lightning-fast ASGI server, built on uvloop and httptools. It is the standard server for running FastAPI applications.

-   **Database ORM:** SQLAlchemy
    -   *Reasoning:* The de-facto standard for database interaction in Python. It provides a powerful and flexible Object-Relational Mapper (ORM) that allows us to work with our database using Python objects, abstracting away the underlying SQL.

-   **Database Engine:** SQLite
    -   *Reasoning:* A serverless, self-contained, transactional SQL database engine. It's perfect for our offline-first requirement, as the entire database is just a single file on the Raspberry Pi, requiring no separate server process.

-   **Database Migrations:** Alembic
    -   *Reasoning:* A lightweight database migration tool for SQLAlchemy. It allows us to manage and version our database schema over time, making it easy to apply changes as our data models evolve.

## 2. AI & Audio

-   **AI Model:** Gemma 3n
    -   *Reasoning:* The core of our project. Its on-device, offline, and multimodal (text, audio) capabilities are the central pillar of the system's functionality. We will leverage it for Speech-to-Text (STT), core reasoning/response generation, and Text-to-Speech (TTS).

-   **Model Server:** Ollama
    -   *Reasoning:* Provides a simple, reliable way to serve and manage LLMs like Gemma locally. It exposes a consistent, OpenAI-compatible API for model interaction, simplifying development and allowing for easier model swapping and management between development (macOS) and deployment (Raspberry Pi).

-   **AI Client Library:** OpenAI Python Library
    -   *Reasoning:* The official, well-supported library for interacting with OpenAI-compatible APIs. Using it to communicate with our local Ollama server is the cleanest and most robust method.

-   **Audio I/O:** PyAudio
    -   *Reasoning:* Provides Python bindings for PortAudio, the cross-platform I/O library. It allows us to easily interface with USB sound cards and other audio hardware to capture and play back audio.

-   **Voice Activity Detection (VAD):** webrtcvad
    -   *Reasoning:* A high-quality, low-overhead VAD library originating from the WebRTC project. It is effective for distinguishing between speech and silence, which is essential for segmenting audio from a continuous radio transmission.

## 3. Frontend

-   **Framework:** Vue.js 3
    -   *Reasoning:* A progressive and approachable JavaScript framework. Its component-based architecture is ideal for building a modular and maintainable user interface. The Composition API in Vue 3 makes managing complex state for our real-time dashboard more straightforward.

-   **Build Tool:** Vite
    -   *Reasoning:* A next-generation frontend build tool that provides an extremely fast development experience with features like Hot Module Replacement (HMR). It's the recommended build tool for modern Vue.js applications.

-   **API Communication:** Axios
    -   *Reasoning:* A promise-based HTTP client for the browser. It simplifies making requests to our FastAPI backend.

-   **Real-time Communication:** Native WebSockets
    -   *Reasoning:* We will use the browser's native WebSocket API to connect to our FastAPI backend for real-time updates, which is efficient and requires no extra client-side libraries.

## 4. Project Tooling & DevOps

-   **Version Control:** Git
    -   *Reasoning:* The industry standard for version control.

-   **Package Management:** pip & `requirements.txt`
    -   *Reasoning:* The standard Python package manager. We will use a `requirements.txt` file to ensure our environment is reproducible.

-   **Virtual Environment:** venv
    -   *Reasoning:* The standard tool for creating isolated Python environments, preventing dependency conflicts.
