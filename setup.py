import os
import platform

system = platform.system()
print("OS:", system)
path = os.path.abspath(".")

if system == "Windows":
    pyhome = path + "\\venv-windows\\ext"
    pyvenv = f"""home = {pyhome}
include-system-site-packages = false
version = 3.11.2"""

    with open(".\\venv-windows\\pyvenv.cfg", "w") as f:
        f.write(pyvenv)

    print("Setup complete!")
else:
    print("On Linux if you have Python installed it should run normally.")