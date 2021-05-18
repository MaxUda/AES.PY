#import myeas

def main():
	while True:
		print("1 - ECB\n2 - CBC\n3 - CFB\n4 - OFB")
		com1 = int(input())
		if com1 == 1:
			print("Encrypt/Decrypt? e/d", end = ' ')
			com2 = input()
			if com2[0] == 'e':
				print("e")
			else:
				print("d")
		elif com1 == 2:
			print("Encrypt/Decrypt? e/d", end = ' ')
			com2 = input()
			if com2[0] == 'e':
				print("e")
			else:
				print("d")
		elif com1 == 3:
			print("Encrypt/Decrypt? e/d", end = ' ')
			com2 = input()
			if com2[0] == 'e':
				print("e")
			else:
				print("d")
		elif com1 == 4:
			print("Encrypt/Decrypt? e/d", end = ' ')
			com2 = input()
			if com2[0] == 'e':
				print("e")
			else:
				print("d")
		elif com1 == 5:
			return

main()