""" 
Handle WebSocket-based API (REST) endpoint for handling real-time audio data processing

## in Server side ##

Funtion: The defined WebSocket endpoint will recieve audio from frontend, then process the audio
ans send back output. Utlizes transcription (transcribe from audio) and translation services.
Websocket handles continuous bi-directional communication between server and client.
Suitable for modular and asynchronous approach ensures low-latency, scalable processing for real-time applications.

Additonal:
- APIRouter: FastAPI utility to orga and manage API routes, which allows the router to be modular and integrated into the main app.
- Websocket: ENables an bi-directional communication between client and server

"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.transcription_service import Transcribe_Audio
import logging
import numpy as np


# configure logging
logging.basicConfig(level=logging.INFO)

# define router; all routers will have "ws" prefix
router = APIRouter()

# create transcription service instance
transcriber = Transcribe_Audio()


# define WebSocker endpoint (path: "ws/real-time-running")
@router.websocket("/ws/real-time")
async def websocket_endpoint(websocket: WebSocket):
	logging.info("Router connected")
	# wait until the WebSocket connection is established
	await websocket.accept() 

	# buffer to store audio chunks streamed from websocket
	buffer = bytearray()

	try:
		while True:
			# Receive audio data from frontend
			audio_packet = await websocket.receive_bytes()
			buffer.extend(audio_packet) # aacumulate data

			# Check if buffer size is sufficient for transcription
			if len(buffer) >= transcriber.chunk_duration * transcriber.SAMPLE_RATE * 4:
				logging.info(f"Buffer length: {len(buffer)/(transcriber.SAMPLE_RATE*4)}")
				# transcribe audio
				transcription = transcriber.transcribe_audio(buffer)

				if transcription: 
					# send processed transcription back to the frontend
					await websocket.send_json({"transcription": transcription})
					logging.info(f"Transcription: {transcription}")
					logging.info("")
				else:
					logging.info("No transcription generated.")
					logging.info("")
				# The buffer is only cleared after processing to avoid prematurely discarding unprocessed data.
				buffer.clear()

	# handle if WebSocket connection is closed or the client disconnects.
	except WebSocketDisconnect:
		logging.info("Client disconnected")
	# exception handling
	except Exception as e:
		logging.error(f"An error occured: {e}")