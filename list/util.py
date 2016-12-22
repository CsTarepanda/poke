#!/usr/bin/python3
#encoding: utf-8
import re

def make_function_hiragana():
    re_katakana = re.compile('[ァ-ヴ]')
    def hiragana(text):
        """ひらがな変換"""
        return re_katakana.sub(lambda x: chr(ord(x.group(0)) - 0x60), text)
    return hiragana
hiragana = make_function_hiragana()


def make_function_katakana():
    re_hiragana = re.compile('[ぁ-ゔ]')
    def katakana(text):
        """カタカナ変換"""
        return re_hiragana.sub(lambda x: chr(ord(x.group(0)) + 0x60), text)
    return katakana
katakana = make_function_katakana()
