import pytest
from luckydev_hw_3_2 import caesar_cipher


@pytest.mark.parametrize("original, expected, shift", (
    ("Hello_World!", "Lipps_Asvph!", 4),
    ("By the pricking of my thumbs,\nSomething wicked this way comes.\nOpen, locks,\nWhoever knocks!", "By the pricking of my thumbs,\nSomething wicked this way comes.\nOpen, locks,\nWhoever knocks!", 0),
    ("middle-Outz", "okffng-Qwvb", 2),
    ("Ciphering.", "Ciphering.", 26),
    ("www.abc.xy", "fff.jkl.gh", 87),
    ("159357lcfd", "159357fwzx", 98),
    ("D3q4", "D3q4", 0),
    ("!m-rB`-oN!.W`cLAcVbN/CqSoolII!SImji.!w/`Xu`uZa1TWPRq`uRBtok`xPT`lL-zPTc.BSRIhu..-!.!tcl!-U", "!w-bL`-yX!.G`mVKmFlX/MaCyyvSS!CSwts.!g/`He`eJk1DGZBa`eBLdyu`hZD`vV-jZDm.LCBSre..-!.!dmv!-E", 62),
    ("Pz-/aI/J`EvfthGH", "Dn-/oW/X`SjthvUV", 66),
))
def test_caesar_cipher(original: str, expected: str, shift: str):
    assert caesar_cipher(original, shift) == expected


