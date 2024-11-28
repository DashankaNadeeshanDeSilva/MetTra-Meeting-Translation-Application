let websocket;
let isRecording = false;

const micButton = document.getElementById("mic-button");
const transcriptionText = document.getElementById("transcription-text");

// backend websocket URL
const BACKEND_WS_URL = "ws://localhost:8001/ws/real-time";

const SAMPLE_RATE = 16000; // Target sample rate
const CHUNK_DURATION = 1.0; // 0.5 or 1 seconds
let audioBuffer = [];

micButton.addEventListener("click", async () => {
  if (!isRecording) {
    startRecording();
  } else {
    stopRecording();
  }
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    console.log("Microphone access granted: ", stream);
    
    // Connect to backend WebSocket server for audio streaming
    websocket = new WebSocket(BACKEND_WS_URL);
    console.log("WebSocket initialization done.");

    websocket.onopen = () => {
      console.log("Connected to Backend WebSocket server.");
      micButton.classList.remove("mic-off");
      micButton.classList.add("mic-on");
      isRecording = true;

      const audioContext = new AudioContext({ sampleRate: SAMPLE_RATE });
      const source = audioContext.createMediaStreamSource(stream);
      const processor = audioContext.createScriptProcessor(4096, 1, 1);

      source.connect(processor);
      processor.connect(audioContext.destination);

      // Process audio in chunks
      processor.onaudioprocess = (e) => {
        const audioData = e.inputBuffer.getChannelData(0);
        audioBuffer.push(...audioData);

        if (audioBuffer.length >= SAMPLE_RATE * CHUNK_DURATION) {
          const chunk = new Float32Array(audioBuffer);
          audioBuffer = []; // Clear buffer after sending
          websocket.send(chunk.buffer);
          console.log("Audio chunk sent.");
        }
      };
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.transcription) {
        transcriptionText.textContent += `${data.transcription}\n`;
        micButton.classList.remove("mic-off");
        micButton.classList.add("mic-on"); // Turns the button green
        console.log("Transcription received");
      }else {
        console.log("No transcription in the message.");
      }
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
      stopRecording();
    };

    websocket.onclose = () => {
      console.log("WebSocket connection closed.");
      stopRecording();
    };

  } catch (error) {
    console.error("Error accessing microphone:", error);
  }
}

function stopRecording() {
  if (websocket) {
    websocket.close();
  }
  micButton.classList.remove("mic-on");
  micButton.classList.add("mic-off");
  isRecording = false;
}
