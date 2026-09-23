# 🔐 Decentralized File Storage System

A secure decentralized file storage system built using **Python, Flask, IPFS, SQLite, encryption, and SHA-256 hashing**.

The system allows users to upload files, encrypt them, generate a cryptographic hash, store the encrypted file on the IPFS network, and recover the original file through the web application.

---

## 📌 Project Overview

Traditional file storage systems usually depend on centralized servers.

This project demonstrates a decentralized approach where files are:

1. Uploaded through a Flask web application
2. Encrypted before storage
3. Verified using SHA-256 hashing
4. Uploaded to IPFS
5. Identified using an IPFS CID
6. The CID and file information are stored in SQLite
7. Files can later be recovered from IPFS
8. The recovered file is decrypted and hash-verified before download

---

## 🎯 Objectives

- Provide secure file storage
- Reduce dependency on centralized file storage
- Protect uploaded files using encryption
- Maintain file integrity using SHA-256
- Use IPFS for decentralized file storage
- Store IPFS CIDs in a database
- Allow users to recover files through a web interface

---

## 🏗️ System Architecture

```text
                USER
                  │
                  ▼
          Flask Web Application
                  │
                  ▼
            File Upload
                  │
          ┌───────┴────────┐
          ▼                ▼
      SHA-256          Encryption
       Hashing             🔐
          │                │
          └───────┬────────┘
                  ▼
             Encrypted File
                  │
                  ▼
                 IPFS
                  │
                  ▼
              IPFS CID
                  │
                  ▼
             SQLite DB
                  │
                  ▼
              Dashboard
                  │
                  ▼
          Download / Recover
                  │
                  ▼
           Download from IPFS
                  │
                  ▼
              Decryption
                  │
                  ▼
          SHA-256 Verification
                  │
                  ▼
           Original File