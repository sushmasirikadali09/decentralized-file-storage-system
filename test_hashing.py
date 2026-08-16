from hashing import calculate_file_hash

test_file = "hash_test.txt"

with open(test_file, "w") as file:
    file.write("This is a test file for SHA-256 hashing.")

file_hash = calculate_file_hash(test_file)

print("SHA-256 Hash:")
print(file_hash)

if len(file_hash) == 64:
    print("🎉 Hashing test PASSED!")
else:
    print("❌ Hashing test FAILED!")