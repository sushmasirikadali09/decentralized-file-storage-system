import os


def split_file(file_path, chunk_size=1024 * 1024):
    """
    Split a file into chunks.

    Default chunk size: 1 MB.
    """

    chunks = []

    with open(file_path, "rb") as file:
        chunk_number = 0

        while True:
            data = file.read(chunk_size)

            if not data:
                break

            chunk_filename = f"{file_path}.part{chunk_number}"

            with open(chunk_filename, "wb") as chunk_file:
                chunk_file.write(data)

            chunks.append(chunk_filename)
            chunk_number += 1

    return chunks