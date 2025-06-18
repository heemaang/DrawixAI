import os
import uuid
from groq import Groq

# Load the Groq client using API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe(audio_bytes: bytes) -> dict:
    """
    Transcribe audio bytes using Groq's Whisper model and simulate diarization.

    Args:
        audio_bytes (bytes): The audio file content in bytes

    Returns:
        dict: Structured transcription with simulated speaker diarization
    """
    # Use unique file name to avoid conflicts
    temp_path = f"temp_{uuid.uuid4()}.mp3"

    try:
        # Save the audio bytes to a temporary file
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)

        # Call Groq Whisper with verbose JSON output
        with open(temp_path, "rb") as file:
            response = client.audio.transcriptions.create(
                file=(temp_path, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json"
            )

        # Simulate diarization by alternating speakers
        diarized_segments = []
        speaker_toggle = True
        for seg in response["segments"]:
            speaker = "Speaker 1" if speaker_toggle else "Speaker 2"
            speaker_toggle = not speaker_toggle
            diarized_segments.append({
                "speaker": speaker,
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"]
            })

        return {
            "text": response["text"],
            "language": response["language"],
            "duration": response["duration"],
            "segments": diarized_segments
        }

    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

    finally:
        # Clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

# import os
# from groq import Groq

# # Load the Groq client using API key from environment
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def transcribe(audio_bytes: bytes) -> str:
#     """
#     Transcribe audio bytes using Groq's Whisper model.
#     Args:
#         audio_bytes (bytes): The audio file content in bytes
#     Returns:
#         str: The transcribed text
#     """
#     temp_path = "temp_audio.mp3"
#     try:
#         # Save the audio bytes to a temporary file
#         with open(temp_path, "wb") as f:
#             f.write(audio_bytes)

#         # Open and send the file to Groq for transcription
#         with open(temp_path, "rb") as file:
#             response = client.audio.transcriptions.create(
#                 file=(temp_path, file.read()),
#                 model="whisper-large-v3",
#                 response_format="text"
#             )

#         return response  # This will be plain text as string

#     except Exception as e:
#         raise Exception(f"Transcription failed: {str(e)}")

#     finally:
#         # Always remove the temp file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
