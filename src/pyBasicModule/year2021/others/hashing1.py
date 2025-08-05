import hashlib

# Exerceise : usecase of hash
p='password'
s = p.encode('utf8') ; print(s)
hash_original = hashlib.sha256(s) ; print(hash_original, hash_original.hexdigest())

p=p+'hacked'
hash = hashlib.sha256(p.encode('utf8')) ; print(hash, hash.hexdigest())

if hash == hash_original:
    print(" Password is OK")
else:
    print(" Password has been hacked")