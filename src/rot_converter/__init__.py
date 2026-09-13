# SPDX-License-Identifier: MIT OR GPL-3.0-or-later
# Copyright (c) 2026 BasicSweater

"""
ROT Converter - a library for the ROT cipher.

Main features:
- Encryption and decryption from ROT.
- ROT bruteforce.
- Error handling with clear messages.
"""

__version__ = "3.0.1"
__author__ = "BasicSweater"
__email__ = "basicsweater@petalmail.com"

from .converter import b_rot, m_rot, smart_rot

__all__ = ["m_rot", "b_rot", "smart_rot"]
