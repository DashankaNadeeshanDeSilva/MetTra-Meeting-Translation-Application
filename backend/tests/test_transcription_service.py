# Unit test for transcription function
"""
Tests for isolated components of transcription service
- Mock dependencies by loading whisper more and behavior Address edge cases
"""

import pytest
import numpy as np

from app.services.transciption_service import transcribe_audio_bytes

'''
# load sample audio file
with open("resources/sample.wav", "rb") as f:
	audio = f.read()

# call transcription function
transcrber = Transcribe_Audio()
transcription = transcrber.transcribe_audio(audio)

print("Transcription: ", transcription)
'''


@pytest.fixture
def transcriber():
	"""fixture to init the Transcribe_Audio class"""
	return Transcribe_Audio()


def test_get_audio_chunk_with_speech(transcriber):
	"""test get_audio_chunk() with valid speech audio data"""
	# simulate audio data above silent thershold
	audio_data = np.random.randn(16000).astype(np.float32) * 0.1 
	'''multiplication by 0.1 ensures the generated audio data has 
	amplitudes that better mimic real audio signals in terms of scale'''
	buffer = bytearray(audio_data.tobytes()) # convert to byte array

	chunk = transcriber.get_audio_chunk(buffer)
	assert chunk is not None # outputs audio
	assert len(chunk) == 16000 # 1 second of audio at 16kHz


def test_get_audio_chunk_with_silance(transcriber):
	"""test get_audio_chunk() with silent audio data"""
	# simulate audio data above silent thershold
	audio_data = np.zeros(16000).astype(np.float32) * 0.1
	buffer = bytearray(audio_data.tobytes())

	chunk = transcriber.get_audio_chunk(buffer)
	assert chunk is None # outputs None for silence
	assert transcriber.chunk_duration == transcriber.MIN_CHUNK_DURATION


def test_stitch_transcription_with_overlap(transcriber):
	"""test stitch_transcription() with overlapping text"""

	prev = "The quick brown fox jumps over"
    curr = "over the lazy dog and runs away"

    stitched = transcriber.stitch_transcription(prev, curr)
    assert stitched == "the lazy dog and runs away"


 def test_stitch_transcription_without_overlap(transcriber):
	"""test stitch_transcription() without overlapping text"""

	prev = "The quick brown fox"
    curr = "The hen came out of the nest"

    stitched = transcriber.stitch_transcription(prev, curr)
    assert stitched == curr


def test_transcribe_audio_mocked(mocker, transcriber):
	"""test transcribe_audio() with mocked whisper model"""
	'''goal: isolates the test to only the transcribe_audio method's logic, 
	ensuring it behaves correctly regardless of actual Whisper model implementation.'''
	# Mock Whisper model output
    mock_model = mocker.patch("app.services.transcription_service.whisper")
    '''this replaces the real Whisper model (used in transcription_service) 
    with a mock object for the duration of the test that ensures the test 
    does not rely on the actual Whisper model'''
    mock_model.load_model.return_value.transcribe.return_value = {"text": "Test transcription"}
    '''Specifies the behavior of the mocked Whisper model's methods:
	when load_model is called, it returns an object whose transcribe method 
	always returns the dictionary {"text": "Test transcription"} which simulates 
	the output of a successful transcription without actually running the model.'''
	# Simulate audio buffer
	audio_data = np.random.randn(16000).astype(np.float32) * 0.1
	buffer = bytearray(audio_data.tobytes())

	transcription = transcriber.transcrbe_audio(buffer)
	assert transcription == "Test transcription"