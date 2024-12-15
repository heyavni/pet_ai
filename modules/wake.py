import pvporcupine
import pyaudio
import struct

def listen_for_wake_word():
    # Your Picovoice Access Key (replace this with your actual key)
    access_key = "xbfr5nzomftwtaDOJxjFxoRzMamu7uqDoj3M2W0UcGoFndTacbBgow=="

    # Path to your Porcupine model
    keyword_file_path = "/Users/avnisoni/pup_ai/resources/wake_up_models/Hey-Pup_en_mac_v3_0_0/Hey-Pup_en_mac_v3_0_0.ppn"

    # Initialize Porcupine with the custom keyword model and access key
    porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[keyword_file_path])

    # Open the microphone stream
    audio = pyaudio.PyAudio()

    # Use the exact frame length from Porcupine
    frames_per_buffer = porcupine.frame_length
    print(f"Porcupine frame length: {frames_per_buffer}")

    # Open stream with sample rate and buffer length matching the Porcupine configuration
    stream = audio.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=frames_per_buffer
    )

    print("Listening for wake word...")

    try:
        while True:
            # Read audio frame
            pcm_data = stream.read(frames_per_buffer, exception_on_overflow=False)
            
            # Convert audio data to the format Porcupine expects
            pcm = struct.unpack_from("h" * frames_per_buffer, pcm_data)

            # Process the audio frame to detect the wake word
            result = porcupine.process(pcm)

            # If the wake word is detected, print a message
            if result >= 0:
                print("Wake word detected!")
                return True

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Clean up resources
        stream.close()
        audio.terminate()
        porcupine.delete()

    return False

