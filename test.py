from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

output_file = 'encrypted.bin' # Output file
data = b'12345678901234561' # Must be a bytes object
key = b'1234567890123456' # The key you generated

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_CFB, iv = b'1234567890123456') # Create a AES cipher object with the key using the mode CBC
ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt

print(ciphered_data.decode("latin-1"))

