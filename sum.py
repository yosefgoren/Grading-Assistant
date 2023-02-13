import json
from speech import *

SPEECH_MODE = False
VOICE_MODE = False

io = AudibleIO()

def out_msg(msg: str):
	"""Print a message and speak it"""
	print(msg)
	if SPEECH_MODE:
		io.Speak(msg)

def gen_interpret_txt_integer_range(start: int, end: int):
	"""returns a function that interprets a number like interpret_text_number but returns None if number out of range"""
	if start > end:
		raise ValueError("start must be less than end")
	if end > 10:
		raise ValueError("end more than 10 is not supported")
	def f(txt: str) -> int:
		res = interpret_text_number(txt)
		if res is not None and start <= res and res <= end:
			return res
		else:
			return None
	return f

def prompt_num(msg: str, out_of: int) -> int:
	"""Prompt the user for a number between 0 and out_of"""
	while True:
		try:
			print(f"{msg} (0-{out_of}): ")
			if SPEECH_MODE:
				io.Speak(msg)
			if VOICE_MODE:
				num = io.Listen(gen_interpret_txt_integer_range(0, out_of))
			else:
				num = int(input())
			if 0 <= num <= out_of:
				if SPEECH_MODE:
					io.Speak(str(num))
				return num
			out_msg("Number not in range")
		except ValueError:
			out_msg("Invalid number")

def prompt_binstring(msg: str, nbits: int) -> list:
	"""Prompt the user for a binary string of length nbits"""
	while True:
		binstring = input(f"{msg} ({nbits} bits): ")
		if len(binstring) != nbits:
			print("Incorrect length")
			continue
		try:
			for bit in binstring:
				if bit not in "01":
					raise ValueError
			return [int(bit) for bit in binstring]
		except ValueError:
			print("Invalid number")

def product(ls1: list, ls2: list) -> int:
	"""Return the product of two lists of numbers"""
	return sum([a * b for a, b in zip(ls1, ls2)])

def get_test_results() -> dict:
	results = {}
	results["b"] = product([1, 1, 2, 1], prompt_binstring("b", 4))
	results["a"] = prompt_num("part a", 4)
	results["c.1"] = prompt_num("part c.1", 3)
	results["c.2"] = prompt_num("part c.2", 3)
	results["d"] = prompt_num("part d", 3)
	results["e"] = prompt_num("part e", 3)
	results["f"] = prompt_num("part f", 3)

	summery = f"grade is {sum(results.values())}"
	print(summery)
	if SPEECH_MODE:
		io.Speak(summery)
	
	return results

def main():
	#load results.json file if already exists:
	try:
		with open("results.json", "r") as f:
			results = json.load(f)
			if(type(results) != dict):
				print("warning: results.json is not a dictionary!")
				results = dict()
	except FileNotFoundError:
		results = dict()
		pass
	except json.decoder.JSONDecodeError:
		print("warning: results.json is not valid json!")
		results = dict()
		pass

	#prompt for a new class untill quits:
	def get_new_testres_prompt(text: str):
		first_word = text.split(" ")[0]
		if first_word in {"finish", "f"}:
			return "f"
		elif first_word in {"new", "next", "n"}:
			return "n"
		elif first_word in {"delete", "del", "d"}:
			return "d"
		elif first_word in {"show", "s"}:
			return "s"
		return None
		
	while True:
		class_id = input("New class? (Class ID for yes, n for no): ")
		if class_id == "n":
			break
		if class_id in results.keys():
			print("Appending to existing class")
			class_res = results[class_id]
		else:
			print("Creating new class")
			class_res = []
		while True:
			if VOICE_MODE and SPEECH_MODE:
				print("next/finish/delete/show")
				ans = io.Listen(get_new_testres_prompt)
			else:
				ans = input("- 'Enter/n' for new entry\n- 'f' to finish\n- 'd' to delete last entry\n- 's' to show last entry\n\t")
			if ans == "f":
				break
			elif ans == "d":
				if(len(class_res) == 0):
					print("No entries to delete")
					continue
				class_res.pop()
				print("Last entry deleted")
			elif ans == "s":
				if(len(class_res) == 0):
					print("No entries to show")
					continue
				print(class_res[-1])
			elif ans == "" or ans == "n":
				class_res.append(get_test_results())
			else:
				print("Invalid input")
		results[class_id] = class_res
	
	#save results to results.json:
	with open("results.json", "w") as f:
		json.dump(results, f, indent=3)

if __name__ == "__main__":
	main()
	

