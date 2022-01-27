import requests
import json
import time
import random
from PIL import Image
from io import BytesIO

PLANECHASE_REQUEST = "http://api.scryfall.com/sets/opca?as=grid&order=set"

PLANAR_DIE_OUTCOMES = ["", "chaos", "planeswalk"]
PLANAR_DIE_WEIGHTS = [4, 1, 1]
    
def get_pc_set():
    pc_set = requests.get(PLANECHASE_REQUEST)
    time.sleep(0.3)
    return pc_set.json()

def get_pc_cards():
    pc_set_json = get_pc_set()
    pc_cards = requests.get(pc_set_json['search_uri'])
    time.sleep(0.3)
    return pc_cards.json()

class Planechase(object):
    def __init__(self):
        self._name = "planechase"
        self._cards_json = get_pc_cards()
        self._planes = self._cards_json['data']
        self._num_cards = self._cards_json['total_cards']
        print("Loaded planechase cards!")
        self._current_plane = Plane()
        self.planeswalk()

    def roll_planar_die(self):
        choice = random.choices(PLANAR_DIE_OUTCOMES, PLANAR_DIE_WEIGHTS)[0]
        if (choice == "chaos"):
            self._chaos()
        elif (choice == "planeswalk"):
            self.planeswalk()
        return choice
    
    def planeswalk(self):
        plane_data = random.choice(self._planes)
        if (self._current_plane.get_name() == plane_data['name']) :
            self.planeswalk()
            return
        self._current_plane = Plane(plane_data['name'], plane_data['oracle_text'], plane_data['image_uris']['art_crop'])
    
    def _chaos(self):
        print(self._current_plane.get_chaos_ability())
     
    def get_current_plane_name(self):
        return self._current_plane.get_name()

    def get_current_plane_ability(self):
        return self._current_plane.get_ability()
    
    def get_current_plane_static_ability(self):
        return self._current_plane.get_static_ability()

    def get_current_plane_chaos_ability(self):
        return self._current_plane.get_chaos_ability()

    def get_current_plane_image(self):
        return self._current_plane.get_plane_image()


class Plane(object):
    def __init__(self, name="", ability="", image_uri=""):
        self._name = name
        self._ability = ability
        self._image_uri = image_uri
        self._static_ability = ""
        self._chaos_ability = ""
        self._parse_ability(self._ability)
        self._image = None

    def _parse_ability(self, ability):
        ability_split = ability.split('Whenever you roll {CHAOS}, ')
        self._static_ability = ability_split[0]
        if (len(ability_split) == 1):
            return
        else:
            self._chaos_ability = ability_split[1]
        self._chaos_ability = self._chaos_ability[0].upper() + self._chaos_ability[1:]

    def get_name(self):
        return self._name

    def get_ability(self):
        return self._ability

    def get_static_ability(self):
        return self._static_ability

    def get_chaos_ability(self):
        return self._chaos_ability

    def _load_plane_image(self):
        print("Loading image")
        image_response = requests.get(self._image_uri)
        plane_img = Image.open(BytesIO(image_response.content))
        self._image = BytesIO()
        plane_img.save(self._image, 'PNG')
        self._image.seek(0)
        time.sleep(0.3)

    def get_plane_image(self):
        if (not self._image):
            self._load_plane_image()
        self._image.seek(0)
        return self._image