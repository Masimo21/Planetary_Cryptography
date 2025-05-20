
from skyfield.api import load
from hashlib import sha3_256
import numpy as np

def get_planetary_vector(timestamp=None):
    planets = load('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now() if timestamp is None else ts.utc(*timestamp)

    planet_names = ['mercury', 'venus', 'mars', 'jupiter barycenter', 'saturn barycenter', 'uranus barycenter', 'neptune barycenter']
    planet_vector = []

    for name in planet_names:
        try:
            pos = earth.observe(planets[name]).apparent().position.km  # x, y, z
            planet_vector.extend(pos)
        except KeyError:
            continue

    return np.array(planet_vector, dtype=np.float64)

def generate_crypto_key(user_secret=""):
    vec = get_planetary_vector()
    vec_bytes = vec.tobytes()
    combined = vec_bytes + user_secret.encode('utf-8')
    key = sha3_256(combined).digest()  # 256-bit key
    return key.hex()

key_no_secret = generate_crypto_key()
key_with_secret = generate_crypto_key("secret_key")

key_no_secret, key_with_secret
