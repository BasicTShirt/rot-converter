#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3.0.0b1
import unicodedata

try:
    from .frequencies import FREQUENCIES
except ImportError:
    from frequencies import FREQUENCIES

class ROTConvertor():
    def __init__(self):
        self.alphabets = {
            'en': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'es': 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜ',
            'de': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß',
            'fr': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÇÉÈÊËÎÏÔÙÛÜŸ',
            'it': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÌÒÙ',
            'pt': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÇÉÊÍÓÔÕÚÜ',
            'tr': 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ',
            'sv': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ',
            'no': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ',
            'fi': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ',
            'nl': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'da': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ',
            'ru': 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
            'bg': 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ',
            'sr': 'АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ',
            'mk': 'АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ',
            'be': 'АБВГДЕЁЖЗІЙКЛМНОПРСТУЎФХЦЧШЫЭЮЯ',
            'el': 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',
            'he': 'אבגדהוזחטיכלמנסעפצקרשת',
            'hy': 'ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՈՒՓՔՕՖ',
        }

        self.control_dict = {
            language: {symbol: index for index, symbol in enumerate(alphabet)}
            for language, alphabet in self.alphabets.items()
        }

        self.smart_mode_state = False
        self.frequencies = FREQUENCIES

    def custom_alphabet_handler(
            self,
            rot_language_or_custom_alphabet: str
    ) -> None:
        self.alphabet_state = (
            True if rot_language_or_custom_alphabet in self.alphabets
            else False
        )

        self.custom_control_dict = {
            symbol: index for index, symbol in enumerate(rot_language_or_custom_alphabet)
            if not self.alphabet_state
        }

        self.general_rot_alphabet = (
            self.alphabets[rot_language_or_custom_alphabet] if self.alphabet_state
            else rot_language_or_custom_alphabet
        )

    def _combine_error_handler(
            self,
            rot_string: str,
            rot_key: int | None,
            rot_language_or_custom_alphabet: str,
            mode: str,
    ) -> None:
        errors = []
        local_state_1 = True

        if (
                rot_string is None
                or rot_string == ""
        ):
            errors.append("ERROR! You did not enter a string")

        if (
                rot_language_or_custom_alphabet is None
                or rot_language_or_custom_alphabet == ""
        ):
            errors.append("ERROR! You did not enter a language or a custom alphabet")
            local_state_1 = False
        if (
                not isinstance(rot_language_or_custom_alphabet, str)
                and local_state_1
        ):
            errors.append("ERROR! Type of the language or the custom alphabet is not a string")

        if mode == "manual":
            if rot_key is None:
                errors.append("ERROR! You did not enter a key")
            else:
                if not isinstance(rot_key, int):
                    errors.append("ERROR! Type of the key is not a integer")

        if (
                self.smart_mode_state
                and rot_language_or_custom_alphabet not in self.alphabets
                and local_state_1
        ):
            errors.append("ERROR! Language for the smart mode is not support")


        if errors:
            raise ValueError("\n".join(errors))
        else:
            self.custom_alphabet_handler(rot_language_or_custom_alphabet)

    def universal_rot_handler(
            self,
            local_rot_string: str,
            local_rot_key: int,
            rot_language_or_custom_alphabet: str,
    ) -> str:
        local_rot_alphabet = self.general_rot_alphabet
        new_rot_string = ""

        for symbol in local_rot_string:
            if symbol.upper() in local_rot_alphabet:
                symbol_state = symbol.islower()

                index = (
                    self.control_dict[rot_language_or_custom_alphabet][symbol.upper()] if self.alphabet_state
                    else self.custom_control_dict[symbol.upper()]
                )

                alphabet_len = len(local_rot_alphabet)
                new_index = (index + local_rot_key) % alphabet_len

                new_rot_string += (
                    local_rot_alphabet[new_index].lower() if symbol_state
                    else local_rot_alphabet[new_index]
                )
            else:
                new_rot_string += symbol

        return new_rot_string

    def m_rot(
            self,
            rot_string: str,
            rot_key: int,
            rot_language_or_custom_alphabet: str,
    ) -> str:
        local_rot_string = unicodedata.normalize('NFC', str(rot_string))
        local_rot_key = rot_key

        self._combine_error_handler(
            rot_string,
            rot_key,
            rot_language_or_custom_alphabet,
            "manual",
        )

        new_mrot_string = self.universal_rot_handler(
            local_rot_string,
            local_rot_key,
            rot_language_or_custom_alphabet
        )

        return new_mrot_string

    def b_rot(
            self,
            rot_string: str,
            rot_language_or_custom_alphabet: str | None,
    ) -> dict[int, str]:
        local_rot_string = unicodedata.normalize('NFC', str(rot_string))

        if not self.smart_mode_state:
            self._combine_error_handler(
                rot_string,
                None,
                rot_language_or_custom_alphabet,
                "bruteforce",
            )

        new_brot_string = ""
        bruteforce_dict = {}
        bruteforce_counter = 0

        for bruteforce_key in range(len(self.general_rot_alphabet)):
            new_brot_string = self.universal_rot_handler(
                local_rot_string,
                bruteforce_key,
                rot_language_or_custom_alphabet
            )

            bruteforce_dict[bruteforce_counter] = new_brot_string
            bruteforce_counter += 1

        return bruteforce_dict

    def smart_rot(
            self,
            rot_string: str,
            rot_language_or_custom_alphabet: str,
    ) -> str:
        self.smart_mode_state = True
        self._combine_error_handler(
            rot_string,
            None,
            rot_language_or_custom_alphabet,
            None
        )

        rot_smart_dict = self.b_rot(rot_string, rot_language_or_custom_alphabet)

        guesses = []
        for key, string in rot_smart_dict.items():
            score = self._smart_mode_score(string, rot_language_or_custom_alphabet)
            guesses.append((key, string, score))

        self.smart_mode_state = False
        guesses.sort(key=lambda x: x[2], reverse=True)

        return guesses

    def _smart_mode_score(
            self,
            rot_string_score: str,
            rot_language_score: str
    ) -> float:
        score_alphabet = self.alphabets[rot_language_score]
        score_frequencies = self.frequencies[rot_language_score]

        score_counts = {char: 0 for char in score_alphabet}
        score_total = 0

        for symbol in rot_string_score:
            if symbol in score_counts:
                score_counts[symbol] += 1
                score_total += 1

        if score_total == 0:
            return 0.0

        dot_product = 0.0
        norm_text = 0.0
        norm_ref = 0.0

        for symbol in score_alphabet:
            text_freq = (score_counts[symbol] / score_total) * 100
            ref_freq = score_frequencies[symbol]

            dot_product += text_freq * ref_freq
            norm_text += text_freq ** 2
            norm_ref += ref_freq ** 2

        if norm_text == 0 or norm_ref == 0:
            return 0.0

        return dot_product / (norm_text ** 0.5 * norm_ref ** 0.5)

def m_rot(s, n, l):
    converter = ROTConvertor()
    return converter.m_rot(s, n, l)

def b_rot(s, l):
    converter = ROTConvertor()
    return converter.b_rot(s, l)

def smart_rot(s, l):
    converter = ROTConvertor()
    return converter.smart_rot(s, l)

if __name__ == '__main__':
	pass