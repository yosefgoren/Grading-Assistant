import json

def main():
	try:
		with open("results.json", "r") as f:
			results = json.load(f)
			if(type(results) != dict):
				print("results.json is not a dictionary!")
				return
	except FileNotFoundError:
		print("results.json not found")
		return
	except json.decoder.JSONDecodeError:
		print("results.json is not valid json!")
		return
	for cls, cres in results.items():
		print(f"showing analysis for '{cls}':")
		grades_per_student = [sum([grade for name, grade in qgrades.items()]) for qgrades in cres]
		avg = sum(grades_per_student)/float(len(cres))
		m = min(grades_per_student)
		print(f"average grade: {avg}/24, min grade: {m}/24")

if __name__ == "__main__":
	main()