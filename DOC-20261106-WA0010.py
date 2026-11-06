"""Jarvis: a small voice assistant.

Uses your microphone and speakers when `SpeechRecognition`, `PyAudio` and
`pyttsx3` are installed. Otherwise it falls back to typing in the terminal.
"""
import datetime
import urllib.parse
import webbrowser

try:
    import pyttsx3
    _engine = pyttsx3.init()
except Exception:
    _engine = None

try:
    import speech_recognition as sr
except Exception:
    sr = None

SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
}


def speak(text):
    print(f"Jarvis: {text}")
    if _engine:
        _engine.say(text)
        _engine.runAndWait()


def voice_available():
    if sr is None:
        return False
    try:
        sr.Microphone()
        return True
    except Exception:
        return False


def listen(use_voice):
    """Return the next command as lowercase text ('' if nothing was heard)."""
    if not use_voice:
        return input("You: ").strip().lower()
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        text = recognizer.recognize_google(audio).lower()
        print(f"You: {text}")
        return text
    except Exception:
        return ""


def handle(command):
    """Run one command. Return False when Jarvis should quit."""
    if not command:
        return True
    if any(w in command for w in ("exit", "quit", "goodbye", "bye")):
        speak("Goodbye!")
        return False
    if "time" in command:
        speak(datetime.datetime.now().strftime("It is %I:%M %p."))
    elif "date" in command or "today" in command:
        speak(datetime.datetime.now().strftime("Today is %A, %d %B %Y."))
    elif command.startswith(("search for ", "search ")):
        query = command.split("search", 1)[1].replace("for", "", 1).strip()
        if query:
            speak(f"Searching for {query}.")
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))
        else:
            speak("What should I search for?")
    elif command.startswith("open "):
        name = command[5:].strip()
        if name in SITES:
            speak(f"Opening {name}.")
            webbrowser.open(SITES[name])
        else:
            speak(f"I don't know how to open {name} yet.")
    elif "help" in command:
        speak("Try: what time is it, what is the date, search for something, "
              "open youtube, or say goodbye.")
    elif any(w in command for w in ("hello", "hi", "hey")):
        speak("Hello! How can I help?")
    else:
        speak("Sorry, I didn't understand that. Say help to see what I can do.")
    return True


def main():
    use_voice = voice_available()
    mode = "voice" if use_voice else "text"
    speak(f"Jarvis online in {mode} mode. Say help to see what I can do.")
    try:
        while handle(listen(use_voice)):
            pass
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
