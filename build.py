import os
import subprocess

ui_folder = r'.\GUI\ui_forms'

pyui_folder = r'.\GUI\py_forms'

command_template = "pyuic6 -x {ui_file} -o {pyui_file}"

# Loop through each file in the folder
print('Creating pyuic6:')
for file in os.listdir(ui_folder):
    if file.endswith(".ui"):
        ui_file = os.path.join(ui_folder, file)
        filename = os.path.splitext(file)[0]
        pyui_file = os.path.join(pyui_folder, f"{filename}_ui.py")
        # Build the command and execute it
        cmd = command_template.format(ui_file = ui_file, pyui_file = pyui_file)
        subprocess.run(cmd, shell=True)
        print(f"{ui_file} -> {pyui_file}")
