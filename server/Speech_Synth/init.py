# python3 init.py 'es/en' 'name' '"Text"'
# example: python3 init.py es aud "Hola que tal"

from SpeechSynth import SpeechSynth
import sys
from pathlib import Path

Speech = SpeechSynth(sys.argv[1], sys.argv[2], sys.argv[3])

#devuelve el path para que pueda ser copiado a android o done sea y reproducirse
Path = Speech.Path() + "/" + sys.argv[2] + ".mp3"