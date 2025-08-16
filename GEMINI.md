## Project Overview

This project, named "Suna" (or Kortix), is an open-source generalist AI Worker platform. It demonstrates the capabilities of the Kortix platform by providing a versatile AI worker that can perform tasks such as web research, browser automation, file and document management, data processing and analysis, and system administration. The platform also enables users to build and deploy their own specialized AI agents for various domains like customer service, content creation, sales & marketing, and research & development.

### Architecture:

The project follows a microservices architecture, primarily composed of:

*   **Backend API:** A Python-based FastAPI service responsible for agent orchestration, thread management, LLM integration (via LiteLLM), and an extensible tool system.
*   **Frontend Dashboard:** A Next.js/React application providing a comprehensive user interface for agent management, configuration, workflow building, and monitoring.
*   **Agent Runtime:** Isolated Docker execution environments for each agent instance, offering capabilities like browser automation, code interpretation, and secure sandboxing.
*   **Database & Storage:** Utilizes Supabase for authentication, user management, agent configurations, conversation history, file storage, and real-time analytics.
*   **Message Queue:** Uses Redis as a message broker for background tasks and inter-service communication.

## Building and Running

This project is designed to be run using Docker and Docker Compose, which orchestrates all the necessary services.

### Prerequisites:

*   Docker
*   Docker Compose

### Setup:

1.  **Environment Variables:**
    *   Create a `.env` file in the `backend/` directory based on `backend/.env.example`.
    *   Create a `.env.local` file in the `frontend/` directory based on `frontend/.env.example`.
    *   Ensure all necessary environment variables for Supabase, Redis, and other services are configured.

2.  **Build and Run with Docker Compose:**
    Navigate to the project root directory and run:
    ```bash
    docker-compose up --build
    ```
    This command will:
    *   Build the Docker images for the `backend` and `frontend` services.
    *   Start all services defined in `docker-compose.yaml` (redis, backend, worker, frontend).

    The backend API will be accessible at `http://localhost:8000` and the frontend dashboard at `http://localhost:3000`.

### Individual Service Commands (for development/debugging):

#### Backend:

*   **Install dependencies (using `uv`):**
    ```bash
    cd backend
    uv sync
    ```
*   **Run the FastAPI application (development mode):**
    ```bash
    cd backend
    uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000
    ```
*   **Run the Dramatiq worker:**
    ```bash
    cd backend
    uv run dramatiq --skip-logging --processes 4 --threads 4 run_agent_background
    ```

#### Frontend:

*   **Install dependencies (using `npm`):**
    ```bash
    cd frontend
    npm install
    ```
*   **Run the Next.js development server:**
    ```bash
    cd frontend
    npm run dev
    ```
*   **Build the Next.js application:**
    ```bash
    cd frontend
    npm run build
    ```
*   **Start the Next.js production server (after building):**
    ```bash
    cd frontend
    npm run start
    ```

## Development Conventions

### Python (Backend):

*   **Dependency Management:** `uv` is used for managing Python dependencies, with `pyproject.toml` and `uv.lock` defining the project's dependencies.
*   **Framework:** FastAPI for building REST APIs.
*   **Code Formatting:** (Implicit, but common for Python projects) Adherence to PEP 8 guidelines.

### TypeScript/JavaScript (Frontend):

*   **Framework:** Next.js with React.
*   **Dependency Management:** `npm` is used for managing Node.js dependencies, with `package.json` and `package-lock.json`.
*   **Styling:** Tailwind CSS for utility-first styling.
*   **UI Components:** Utilizes Radix UI for unstyled, accessible components, likely combined with `shadcn/ui` for pre-built components.
*   **State Management:** `zustand` for client-side state management.
*   **Data Fetching:** `@tanstack/react-query` for server state management and data fetching.
*   **Code Formatting:** `prettier` is configured for automatic code formatting (`npm run format`).
*   **Linting:** `eslint` is used for code linting (`npm run lint`).

### General:

*   **Containerization:** Docker and Docker Compose are central to the development and deployment workflow, ensuring consistent environments.
*   **Version Control:** Git is used for version control, with a `.gitignore` file to exclude unnecessary files.
*   **Contribution Guidelines:** Refer to `CONTRIBUTING.md` for detailed contribution guidelines.
