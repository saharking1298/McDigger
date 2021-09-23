# For Licensing, see LICENSE

from pynput import keyboard
import _thread as t
import pyautogui
import time
import json

# Tool slots
# Pickaxe: slot 1
# Axe: Slot 2
# Shovel: slot 3

save_file = "McDiggerData.json"
default_colors = {
    "dirt": (156, 100, 70),
    "wood": (218, 170, 116),
    "stone": (131, 131, 131)
}  #
material_slots = {
    0: "Same Block",
    1: "Stone",
    2: "Wood",
    3: "Dirt"
}
# Minecraft cursor coordinates on maximized windowed mode
pixels = (950, 540)


def get_slot(dirt, wood, stone):
    if dirt:
        return 1
    if stone:
        return 2
    if wood:
        return 3
    return 0


def setup_colors():
    try:
        colors = json.load(open(save_file, "r"))
        return colors
    except FileNotFoundError:
        json.dump(default_colors, open(save_file, "w"), indent=2)
        return default_colors


class McDigger:
    def __init__(self):
        self.activated = False
        self.listener = keyboard.Listener(on_release=self.on_key_release)
        self.material_colors = setup_colors()

    def start(self):
        print("Press f10 to start or stop digging")
        print("f7 -> dirt")
        print("f8 -> wood")
        print("f9 -> stone")
        self.listener.start()
        self.listener.join()

    def on_key_release(self, key):
        if str(key) == "Key.f10":
            self.activated = not self.activated
            if self.activated:
                t.start_new_thread(self.dig, ())
        elif str(key) == "Key.f7":
            color = pyautogui.pixel(*pixels)
            self.material_colors["dirt"] = color
            print("Dirt is now:", color)
            self.update_save()
        elif str(key) == "Key.f8":
            color = pyautogui.pixel(*pixels)
            self.material_colors["wood"] = color
            print("Wood is now:", color)
            self.update_save()
        elif str(key) == "Key.f9":
            color = pyautogui.pixel(*pixels)
            self.material_colors["stone"] = color
            print("Stone is now:", color)
            self.update_save()

    def update_save(self):
        json.dump(self.material_colors, open(save_file, "w"))

    def dig(self):
        print("Start Digging!")
        last = 0
        pyautogui.mouseDown()
        while self.activated:
            time.sleep(0.2)
            dirt = pyautogui.pixelMatchesColor(*pixels, self.material_colors["dirt"], tolerance=20)
            wood = pyautogui.pixelMatchesColor(*pixels, self.material_colors["wood"], tolerance=20)
            stone = pyautogui.pixelMatchesColor(*pixels, self.material_colors["stone"], tolerance=20)
            slot = get_slot(dirt, wood, stone)
            if slot != last:
                pyautogui.press(str(slot))
                last = slot
                print(material_slots[slot], "detected!")
        pyautogui.mouseUp()
        print("Stopped digging!")


digger = McDigger()
digger.start()
