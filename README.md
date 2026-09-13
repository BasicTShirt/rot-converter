[![License](https://img.shields.io/badge/License-MIT%20OR%20GPL%20v3-green.svg)](#license)

# Last Big Update: 3.0.0

### - Added Smart ROT Mode

---

# ROT Converter

A library for the ROT cipher with multi-language support.

## Features

- Encryption and decryption with ROT for 20 languages.
- ROT bruteforce for all supported alphabets.
- CLI Mode.
- Custom Alphabets For The ROT.
- Error handling with clear messages.
- Smart ROT mode based on frequency analysis

## Installation

```bash
pip install rot-converter
```

---

## Usage

Import the functions:

```python
from rot_converter import m_rot, b_rot, smart_rot
```

### Manual ROT — `m_rot(string: str, key: int, language: str)`

Shifts each letter in the string by the given key within the specified alphabet.

```python
from rot_converter import m_rot

temp_str = "tqv_eqpxgtvgt"
new_str = m_rot(temp_str, -2, "en")

print(new_str)  # Output: rot_converter
```

### Bruteforce ROT — `b_rot(string: str, language: str)`

Returns a list of all possible ROT shifts for the given string.

```python
from rot_converter import b_rot

temp_str = "bcd"
results = b_rot(temp_str, "en")

print(results[24])  # Output: zab
print(results[25])  # Output: abc
```

### Custom Alphabet — `m_rot(string: str, key: int, custom_alphabet: str)`

Use your own alphabet for encryption/decryption.

```python
from rot_converter import m_rot

# Base-36 alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
result = m_rot("HELLO", 5, alphabet)
print(result)
```
### Smart ROT — `smart_rot(string: str, language: str)`

Automatically detects the most likely shift using frequency analysis. Returns a sorted list of tuples `(shift, decrypted_text, score)` in descending order of confidence score.

```python
from rot_converter import smart_rot

# Ciphertext: "Hello, world! How are things? I'm doing well too!" (Shift +6, language: "en")
ciphertext = "Byffi, qilfx! Biq uly nbcham? C'g xicha qyff nii!"
results = smart_rot(ciphertext, "en")

# The most probable match is the first element
best_shift, best_text, score = results[0]

print(f"Shift: {best_shift}")       # Output: Shift: 6
print(f"Decrypted: {best_text}")   # Output: Decrypted: Hello, world! How are things? I'm doing well too!
print(f"Confidence: {score:.3f}")  # Output: Confidence: 0.794
```

---
## CLI Usage

After installation, the `rot-converter` command is available in your terminal.

### Commands

| Command | Description                     |
|---------|---------------------------------|
| `encrypt` | Encrypt text with a given key   |
| `decrypt` | Decrypt text with a given key   |
| `brute`   | Bruteforce all possible shifts  |
| `smart`   | Auto-detect the correct shift using frequency analysiss  |

### Options

| Option | Description                                          |
|--------|------------------------------------------------------|
| `-l, --lang`    | Language code (default: en)                          |
| `-c, --custom`  | Custom alphabet string                               |
| `-k, --key`     | Shift key (integer, required for encrypt/decrypt)    |

### Examples

```bash
# Encrypt
rot-converter encrypt "hello" --key 3 --lang en
# Output: khoor

# Decrypt
rot-converter decrypt "khoor" --key 3 --lang en
# Output: hello

# Bruteforce
rot-converter brute "bcd" --lang en
# Output:
#  Shift | Text
# ----------------------------------------
#      0 | bcd
#      1 | cde
#     ...
#     25 | abc

# Smart auto-detection
rot-converter smart "Khoor, Zruog!" --lang en

# Output:
#  Rank |  Shift |   Score | Text
# ------------------------------------------------------------
#     1 |     20 |   0.625 | Ebiil, Tloia!
#     2 |     16 |   0.586 | Axeeh, Phkew!
#     3 |     23 |   0.539 | Hello, World!
```

---
## Supported Languages

| Code | Language   | Alphabet Length |
|------|------------|-----------------|
| en   | English    | 26              |
| es   | Spanish    | 27              |
| de   | German     | 29              |
| fr   | French     | 26              |
| it   | Italian    | 26              |
| pt   | Portuguese | 26              |
| tr   | Turkish    | 29              |
| sv   | Swedish    | 29              |
| no   | Norwegian  | 29              |
| fi   | Finnish    | 29              |
| nl   | Dutch      | 26              |
| da   | Danish     | 29              |
| ru   | Russian    | 33              |
| bg   | Bulgarian  | 30              |
| sr   | Serbian    | 30              |
| mk   | Macedonian | 31              |
| be   | Belarusian | 31              |
| el   | Greek      | 24              |
| he   | Hebrew     | 22              |
| hy   | Armenian   | 38              |

---

## Requirements

- Python 3.10 or higher.
- No external dependencies (uses only standard library).

---

## Error Handling

The library validates all inputs and raises `ValueError` with descriptive messages.

### Error Types

| Error                                                        | Description                                                        |
|--------------------------------------------------------------|--------------------------------------------------------------------|
| **You did not enter a string**                               | The `string` parameter is missing or empty.                        |
| **You did not enter a language or a custom alphabet**        | The `language` or `custom alphabet` parameter is missing or empty. |
| **Type of the language or custom alphabet is not a string**  | The `language` or `custom alphabet` parameter is not a `str`.      |
| **You did not enter a key**                                  | The `key` parameter is missing (`None`) in manual mode.            |
| **You entered an unsupported language for the smart mode**   | The `language` is unsupported                                      |
| **Type of the key is not a integer**                         | The `key` parameter is not an `int`.                               |

### Error Examples

```python
from rot_converter import m_rot, b_rot

# Missing string
m_rot("", 2, "en")
# ValueError: ERROR! You did not enter a string

# Missing language or custom alphabet
m_rot("abc", 2, "")
# ValueError: ERROR! You did not enter a language or a custom alphabet

# Missing key
m_rot("abc", None, "en")
# ValueError: ERROR! You did not enter a key

# Key is a float
m_rot("abc", 1.5, "en")
# ValueError: ERROR! Type of the key is not a integer

# Unsupported language for the smart mode
smart_rot("Hello", "xx")
# ValueError: ERROR! Language for the smart mode is not support

# Multiple errors
m_rot("", 2.5, "")
# ValueError: ERROR! You did not enter a string
# ERROR! You did not enter a language or a custom alphabet
# ERROR! Type of the key is not a integer
```
---
## Changelog

| Version     | Date       | Commit                                                                                                    |
|-------------|------------|-----------------------------------------------------------------------------------------------------------|
| **0.1.0**   | 07.08.2026 | Beta: First Beta Version On PyPI                                                                          |
| **1.0.0**   | 13.08.2026 | Release: Just A Release                                                                                   |
| **2.0.0**   | 15.08.2026 | Release: New Clean Code, Added Support for 20 Languages And New Error Handler                             |
| **2.0.1**   | 15.08.2026 | Release: Improved Efficiency, Minor Bugs Fixed And a New GitHub Repository                                |
| **2.0.2**   | 15.08.2026 | Release: Normalize Input Strings To NFC                                                                   |
| **2.1.0**   | 16.08.2026 | Release: Significant Efficiency Boost, Custom Alphabet Support Added And Added CLI Mode Support           |
| **3.0.0b1** | 16.08.2026 | Beta: Added Smart ROT Mode Based On Frequency Analysis                                                    |
| **3.0.0b2** | 17.08.2026 | Beta: Critical Import Bug Fixed And Frequency Analysis Accuracy Increased                                 |
| **3.0.0**   | 13.09.2026 | Release: Added Stable Smart ROT Mode Based On Frequency Analysis                                          |
| **3.0.1**   | 13.09.2026 | Release: In Version 3.0.0, The Project Switched To The Strict GPLv3 License. To Avoid Blocking The Converter's Use In Closed-Source Commercial Integrations And To Restore Freedoms, An MIT-licensed Alternative Was Added. And Updated Error Handler|

###### **Made by the Hi Team.**
