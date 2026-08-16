"""
ROT Converter - a library for the ROT cipher.

Main features:
- Encryption and decryption from ROT.
- ROT bruteforce.
- Error handling with clear messages.
"""

__version__ = "3.0.0b1"
__author__ = "BasicSweater"
__email__ = "basicsweater@petalmail.com"

from .converter import m_rot, b_rot

__all__ = ["m_rot", "b_rot"]