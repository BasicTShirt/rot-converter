#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 0.0.2b1
import argparse
import sys
from rot_converter.converter import ROTConvertor

SUPPORTED_LANGS = (
    "en, es, de, fr, it, pt, tr, sv, no, fi, nl, da,"
    "ru, bg, sr, mk, be, el, he, hy"
)

EXAMPLES = """
EXAMPLES:
  rot-converter encrypt "hello" --key 3 --lang en
  rot-converter decrypt "khoor" --key 3 --lang en
  rot-converter brute "bcd" --lang en
  rot-converter smart "khoor" --lang en
  rot-converter encrypt "abc" --key 1 --custom "ABCDEF"
"""

class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            parts = []
            for name, parser in action.choices.items():
                parts.append(f"  {name:12s} {parser.description}")
            return "\n".join(parts) + "\n"
        return super()._format_action(action)

def _add_common_args(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--lang", default="en", help="Language code (default: en)")
    group.add_argument("-c", "--custom", help="Custom alphabet string")

def _get_alphabet_arg(args):
    if args.custom:
        return args.custom
    return args.lang

def main():
    parser = argparse.ArgumentParser(
        prog="rot-converter",
        description=(
            "ROT Converter — Multi-language Caesar cipher tool.\n"
            "Encrypt, decrypt, bruteforce or auto-detect ROT ciphers for 20+ languages.\n"
            "Supports custom alphabets."
        ),
        epilog=(
            "SUPPORTED LANGUAGES:\n  " + " ".join(SUPPORTED_LANGS) + "\n" + EXAMPLES
        ),
        formatter_class=CustomHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", title="COMMANDS", metavar="<command>")

    enc = subparsers.add_parser(
        "encrypt",
        description="Encrypt plaintext using ROT cipher.",
        help="Encrypt text with a given key",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example: rot-converter encrypt "hello" --key 3 --lang en',
    )
    enc.add_argument("text", help="Text to encrypt")
    enc.add_argument("-k", "--key", type=int, required=True, help="Shift key (integer)")
    _add_common_args(enc)

    dec = subparsers.add_parser(
        "decrypt",
        description="Decrypt ciphertext using ROT cipher.",
        help="Decrypt text with a given key",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example: rot-converter decrypt "khoor" --key 3 --lang en',
    )
    dec.add_argument("text", help="Text to decrypt")
    dec.add_argument("-k", "--key", type=int, required=True, help="Shift key (integer)")
    _add_common_args(dec)

    brute = subparsers.add_parser(
        "brute",
        description="Try all possible shifts and print results.",
        help="Bruteforce all ROT shifts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example: rot-converter brute "bcd" --lang en',
    )
    brute.add_argument("text", help="Text to bruteforce")
    _add_common_args(brute)

    smart = subparsers.add_parser(
        "smart",
        description="Auto-detect the correct shift using frequency analysis.",
        help="Auto-detect ROT shift via frequency analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example: rot-converter smart "khoor" --lang en --top 3',
    )
    smart.add_argument("text", help="Ciphertext to analyze")
    smart.add_argument(
        "-l", "--lang", required=True,
        help="Language code (frequency analysis only works for built-in languages)"
    )
    smart.add_argument(
        "-n", "--top", type=int, default=3, dest="top_n",
        help="Show top N best guesses (default: 3)"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    converter = ROTConvertor()

    try:
        if args.command == "encrypt":
            alphabet = _get_alphabet_arg(args)
            print(converter.m_rot(args.text, args.key, alphabet))

        elif args.command == "decrypt":
            alphabet = _get_alphabet_arg(args)
            print(converter.m_rot(args.text, -args.key, alphabet))

        elif args.command == "brute":
            alphabet = _get_alphabet_arg(args)
            print("  Shift | Text")
            print("-" * 40)
            for shift, text in converter.b_rot(args.text, alphabet).items():
                print(f"{shift:>6d} | {text}")

        elif args.command == "smart":
            guesses = converter.smart_rot(args.text, args.lang)
            top_n = min(args.top_n, len(guesses))
            print(" Rank |  Shift |   Score | Text")
            print("-" * 60)
            for rank, (shift, text, score) in enumerate(guesses[:top_n], start=1):
                print(f"{rank:>5d} | {shift:>6d} | {score:>7.3f} | {text}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()