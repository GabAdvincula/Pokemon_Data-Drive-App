import tkinter as tk
from tkinter import ttk
import pypokedex
import PIL.Image, PIL.ImageTk
import urllib3
from io import BytesIO

class PokedexApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokédex")
        self.master.geometry("700x600")
        self.master.configure(bg="#e6d6f4")
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Label(
            self.master,
            text="Pokédex",
            font=("Arial Rounded MT Bold", 44, "bold"),
            fg="#7a42f4",
            bg="#e6d6f4",
            pady=20
        )
        header.pack()

        # Input Frame
        input_frame = tk.Frame(self.master, bg="#e6d6f4")
        input_frame.pack(pady=10)
        tk.Label(
            input_frame,
            text="ID or Name:",
            font=("Arial", 20),
            bg="#e6d6f4"
        ).pack(side=tk.LEFT, padx=8)
        self.entry = ttk.Entry(input_frame, font=("Arial", 18), width=18)
        self.entry.pack(side=tk.LEFT, padx=8)
        self.entry.bind('<Return>', lambda e: self.load_pokemon())
        ttk.Button(input_frame, text="Load Pokémon", command=self.load_pokemon).pack(side=tk.LEFT, padx=8)

        # Image Card
        self.img_frame = tk.Frame(self.master, bg="white", bd=2, relief=tk.RIDGE)
        self.img_frame.pack(pady=15)
        self.pokemon_image = tk.Label(self.img_frame, bg="white")
        self.pokemon_image.pack(padx=14, pady=14)
        
        # Info
        self.pokemon_information = tk.Label(
            self.master,
            font=("Arial", 28, "bold"),
            bg="#e6d6f4",
            fg="#222"
        )
        self.pokemon_information.pack(pady=(10,0))
        self.pokemon_types = tk.Label(
            self.master,
            font=("Arial", 20),
            bg="#e6d6f4",
            fg="#222"
        )
        self.pokemon_types.pack()
        self.error_label = tk.Label(
            self.master,
            font=("Arial", 16),
            fg="red",
            bg="#e6d6f4"
        )
        self.error_label.pack(pady=10)

    def load_pokemon(self):
        name = self.entry.get().strip().lower()
        if not name:
            self.error_label.config(text="Please enter a Pokémon name or ID.")
            return
        
        # Fetch data
        try:
            pokemon = pypokedex.get(name=name)
            sprite_url = pokemon.sprites.front.get('default')
            if sprite_url:
                http = urllib3.PoolManager()
                response = http.request('GET', sprite_url)
                image = PIL.Image.open(BytesIO(response.data)).resize((250,250))
                img = PIL.ImageTk.PhotoImage(image)
                self.pokemon_image.config(image=img)
                self.pokemon_image.image = img
            else:
                self.pokemon_image.config(image='')
                self.pokemon_image.image = None
            self.pokemon_information.config(
                text=f"{pokemon.dex} - {pokemon.name.title()}"
            )
            self.pokemon_types.config(
                text="Type: " + " - ".join([t.capitalize() for t in pokemon.types])
            )
            self.error_label.config(text="")
        except Exception as e:
            self.error_label.config(text="Pokémon not found.")
            self.pokemon_information.config(text="")
            self.pokemon_types.config(text="")
            self.pokemon_image.config(image="")
            self.pokemon_image.image = None

if __name__ == "__main__":
    root = tk.Tk()
    app = PokedexApp(root)
    root.mainloop()