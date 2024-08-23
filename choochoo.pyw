import mido
import pygame
import tkinter as tk
import os
import customtkinter as ctk
import sys
from tkinter import messagebox
from PIL import Image, ImageTk

# Start pygame for the choo choo sounds
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"bruh: {e}", file=sys.stderr)
    sys.exit(1)

class MidiPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("The Shawnee Heights HS choo choo machine 9000!!!")

        # Prevent window resizing
        self.master.resizable(False, False)  # Disable resizing so the photo doesn't get messed up lmao
        self.master.geometry("830x550")  # width x height

        # Paths to audio files
        self.audio_file_93 = os.path.join(os.path.dirname(__file__), "sample 1.mp3")
        self.audio_file_95 = os.path.join(os.path.dirname(__file__), "sample 2.mp3")
        self.audio_file_96 = os.path.join(os.path.dirname(__file__), "sample 3.mp3")
        self.audio_file_98 = os.path.join(os.path.dirname(__file__), "sample 4.mp3")
        self.audio_file_100 = os.path.join(os.path.dirname(__file__), "sample 5.mp3")
        self.audio_file_101 = os.path.join(os.path.dirname(__file__), "sample 6.mp3")
        self.audio_file_103 = os.path.join(os.path.dirname(__file__), "sample 7.mp3")
        self.audio_file_105 = os.path.join(os.path.dirname(__file__), "sample 8.mp3")
        self.audio_file_107 = os.path.join(os.path.dirname(__file__), "sample 9.mp3")
        self.audio_file_108 = os.path.join(os.path.dirname(__file__), "sample 10.mp3")

        # List of all audio files
        self.audio_files = [
            (self.audio_file_93, 93, "Sample 1"),
            (self.audio_file_95, 95, "Sample 2"),
            (self.audio_file_96, 96, "Sample 3"),
            (self.audio_file_98, 98, "Sample 4"),
            (self.audio_file_100, 100, "Sample 5"),
            (self.audio_file_101, 101, "Sample 6"),
            (self.audio_file_103, 103, "Sample 7"),
            (self.audio_file_105, 105, "Sample 8"),
            (self.audio_file_107, 107, "Sample 9"),
            (self.audio_file_108, 108, "Sample 10")
        ]

        self.buttons = {}
        self.error_buttons = []
        self.currently_playing = None
        self.played_sounds = set()  # Keep track of sounds that've been played

        # Create the main frame for buttons
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a frame for the color explanation and image
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Create the color explanation label
        self.color_explanation_label = ctk.CTkLabel(
            self.top_frame,
            text="Grey = Not Played | Green = Currently Playing | Orange = Already Played",
            text_color="black",
            font=("Arial", 12)  # Adjust font size if needed
        )
        self.color_explanation_label.pack(pady=(10, 5))  # Add padding below the label

        # Load and display the image
        self.image_path = os.path.join(os.path.dirname(__file__), "pic.png")
        self.load_and_display_image()

        # Create the buttons with the same color-changing logic as labels
        for audio_file, midi_note, display_name in self.audio_files:
            # Create a frame to hold both the button and the label side by side
            button_frame = tk.Frame(self.frame)
            button_frame.pack(pady=10)

            # Determine the button text and color
            if os.path.isfile(audio_file):
                button_text = f"Play {display_name}"
                fg_color = "grey"
                hover_color = "#404040"  # Darker grey for hover
            else:
                button_text = f"Bruh, where is {display_name}?? WHERE IS ITT????!!!"
                fg_color = "red"
                hover_color = "#a00a00"  # Darker red for hover
                self.error_buttons.append(midi_note)

            # Create the playback button with text
            play_button = ctk.CTkButton(
                button_frame,
                text=button_text,
                command=lambda af=audio_file, mn=midi_note: self.play_audio_file(af, mn),
                fg_color=fg_color,
                width=200,  # Adjust the width if needed
                hover_color=hover_color  # Set the hover color
            )
            play_button.pack(side=tk.LEFT, padx=5)  # Position the button to the left
            self.buttons[midi_note] = play_button

        # Reset button
        self.color_change_button = ctk.CTkButton(self.frame, text="Reset Button Colors", command=self.change_button_colors)
        self.color_change_button.pack(pady=10)

        # Stop playback button
        self.stop_button = ctk.CTkButton(
            self.frame, 
            text="Stop Playback", 
            command=self.stop_playback,
            fg_color="red",  # Set foreground color (button color) to red
            text_color="white",  # Set text color to white
            hover_color="#c00"  # Set hover color to a slightly darker red
        )
        self.stop_button.pack(pady=10)

        # Start MIDI listener
        self.start_midi_listener()

    def change_button_colors(self):
        for midi_note in self.buttons:
            if midi_note == 101:  # sample 6
                self.update_button_color(midi_note, "red", "#a00a00")  # Darker red for hover
            else:
                self.update_button_color(midi_note, "grey", "#404040")  # Darker grey for hover

    def stop_playback(self):
        pygame.mixer.music.stop()
        if self.currently_playing is not None:
            self.update_button_color(self.currently_playing, "orange", "#cc8400")  # Darker orange for hover
        self.currently_playing = None

    def load_and_display_image(self):
        try:
            # Load n' convert
            image = Image.open(self.image_path)
            photo = ImageTk.PhotoImage(image)
            # Empty label lmao
            image_label = tk.Label(self.top_frame, image=photo)
            image_label.image = photo  # Reference
            image_label.pack(pady=10)
        except Exception as e:
            print(f"", file=sys.stderr)

    def play_audio_file(self, audio_file, midi_note):
        try:
            # Halt!
            if self.currently_playing is not None:
                # If there's already a sound playing, set its button to orange
                self.update_button_color(self.currently_playing, "orange", "#cc8400")  # Darker orange for hover
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            self.update_button_color(midi_note, "#009900", "green")  # Darker green for hover
            self.played_sounds.add(midi_note)
            self.currently_playing = midi_note
            self.master.after(100, self.check_music_playback)  # Double check
        except pygame.error as e:
            print(f"Failed to play MP3 file {audio_file}: {e}", file=sys.stderr)

    def check_music_playback(self):
        if not pygame.mixer.music.get_busy():  # Check for choo choo sounds playing
            if self.currently_playing is not None:
                self.update_button_color(self.currently_playing, "orange", "#cc8400")  # Darker orange for hover
            self.currently_playing = None
        else:
            self.master.after(100, self.check_music_playback)  # KEEP checking

    def update_button_color(self, midi_note, color, hover_color):
        if midi_note in self.buttons:
            button = self.buttons[midi_note]
            button.configure(fg_color=color, hover_color=hover_color)

    def start_midi_listener(self):  # Skill issue handling
        try:
            input_names = mido.get_input_names()
            if input_names:
                self.midi_input = mido.open_input(input_names[0])
                self.master.after(100, self.check_midi_input)
                print(f"GOOD JOB JOA!! YOU REMEMBERED TO CONNECT THE KEYBOARD")
            else:
                print("You had ONE JOB: Plug the keyboard into the laptop!", file=sys.stderr)
                messagebox.showerror("womp womp", "You had ONE JOB: Plug the keyboard into the laptop!")
        except Exception as e:
            print(f"womp womp", file=sys.stderr)
            messagebox.showerror("MIDI Error", f"You had ONE JOB: Plug the keyboard into the laptop!")

    def check_midi_input(self):  # Man, what is all this brainrot ah videos on my feed??
        if hasattr(self, 'midi_input'):
            try:
                for msg in self.midi_input.iter_pending():
                    if msg.type == 'note_on' and msg.velocity > 0:
                        for audio_file, midi_note, _ in self.audio_files:
                            if msg.note == midi_note:
                                self.play_audio_file(audio_file, midi_note)
                                break  # in half lol
            except Exception as e:  # Need this oops
                print(f"bruh, something messed up... try again??", file=sys.stderr)
        self.master.after(90, self.check_midi_input)

# Degrees haha get it, cuz it's like... line 180, and I said degrees in a comment
if __name__ == "__main__":
    root = ctk.CTk()
    app = MidiPlayerApp(root)
    root.mainloop()
