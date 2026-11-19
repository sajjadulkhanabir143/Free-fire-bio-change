# Free Fire Bio Changer (Termux CLI)

A lightweight Python command-line tool built for **Termux** to update your Free Fire profile bio directly via API using dynamic Protocol Buffers and AES-CBC encryption.

---

## Features

- **Dynamic Protobuf Encoding:** Serializes custom bio text (`field_8`) on the fly without external `.proto` schema files.
- **AES-128-CBC Encryption:** Automatically encrypts request payloads before transmission.
- **Interactive CLI:** Clean terminal interface with continuous bio updates in a single session.
- **Mobile Ready:** Optimized for Android Termux environments.

---

## Prerequisites

- Android device with **Termux** installed
- **Python 3** & **Git**
- A valid Free Fire **JWT Access Token**

---

## Termux Installation

Run the following commands step by step in Termux:

```bash
pkg update && pkg upgrade -y
pkg install python git clang -y
git clone [https://github.com/sajjadulkhanabir143/Free-fire-bio-change.git](https://github.com/sajjadulkhanabir143/Free-fire-bio-change.git)
cd Free-fire-bio-change
pip install -r requirements.txt
python bio_changer.py

