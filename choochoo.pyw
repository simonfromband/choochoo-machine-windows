import mido
import pygame
import tkinter as tk
import os
import customtkinter as ctk
import sys
from tkinter import messagebox
from PIL import Image, ImageTk

# start pygame for the choo choo sounds
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
        self.master.resizable(False, False)  # Disable resizing so the photo doesnt get messed up lmao
        self.master.geometry("750x500")  # width x height)

        # paths
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
            (self.audio_file_93, 93, "sample 1.mp3"),
            (self.audio_file_95, 95, "sample 2.mp3"),
            (self.audio_file_96, 96, "sample 3.mp3"),
            (self.audio_file_98, 98, "sample 4.mp3"),
            (self.audio_file_100, 100, "sample 5.mp3"),
            (self.audio_file_101, 101, "sample 6.mp3"),
            (self.audio_file_103, 103, "sample 7.mp3"),
            (self.audio_file_105, 105, "sample 8.mp3"),
            (self.audio_file_107, 107, "sample 9.mp3"),
            (self.audio_file_108, 108, "sample 10.mp3")
        ]

        self.labels = {}
        self.error_labels = []
        self.currently_playing = None
        self.played_sounds = set()  # keep track of sounds that've been played

        # the frame for the awesomesauce image
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, padx=10, pady=10)

        # make the useless labels
        for audio_file, midi_note, display_name in self.audio_files:
            if os.path.isfile(audio_file):
                label_text = f"Sample loaded for MIDI Note {midi_note}"
                color = "black"
            else:
                label_text = f"Bruh, where is {display_name}?? WHERE IS ITT????!!!"
                color = "red"
                self.error_labels.append(midi_note)
            label = tk.Label(
                self.frame, 
                text=label_text, 
                fg=color,
                font=("Helvetica", 10)  # Adjust the font size here
            )
            label.pack(pady=10)
            self.labels[midi_note] = label

        # Reset button
        self.color_change_button = ctk.CTkButton(self.frame, text="Reset", command=self.change_label_colors)
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

        # load my awesome pic 
        self.image_path = os.path.join(os.path.dirname(__file__), "pic.png")
        self.load_and_display_image()

        # where midi??
        self.start_midi_listener()

    def change_label_colors(self):
        for midi_note in self.labels:
            if midi_note == 101:  # sample 6
                self.update_label_color(midi_note, "red")
            else:
                self.update_label_color(midi_note, "black")

    def stop_playback(self):
        pygame.mixer.music.stop()
        if self.currently_playing is not None:
            self.update_label_color(self.currently_playing, "orange")
        self.currently_playing = None

    def load_and_display_image(self):
        try:
            # load n' convert
            image = Image.open(self.image_path)
            photo = ImageTk.PhotoImage(image)
            # empty label lmao
            image_label = tk.Label(self.master, image=photo)
            image_label.image = photo  # reference
            image_label.pack(side=tk.RIGHT, padx=10, pady=10)
        except Exception as e:
            print(f"", file=sys.stderr)

    def play_audio_file(self, audio_file, midi_note):
        try:
            # halt!
            if self.currently_playing is not None:
                # If there's already a sound playing, set its label to orange
                self.update_label_color(self.currently_playing, "orange")
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            self.update_label_color(midi_note, "green")  # Highlight the currently playing label
            self.played_sounds.add(midi_note)
            self.currently_playing = midi_note
            self.master.after(100, self.check_music_playback)  # double check
        except pygame.error as e:
            print(f"Failed to play MP3 file {audio_file}: {e}", file=sys.stderr)

    def check_music_playback(self):
        if not pygame.mixer.music.get_busy():  # check for choo choo sounds playing
            if self.currently_playing is not None:
                self.update_label_color(self.currently_playing, "orange")  # PLEAAASSSEEE WORK CORRECTLYYYY
            self.currently_playing = None
        else:
            self.master.after(100, self.check_music_playback)  # KEEP checking
#da color function
    def update_label_color(self, midi_note, color):
        if midi_note in self.labels:
            self.labels[midi_note].config(fg=color)

    def start_midi_listener(self): #skill issue handling
        try:
            input_names = mido.get_input_names()
            if input_names:
                self.midi_input = mido.open_input(input_names[0])
                self.master.after(100, self.check_midi_input)
                print(f"GOOD JOB PARKER!! YOU REMEMBERED TO CONNECT THE KEYBOARD")
            else:
                print("You had ONE JOB: Plug the keyboard into the laptop!", file=sys.stderr)
                messagebox.showerror("womp womp", "You had ONE JOB: Plug the keyboard into the laptop!")
        except Exception as e:
            print(f"womp womp", file=sys.stderr)
            messagebox.showerror("MIDI Error", f"You had ONE JOB: Plug the keyboard into the laptop!")
                                   
    def check_midi_input(self):    #man, what is all this brainrot ah videos on my feed??
        if hasattr(self, 'midi_input'):
            try:
                for msg in self.midi_input.iter_pending():
                    if msg.type == 'note_on' and msg.velocity > 0:
                        for audio_file, midi_note, _ in self.audio_files:
                            if msg.note == midi_note:
                                self.play_audio_file(audio_file, midi_note)
                                break #in half lol
            except Exception as e: #need this oops
                print(f"bruh, something messed up... try again??", file=sys.stderr)
        self.master.after(90, self.check_midi_input)
#degrees haha get it, cuz its like... line 180, and i said degrees in a comment
if __name__ == "__main__":
    root = ctk.CTk()
    app = MidiPlayerApp(root)
    root.mainloop()
