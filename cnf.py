
import json
with open("config.ini") as file:
	for k, v in [i.split("=") for i in file.read().strip("\n").split("\n")]:
		print(k, v)
		globals()[k] = eval("lambda: " + v)()
		print(repr(globals()[k]))
