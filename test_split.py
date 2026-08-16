from split_file import split_file
import os

test_file = "split_test.txt"

# Create a test file larger than our normal small examples
with open(test_file, "w") as file:
    file.write("A" * 3000)

# Split the file into 1 KB chunks
chunks = split_file(test_file, chunk_size=1024)

print("Chunks created:")

for chunk in chunks:
    print(chunk)

print(f"Total chunks: {len(chunks)}")

# Verify chunks exist
if chunks and all(os.path.exists(chunk) for chunk in chunks):
    print("🎉 File splitting test PASSED!")
else:
    print("❌ File splitting test FAILED!")