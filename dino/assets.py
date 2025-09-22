import os
import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

def load_image(name):
    path = os.path.join(ASSETS_DIR, name)
    if not os.path.exists(path):
        return None
    return pygame.image.load(path).convert_alpha()

def scale_image(img, target_h=None, target_w=None):
    if img is None:
        return None
    w, h = img.get_size()
    if target_h is None and target_w is None:
        return img
    if target_h is not None:
        scale = target_h / h
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
    else:
        scale = target_w / w
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
    return pygame.transform.smoothscale(img, (new_w, new_h))
