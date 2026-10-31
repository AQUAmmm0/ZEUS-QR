# ZEUS QR

**AQUAmmm | ZEUS project**  
Local QR-code generator with a desktop GUI.

## Features

- Generate QR codes from URLs or plain text.
- Preview the QR code inside the application.
- Export PNG images in 256, 512, 768, or 1024 px.
- All QR generation happens locally on your computer.
- No account, hosting, or external API required.

## Requirements

- Python 3.10+
- pip

## Install on Kali Linux / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-tk

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

If your system blocks pip installation outside a virtual environment, keep using `.venv` as shown above.

## Project structure

```text
ZEUS-QR/
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Privacy

The application creates QR codes locally. The entered text or URL is not uploaded to a server by this application.

A QR code is static: its encoded destination cannot be changed after creation. Anyone who scans it can access the destination encoded in it, so check links before sharing.

## Project

Created as the first public utility of **AQUAmmm | ZEUS project**.
