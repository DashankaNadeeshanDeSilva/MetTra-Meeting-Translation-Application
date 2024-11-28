## Real-Time Speech Transcription and Translation

### Project Motivation, Goal, and Scope

#### Motivation:
As a foreigner working in Germany and still learning the language, I often face challenges during online meetings conducted in German. To make communication smoother and improve my understanding, I thought it would be helpful to have a tool that provides real-time translated transcriptions of the meeting in English (with my colleagues' consent). This project is a step toward bridging the language gap and enhancing collaboration in multilingual environments.

The goal of this project is to develop a real-time speech transcription and translation application capable of:

- Capturing speech in German.
- Transcribing the speech in real-time.
- Translating the transcription from German to English.

This application can be a valuable tool for breaking language barriers, facilitating communication in multilingual settings, and showcasing MLOps practices in deploying AI solutions.

### Project Architecture

The application consists of three main components:

#### Frontend:

- Captures audio from the user's microphone.
- Streams the audio to the backend in real-time using WebSocket.
- Displays the translated transcription received from the backend.

Technical Components:

- FastAPI: For handling WebSocket connections and API routes.
- OpenAI Whisper: For robust and accurate transcription of audio.
- Hugging Face Transformers: For translation of transcriptions.

#### Backend:

- Processes incoming audio chunks.
- Performs real-time transcription using OpenAI’s Whisper model.
- Translates the transcription from German to English using an NLP model.
- Communicates with the frontend via WebSocket.

Technical Components:

- WebSocket-based communication.
- AudioContext API: For capturing and processing microphone input.

#### Dockerization and CI/CD:

Both frontend and backend are containerized using Docker.
A CI/CD pipeline is implemented using GitHub Actions to automate testing, building, and deployment of the application.

### How the Application Works

Digram...

### How to Use/Run the Application

#### Prerequisites

- Install Docker Desktop
- Clone this repo

#### TO run locally

- Build Docker Images: ```docker-compose build```
- Run Docker Containers: ```docker-compose up```
- Access the Application:
    - Frontend: http://localhost:8080
    - Backend: http://localhost:8001

- Speak into the Microphone:
    - Click the microphone button on the frontend UI.
    - Speak in German and see the real-time transcription and translation into English.

- Stop the Application: ```docker-compose down```

### Challenges Faced

- WebSocket Connection for Audio: Establishing and maintaining real-time WebSocket connections between the frontend and backend posed challenges, especially with varying audio chunk sizes.
Handling Latency:

- Real-time transcription and translation required optimizing audio chunk durations and balancing computational efficiency.
Limitations with Computational Power:

- Whisper and translation models are resource-intensive. Running these on a CPU introduced latency, requiring smaller models and efficient chunk handling.



