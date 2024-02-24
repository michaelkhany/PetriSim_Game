# python toExe.py build
# C:/Python34/python toExe.py build

import cx_Freeze

executables = [cx_Freeze.Executable("petriSim_1.py")]

cx_Freeze.setup(
    name="Petri Simulator",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["PetriSimulatorGameDescription.txt"]}},
    executables = executables

    )   

# From there, you should get a build directory, within it will be an executable that will run your script.

# You can also do something like:

# python setup.py bdist_msi
# If you're on a mac, then you would do:

# python setup.py bdist_dmg
# That will generate a Windows installer.
