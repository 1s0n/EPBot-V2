import cProfile
import re
data = ""
with open("gui.py") as f:
    data = f.read()
cProfile.run(data)