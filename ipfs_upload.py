import requests


IPFS_API = "http://127.0.0.1:5001/api/v0"


def upload_to_ipfs(file_path):
    """
    Upload a file to the local IPFS node
    and return its CID.
    """

    url = f"{IPFS_API}/add"

    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            files={"file": file}
        )

    response.raise_for_status()

    result = response.json()

    return result["Hash"]


if __name__ == "__main__":
    test_file = "ipfs_test.txt"

    with open(test_file, "w") as file:
        file.write("Hello from Decentralized File Storage!")

    cid = upload_to_ipfs(test_file)

    print("🎉 IPFS upload successful!")
    print("CID:", cid)