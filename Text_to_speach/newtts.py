import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pyttsx3
import threading

def save_as_mp3():
    text = text_entry.get("1.0", tk.END)
    filename = filename_entry.get()
    if not filename.endswith(".mp3"):
        filename += ".mp3"
    engine.save_to_file(text, filename)
    engine.runAndWait()
    status_label.config(text=f"Saved as {filename}")

def play():
    text = text_entry.get("1.0", tk.END)
    t = threading.Thread(target=play_thread, args=(text,))
    t.start()

def play_thread(text):
    engine.say(text)
    engine.runAndWait()

def pause():
    engine.stop()

def show_voice_settings():
    popup = tk.Toplevel(window)
    popup.title("New Voice Settings")
    popup.geometry("400x400")

    voice_name_label = tk.Label(popup, text="Voice Name:")
    voice_name_label.pack()
    voice_name_entry = tk.Entry(popup)
    voice_name_entry.pack()

    language_label = tk.Label(popup, text="Language:")
    language_label.pack()
    language_entry = tk.Entry(popup)
    language_entry.pack()

    gender_label = tk.Label(popup, text="Gender:")
    gender_label.pack()
    gender_entry = tk.Entry(popup)
    gender_entry.pack()

    pitch_label = tk.Label(popup, text="Pitch:")
    pitch_label.pack()
    pitch_scale = tk.Scale(popup, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
    pitch_scale.set(1.0)
    pitch_scale.pack(pady=5)

    speed_label = tk.Label(popup, text="Speed:")
    speed_label.pack()
    speed_scale = tk.Scale(popup, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
    speed_scale.set(1.0)
    speed_scale.pack(pady=5)

    volume_label = tk.Label(popup, text="Volume:")
    volume_label.pack()
    volume_scale = tk.Scale(popup, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
    volume_scale.set(1.0)
    volume_scale.pack(pady=5)

    emphasis_label = tk.Label(popup, text="Emphasis:")
    emphasis_label.pack()
    emphasis_scale = tk.Scale(popup, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
    emphasis_scale.set(50)
    emphasis_scale.pack(pady=5)

    # Add more settings as needed

    def save_new_voice():
        voice_name = voice_name_entry.get()
        language = language_entry.get()
        gender = gender_entry.get()
        pitch = pitch_scale.get()
        speed = speed_scale.get()
        volume = volume_scale.get()
        emphasis = emphasis_scale.get()

        # Save the new voice with the specified settings
        # Custom logic to save the voice and add it to the list of available voices

        messagebox.showinfo("New Voice", "Voice saved successfully.")

    save_button = tk.Button(popup, text="Save Voice", command=save_new_voice)
    save_button.pack(pady=10)

def update_settings():
    rate = int(rate_scale.get())
    volume = float(volume_scale.get())
    pitch = float(pitch_scale.get())
    speed = float(speed_scale.get())
    voice_id = voices_listbox.get(tk.ACTIVE)
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    engine.setProperty("pitch", pitch)
    engine.setProperty("speed", speed)
    engine.setProperty("voice", voice_id)

engine = pyttsx3.init()

# Create GUI
window = tk.Tk()
window.title("Text-to-Speech Tool")

# Create a frame for the controls
controls_frame = tk.Frame(window)
controls_frame.pack(padx=20, pady=20)

text_label = tk.Label(controls_frame, text="Text:")
text_label.pack()
text_entry = scrolledtext.ScrolledText(controls_frame, height=10, width=50)
text_entry.pack(pady=10)

filename_label = tk.Label(controls_frame, text="Filename:")
filename_label.pack()
filename_entry = tk.Entry(controls_frame)
filename_entry.pack(pady=5)

save_button = tk.Button(controls_frame, text="Save as MP3", command=save_as_mp3)
save_button.pack(pady=5)

play_button = tk.Button(controls_frame, text="Play", command=play)
play_button.pack(pady=5)

pause_button = tk.Button(controls_frame, text="Pause", command=pause)
pause_button.pack(pady=5)

rate_label = tk.Label(controls_frame, text="Speech Rate:")
rate_label.pack()
rate_scale = tk.Scale(controls_frame, from_=50, to=200, orient=tk.HORIZONTAL, length=200)
rate_scale.set(100)
rate_scale.pack(pady=5)

volume_label = tk.Label(controls_frame, text="Volume:")
volume_label.pack()
volume_scale = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
volume_scale.set(1.0)
volume_scale.pack(pady=5)

pitch_label = tk.Label(controls_frame, text="Pitch:")
pitch_label.pack()
pitch_scale = tk.Scale(controls_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
pitch_scale.set(1.0)
pitch_scale.pack(pady=5)

speed_label = tk.Label(controls_frame, text="Speed:")
speed_label.pack()
speed_scale = tk.Scale(controls_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
speed_scale.set(1.0)
speed_scale.pack(pady=5)

voices_label = tk.Label(controls_frame, text="Voices:")
voices_label.pack()
voices_listbox = tk.Listbox(controls_frame, selectmode=tk.SINGLE)
voices_listbox.pack(pady=5)

# Fetch and populate available voices
voices = engine.getProperty("voices")
for voice in voices:
    voices_listbox.insert(tk.END, voice.id)

settings_button = tk.Button(controls_frame, text="Update Settings", command=update_settings)
settings_button.pack(pady=10)

new_voice_button = tk.Button(controls_frame, text="New Voice", command=show_voice_settings)
new_voice_button.pack(pady=10)

status_label = tk.Label(window, text="")
status_label.pack()

# Start GUI main loop
window.mainloop()
