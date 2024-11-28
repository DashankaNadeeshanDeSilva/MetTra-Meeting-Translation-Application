# Transcription service

import numpy as np
import difflib
import tempfile
import whisper
import logging
import librosa
from scipy.signal import resample_poly

logging.basicConfig(level=logging.INFO)


class Transcribe_Audio:
	def __init__(self):

		self.model = whisper.load_model("base")

		self.MIN_CHUNK_DURATION = 1 # initial chunk duration in seconds
		self.MAX_CHUNK_DURATION = 2
		self.SAMPLE_RATE = 16000
		self.SILENT_THRESHOLD = 0.01

		self.chunk_duration = self.MIN_CHUNK_DURATION
		self.previous_transcription = ""


	def get_audio_chunk(self, buffer):
		"""Extract audio chunckfrp, buffer and dynamically adjest chunk duration"""
			
		if np.abs(buffer).mean() > self.SILENT_THRESHOLD:
			logging.info(f"Speech is NOT silent and its length is: {len(buffer)/(self.SAMPLE_RATE*4)}")
			
			audio_data = self.preprocess_data(buffer)
			logging.info(f"Audio after preprocessing length is: {len(audio_data)/self.SAMPLE_RATE}")

			# process chunks dynamically according to chunk duration (sample rate for processing)
			if len(audio_data) >= self.chunk_duration * self.SAMPLE_RATE:
				buffer.clear()
				# Adjest the chunk duration for long spoken segements by gradually increasing the length
				self.chunk_duration = min(self.MAX_CHUNK_DURATION, self.chunk_duration + 1)
				logging.info(f"chunk_duration: {self.chunk_duration}")
				return audio_data
			else:
				logging.info("Speech is there but less than minimum duration !")
		else:
			buffer.clear()
			# brings back chunk duration to minimum duration to avoid missing small audio segments in the next iter
			self.chunk_duration = self.MIN_CHUNK_DURATION
			logging.info("Speech is silent !")
			return None


	def preprocess_data(self, buffer):

		# transform buffer byte array audio to array and normalize to
		audio_data = np.frombuffer(buffer, dtype=np.float32)

		# Convert to mono
		# audio_data = librosa.to_mono(audio_data)

		# Normalize audio again after resampling
		if np.max(np.abs(audio_data)) > 0:
			audio_data = audio_data / np.max(np.abs(audio_data))

		return audio_data


	def transcribe_audio(self, buffer):
		"""transcribe audio data from buffer"""

		audio_data = self.get_audio_chunk(buffer)
		
		# return None for silent audio
		if audio_data is None:
			return None
		
		transcription_output = self.model.transcribe(audio_data, fp16=False)
		current_transcription = transcription_output["text"]

		transcription = self.stitch_transcription(self.previous_transcription, current_transcription)
		self.previous_transcription = current_transcription

		return transcription
		
		
	def stitch_transcription(self, prev_trans, curr_trans):
		""" find and remove overlap between transcripts based on previous transcription.
			note: This method belongs to the class but does not require access to the instance, and can be called 
			directly on the class without creating an instance and does not modify or rely on class or instance data.
		"""
		
		overlap = difflib.SequenceMatcher(None, prev_trans, curr_trans).find_longest_match(0, len(prev_trans), 
			0, len(curr_trans)
		)
		
		# case: overlap exists, remove overlap from current transcription
		if overlap.size > 0:
			return curr_trans[overlap.b + overlap.size :]
		# case: no overlap, output current transcription
		else:
			return curr_trans