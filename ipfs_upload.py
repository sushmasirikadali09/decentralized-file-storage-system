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


def download_from_ipfs(cid, output_path):
    """
    Download a file from IPFS using its CID.
    """

    url = f"{IPFS_API}/cat"

    response = requests.post(
        url,
        params={"arg": cid}
    )

    response.raise_for_status()

    with open(output_path, "wb") as file:
        file.write(response.content)

    return output_path


if __name__ == "__main__":
    print("IPFS upload/download module is ready.")