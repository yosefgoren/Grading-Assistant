import speech_recognition as sr
import pyttsx3

class AudibleIO:
	def __init__(self):
		self.r = sr.Recognizer()
		self.engine = pyttsx3.init()

	def Speak(self, command):
		# Initialize the engine
		self.engine.say(command)
		self.engine.runAndWait()

	def Listen(self, process = lambda _: True) -> str:
		"""Retries to capture speech untill 'process' is not None"""
		while True:
			try:
				# use the microphone as source for input.
				with sr.Microphone() as source2:	
					# wait for a second to let the recognizer
					# adjust the energy threshold based on
					# the surrounding noise level
					self.r.adjust_for_ambient_noise(source2, duration=0.1)
					
					#listens for the user's input
					print("listenting ...")
					audio2 = self.r.listen(source2, phrase_time_limit=0.0, timeout=5.0)
					print("got audio...")
					# Using google to recognize audio
					result = self.r.recognize_google(audio2)
					if result == []:
						self.Speak("I didn't understand, try again.")
						continue
					txt = result.lower()
					print(f"recorded '{txt}'.")
					res = process(txt)
					print(f"processed to: '{res}'")
					if res is not None:
						return res
					else:
						self.Speak("Got an invalid response, try again.")
			except sr.RequestError as e:
				print("Could not request results; {0}".format(e))
			except sr.UnknownValueError:
				pass
				print("Timeout, trying again...")

def interpret_text_number(txt: str) -> int:
	"""Interpret a text number to an int, works from 0 to 10"""
	conversions = {
		"0": 0,
		"zero": 0,
		"1": 1,
		"one": 1, 
		"2": 2,
		"two": 2, 
		"3": 3,
		"three": 3,
		"4": 4,
		"four": 4,
		"5": 5,
		"five": 5,
		"6": 6,
		"six": 6,
		"7": 7,
		"seven": 7,
		"8": 8,
		"eight": 8,
		"9": 9,
		"nine": 9,
		"10": 10,
		"ten": 10,
	}
	if type(txt) == int:
		return txt
	elif type(txt) == str:
		word = txt.split(" ")[0]
		if word in conversions.keys():
			return conversions[word]
	print(f"could not interpret text number: '{txt}'")
	return None


if __name__ == "__main__":
	# a live test for the AudibleIO class
	io = AudibleIO()
	for word in [
		"zero",
		"one", 
		"two", 
		"three",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
		"ten"]:
		io.Speak(f"say '{word}'")
		res = io.Listen(interpret_text_number)
		print(res)
		io.Speak(f"you said '{res}'")