import pygame
import threading
import tkinter as tk
from pynput import keyboard
import os

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Path to the folder where key sound files are stored
sound_folder = r'C:\ammunation'  # Replace with your folder path

# Map each key to its corresponding sound file (modify this as needed)
key_sounds = {
    'a': 'l.wav',
    'b': 'a.wav',
    
    # Add more key mappings as needed
}

# Load a default sound if no sound is defined for a key
default_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'a.wav'))  # Replace with a default sound

# Define the function that will be called when a key is pressed
def on_press(key):
    try:
        # Get the key name (e.g., 'a', 'b', etc.)
        key_name = key.char if hasattr(key, 'char') else str(key).replace('Key.', '').lower()

        # Get the sound file for the pressed key
        sound_file = key_sounds.get(key_name, 'l.wav')  # Default to 'default_key.wav' if no sound is mapped

        # Play the corresponding sound
        key_sound = pygame.mixer.Sound(os.path.join(sound_folder, sound_file))
        key_sound.play()
    except AttributeError:
        # Handle special keys (e.g., space, enter, shift, etc.)
        pass

# Listener function for the keyboard
def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# Stop the listener function
def stop_listener():
    global listener
    listener.stop()

# Create the GUI window
class KeyboardSoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Sound Listener")
        
        # Status label
        self.status_label = tk.Label(root, text="Not Listening", font=("Arial", 16))
        self.status_label.pack(pady=10)

        # Start button
        self.start_button = tk.Button(root, text="Start", font=("Arial", 14), command=self.start)
        self.start_button.pack(pady=5)

        # Stop button
        self.stop_button = tk.Button(root, text="Stop", font=("Arial", 14), command=self.stop)
        self.stop_button.pack(pady=5)

        # Disable stop button initially
        self.stop_button.config(state=tk.DISABLED)

    # Start button function
    def start(self):
        self.status_label.config(text="Listening...")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start listener in a separate thread
        threading.Thread(target=start_listener, daemon=True).start()

    # Stop button function
    def stop(self):
        self.status_label.config(text="Not Listening")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Stop the listener
        stop_listener()

# Create the main window and start the GUI loop
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardSoundApp(root)
    root.mainloop()
