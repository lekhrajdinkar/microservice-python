# https://en.wikipedia.org/wiki/Caesar_cipher
"""
Original alphabet:      abcdefghijklmnopqrstuvwxyz
Alphabet rotated +3:    defghijklmnopqrstuvwxyzabc
Note: The cipher only encrypts letters; symbols, such as -, remain unencrypted.

caesarCipher has the following parameter(s):
    string s: cleartext
    int k: the alphabet rotation factor
     n, the length of the unencrypted string.
"""

# ❌
def caesarCipher_old(s, k):
    enc_s = ''
    for c in s:
        if c in "abcdefghijklmnopqrstuvwxyz":
            enc_s += str((int(c)+3))
        else:
            enc_s += c

# ✅
# work on interger = 1 to 26
# not on unicode
def caesarCipher(s, k):
    enc_s = ''
    for c in s:
        if c in "abcdefghijklmnopqrstuvwxyz":
            enc_s += chr((ord(c) - ord('a') + k) % 26 + ord('a'))
        elif c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            enc_s += chr((ord(c) - ord('A') + k) % 26 + ord('A'))
        else:
            enc_s += c  # Leave symbols unchanged

    print(s, k, enc_s, end="\n")
    return enc_s

if __name__ == '__main__':
    caesarCipher("middle-Outz", 2)