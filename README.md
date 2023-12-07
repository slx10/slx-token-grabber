# SLx Token grabber

## Introduction

This script is designed to locate and retrieve authentication tokens associated with various platforms, with a primary focus on Discord and web browsers. The recovered tokens can be used for further analysis and investigation.

## Prerequisites

Before running the script, ensure that the following Python libraries are installed:

```bash
pip install requests pypiwin32 pycryptodome
```

## Usage

1. Run the script using Python 3.
2. The script will search for authentication tokens in various locations on your system, including Discord and popular web browsers.
3. If tokens are found, they will be displayed in the console.

## Script Overview

- **validate_token(token):**
  - Validates a Discord token by making a request to the Discord API.

- **find_tokens_in_file(file_path, regexs):**
  - Searches for tokens in a given file using regular expressions.

- **decrypt_val(buff, master_key):**
  - Decrypts a password from a buffer using the provided master key.

- **find_discord(p):**
  - Searches for Discord tokens in the specified directory.

- **find_platform(p):**
  - Searches for tokens in the specified directory based on platform-specific patterns.

- **get_tokens():**
  - Retrieves tokens from various platforms, including Discord, Google Chrome, Opera, Brave, and Yandex.

## Platforms Supported

- Discord
- Discord Canary
- Discord PTB
- Discord Development
- Lightcord
- Google Chrome
- Opera
- Brave
- Yandex

## Updated Functionality

- The script now supports multiple user profiles in web browsers.
- For Chromium-based browsers (Google Chrome, Brave), the script looks for profiles within the specified user data directory.
- The script iterates through profiles, searching for tokens in each one.

## Note

This script is for educational and research purposes only. Unauthorized use of this script may violate the terms of service of the platforms it interacts with. Use it responsibly and only on systems you own or have explicit permission to analyze.

## Disclaimer

The authors of this script are not responsible for any misuse or damage caused by the script. Use it at your own risk.
