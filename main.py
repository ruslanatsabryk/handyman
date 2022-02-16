import speech_recognition as sr
import pyttsx3
from tasks import *
import json

def load_tasks():
    with open("tasks.json") as t:
        task_list = json.load(t)
    return task_list


if __name__ == "__main__":

    tasks = load_tasks()
    
    # Listening parameters
    listener = sr.Recognizer()
    listener.energy_threshold = 1000  # 300 minimum audio energy to consider for recording
    listener.dynamic_energy_threshold = True  # True
    listener.dynamic_energy_adjustment_damping = 0.15 # 0.15
    listener.dynamic_energy_ratio = 1.5 # 1.5
    listener.pause_threshold = 0.6  # seconds of non-speaking audio before a phrase is considered complete
    listener.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
    listener.phrase_threshold = 0.3  # 0.3 minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    listener.non_speaking_duration = 0.5  # 0.5 seconds of non-speaking audio to keep on both sides of the recording

    talker = pyttsx3.init()
    talker.setProperty("rate", 150)
    
    # Set en-US voice for talker if avalable
    voices = talker.getProperty("voices")
    talker.setProperty("voice", voices[1].id)
    

    talker.say("Listen to you carifully my dear user!")
    talker.runAndWait()

    # Listening loop
    phrase_text = ''
    while True:
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source=source, duration=0.7)
                print("Ready to listen")
                phrase_voice = listener.listen(source)
                print("Wait please...")
                phrase_text = listener.recognize_google(phrase_voice, language="en-US")
                
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            listener = sr.Recognizer()
            phrase_text = ''
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            listener = sr.Recognizer()
            phrase_text = ''

        if phrase_text:
            print(f"You sad:\n - {phrase_text.capitalize()}")
            
            # Execute function by key from global dictionary
            for fun, v in tasks.items():
                if phrase_text in v:
                    globals()[fun]()
            phrase_text = ''
