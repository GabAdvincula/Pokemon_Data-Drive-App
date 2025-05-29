import customtkinter as ctk
import pypokedex
import PIL.Image, PIL.ImageTk
import urllib3
from io import BytesIO
import random
import os

# my usual theme setup for the app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PokedexApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # window setup, title, size, and background color (I like it clean)
        self.title("Pokédex")
        self.geometry("460x590")
        self.configure(bg="#f8fbff")
        self.create_widgets()

    def create_widgets(self):
        # --- logo part (shows Pokémon logo at the top if the file exists) ---
        logo_path = "pokemon_logo.png"
        if os.path.exists(logo_path):
            # just resizing the logo to fit nicely
            logo_img = PIL.Image.open(logo_path).resize((240, 90))
            self.logo_photo = PIL.ImageTk.PhotoImage(logo_img)
            # bg_color is set to match the rectangle in the logo image
            logo = ctk.CTkLabel(self, image=self.logo_photo, text="", bg_color="#f3f4f6")
            logo.pack(pady=(16, 0))
        else:
            # backup, in case the logo image isn't there
            logo = ctk.CTkLabel(self, text="Pokémon", font=("Segoe UI", 32, "bold"), text_color="#2a75bb", bg_color="#e3f0fc")
            logo.pack(pady=(16, 0))

        # --- search bar and buttons section ---
        # I put everything in a frame for nicer grouping + round corners
        input_frame = ctk.CTkFrame(self, fg_color="#e3f0fc", corner_radius=25)
        input_frame.pack(pady=(12, 12), padx=10, fill="x")

        # this is where you type the Pokémon name or number
        self.entry = ctk.CTkEntry(input_frame, width=210, height=44, font=("Segoe UI", 14), corner_radius=22)
        self.entry.insert(0, "Search from 1 until 650 or by name")
        self.entry.bind("<FocusIn>", self.clear_placeholder) # placeholder disappears when you click
        self.entry.bind('<Return>', lambda e: self.load_pokemon()) # you can also press Enter to search
        self.entry.pack(side="left", padx=(8, 8), pady=8)

        # search button (does what it says)
        self.search_btn = ctk.CTkButton(
            input_frame,
            text="Search",
            command=self.load_pokemon,
            font=("Segoe UI", 14, "bold"),
            width=98,
            height=40,
            corner_radius=20,
            fg_color="#23408e",
            hover_color="#347fd6",
            text_color="white"
        )
        self.search_btn.pack(side="left", padx=(0,10))

        # lucky button because why not, it's fun
        self.lucky_btn = ctk.CTkButton(
            input_frame,
            text="Get Lucky!",
            command=self.get_lucky,
            font=("Segoe UI", 14, "bold"),
            width=120,
            height=40,
            corner_radius=20,
            fg_color="#347fd6",
            hover_color="#23408e",
            text_color="white"
        )
        self.lucky_btn.pack(side="left")

        # --- card section (shows the Pokémon info, kind of like a Pokédex entry) ---
        # outer frame for some border effect, just looks nicer
        border_frame = ctk.CTkFrame(self, width=368, height=288, corner_radius=38, fg_color="#C8D9F9")
        border_frame.pack(pady=(13, 0))
        border_frame.pack_propagate(False)

        # real card inside, this is where the info and pic go
        self.card_frame = ctk.CTkFrame(border_frame, width=350, height=270, corner_radius=35, fg_color="#f8fbff")
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.card_frame.pack_propagate(False)

        # Pokémon image (sprite) goes here
        self.pokemon_image_label = ctk.CTkLabel(self.card_frame, text="", bg_color="#ffffff")
        self.pokemon_image_label.pack(pady=(26, 0))

        # name of the Pokémon, big and blue
        self.name_label = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=("Segoe UI", 22, "bold"),
            text_color="#2a75bb",
            bg_color="#f8fbff"
        )
        self.name_label.pack(pady=(20, 4))

        # dex number, smaller and grey
        self.number_label = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=("Segoe UI", 14),
            text_color="#586579",
            bg_color="#f8fbff"
        )
        self.number_label.pack()

        # error messages show up here (like "Pokémon not found")
        self.error_label = ctk.CTkLabel(
            self,
            font=("Segoe UI", 13),
            text_color="#ff5c5c",
            bg_color="#e3f0fc",
            text=""
        )
        self.error_label.pack(pady=(16, 2))

    def clear_placeholder(self, event):
        # if the entry box has the default text, clear it when you click
        if self.entry.get() == "Search from 1 until 650 or by name":
            self.entry.delete(0, "end")

    def load_pokemon(self):
        # called when you search (by button or pressing Enter)
        name = self.entry.get().strip().lower()
        if not name or name == "search from 1 until 650 or by name":
            self.error_label.configure(text="Please enter a Pokémon name or ID.")
            return
        self._fetch_and_show(name)

    def get_lucky(self):
        # just picks a random Pokémon for fun
        lucky_num = random.randint(1, 650)
        self._fetch_and_show(str(lucky_num))

    def _fetch_and_show(self, name):
        # this is where the magic happens - gets data and updates the UI
        try:
            pokemon = pypokedex.get(name=name)
            sprite_url = pokemon.sprites.front.get('default')
            if sprite_url:
                # get the image from the web and show it
                http = urllib3.PoolManager()
                response = http.request('GET', sprite_url)
                image = PIL.Image.open(BytesIO(response.data)).resize((120,120))
                poke_img = PIL.ImageTk.PhotoImage(image)
                self.pokemon_image_label.configure(image=poke_img, text="")
                self.pokemon_image_label.image = poke_img # need to keep a reference!
            else:
                # sometimes there's no image available
                self.pokemon_image_label.configure(image="", text="")
                self.pokemon_image_label.image = None
            # update name and number
            self.name_label.configure(text=pokemon.name.title())
            self.number_label.configure(text=f"#{pokemon.dex}")
            self.error_label.configure(text="") # clear old errors
        except Exception:
            # if something goes wrong (typo or out of range), show error
            self.pokemon_image_label.configure(image="", text="")
            self.pokemon_image_label.image = None
            self.name_label.configure(text="")
            self.number_label.configure(text="")
            self.error_label.configure(text="Pokémon not found.")

if __name__ == "__main__":
    # so it actually runs!
    app = PokedexApp()
    app.mainloop()