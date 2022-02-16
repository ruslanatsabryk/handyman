import time

def start_browser():
    print("Browser started")

def start_vs_code():
    print("VS Code started")

def shutdown_computer():
    print("Computer shutting down")

def stop_listening(listener, talker):
    time.sleep(.5)
    talker.say("By-by my dear friend!")
    talker.runAndWait()
    exit()