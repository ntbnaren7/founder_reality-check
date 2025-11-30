# Founder Reality-Check Agent

An AI agent that helps early-stage founders reality-check their startup ideas by enforcing concrete users, specific channels, and structured hypotheses.

## Features
- **Startup Snapshot**: Tracks the evolution of a startup idea.
- **Validation**: Enforces concrete target users and executable distribution channels.
- **Drift Detection**: Highlights major pivots vs. minor refinements between sessions.
- **Experiment Generation**: Suggests minimal tests to validate hypotheses.

## Prerequisites
- **Conda**: Ensure you have conda installed.
- **Python 3.11**: This project uses the `smartpricing311` environment (or create one with `conda create -n py311 python=3.11`).
- **Node.js**: For the frontend.
- **Google Gemini API Key**: Set `GOOGLE_API_KEY` in your environment variables.

## Setup & Running

### 1. Backend
1. Open a terminal.
2. Activate the conda environment:
   ```bash
   conda activate smartpricing311
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run the server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### 2. Frontend
1. Open a new terminal.
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the dev server:
   ```bash
   npm run dev
   ```
5. Open your browser to `http://localhost:5173`.

## Usage
1. Enter a **Startup ID** (e.g., `my-startup`).
2. Describe your idea. Be specific!
   - **Bad**: "Uber for cats."
   - **Good**: "On-demand cat grooming for busy tech professionals in San Francisco, acquired via local vet partnerships."
3. Click **Run Reality Check**.
4. Review the feedback, status, and proposed experiments.
5. Come back later with updates to see **Drift Detection** in action.

## Testing
Run backend tests:
```bash
conda activate smartpricing311
pytest backend/tests
```
