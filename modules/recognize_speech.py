import speech_recognition as sr


def recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Open microphone for speech recognition
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the speech



    try:
        # Use Google's speech recognition API to convert speech to text
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
