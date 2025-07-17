"""
Stephen Smith
Class: CS 521 - Summer 2
Date: July 15, 2025
Homework Problem # 3_2
Description of Problem:
"""

def caesar_cipher(message: str, shift: int) -> str:
    encrypted = ""
    for char in message:
        if not char.isalpha():
            encrypted += char
        elif char.islower():
            encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif char.isupper():
            encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
    return encrypted
