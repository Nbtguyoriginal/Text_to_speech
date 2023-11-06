import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# Event to signal stop request
stop_event = threading.Event()

def read_text_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def load_file():
    filename = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if filename:
        text = read_text_file(filename)
        text_editor.delete('1.0', 'end')
        text_editor.insert('1.0', text)

def start_text_to_speech():
    global engine, stop_event
    stop_event.clear()  # Reset the stop event flag
    text = text_editor.get('1.0', 'end-1c')
    if text:
        # Create a separate thread for text-to-speech playback
        thread = threading.Thread(target=playback_text, args=(text,))
        thread.start()
    else:
        messagebox.showwarning('Warning', 'Please enter some text.')

def stop_text_to_speech():
    global stop_event
    stop_event.set()  # Set the stop event flag

def playback_text(text):
    global engine, stop_event
    # Get the modified speech properties from the GUI
    speed = speed_scale.get()
    tone = tone_scale.get()
    cadence = cadence_scale.get()

    # Apply the modified speech properties
    engine.setProperty('rate', speed)
    engine.setProperty('pitch', tone)
    engine.setProperty('volume', cadence)

    # Generate audio file for the text
    audio_file = "temp.wav"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()

    # Load the audio file and play
    audio = AudioSegment.from_file(audio_file, format="wav")
    play_audio = play(audio)

    # Check if stop event is set to stop playback
    while play_audio.is_playing() and not stop_event.is_set():
        pass

    play_audio.stop()  # Stop playback

    # Delete the temporary audio file
    os.remove(audio_file)

def on_close():
    stop_text_to_speech()
    window.destroy()

# Create the main window
window = tk.Tk()
window.title('Text-to-Speech')
window.protocol("WM_DELETE_WINDOW", on_close)

# Create a button to load the text file
load_button = tk.Button(window, text='Load Text File', command=load_file)
load_button.pack(pady=10)

# Create a text editor for entering text
text_editor = ScrolledText(window, height=10)
text_editor.pack(padx=10, pady=5)

# Create a section for modifying speech properties
properties_frame = tk.Frame(window)
properties_frame.pack(pady=5)

speed_label = tk.Label(properties_frame, text='Speed:')
speed_label.grid(row=0, column=0, padx=5)
speed_scale = tk.Scale(properties_frame, from_=50, to=400, orient='horizontal')
speed_scale.set(150)
speed_scale.grid(row=0, column=1, padx=5)

tone_label = tk.Label(properties_frame, text='Tone:')
tone_label.grid(row=0, column=2, padx=5)
tone_scale = tk.Scale(properties_frame, from_=0.5, to=2, resolution=0.1, orient='horizontal')
tone_scale.set(1)
tone_scale.grid(row=0, column=3, padx=5)

cadence_label = tk.Label(properties_frame, text='Cadence:')
cadence_label.grid(row=0, column=4, padx=5)
cadence_scale = tk.Scale(properties_frame, from_=0, to=1, resolution=0.1, orient='horizontal')
cadence_scale.set(1)
cadence_scale.grid(row=0, column=5, padx=5)

# Create a button to start text-to-speech
start_button = tk.Button(window, text='Start', command=start_text_to_speech)
start_button.pack(pady=5)

# Create a button to stop text-to-speech
stop_button = tk.Button(window, text='Stop', command=stop_text_to_speech)
stop_button.pack(pady=5)

# Start the GUI event loop
window.mainloop()
