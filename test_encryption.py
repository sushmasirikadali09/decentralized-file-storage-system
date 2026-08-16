from encryption import encrypt_file, decrypt_file
import os

original_file = "test_original.txt"
encrypted_file = "test_encrypted.bin"
decrypted_file = "test_decrypted.txt"

# Create a test file
with open(original_file, "w") as file:
    file.write("This is a test file for our decentralized storage system.")

# Encrypt
encrypt_file(original_file, encrypted_file)
print("✅ File encrypted successfully!")

# Decrypt
decrypt_file(encrypted_file, decrypted_file)
print("✅ File decrypted successfully!")

# Check the decrypted content
with open(decrypted_file, "r") as file:
    content = file.read()

print("Decrypted content:")
print(content)

# Check whether original and decrypted content are identical
if content == "This is a test file for our decentralized storage system.":
    print("🎉 Encryption test PASSED!")
else:
    print("❌ Encryption test FAILED!")