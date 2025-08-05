def str_all():
    # --- 1. String Creation ---
    s1 = "hello"
    s2 = 'world'
    s3 = """multi-line
    string"""
    s4 = str(1234)         # From int
    s5 = str(['a', 'b'])    # From list
    print(f"➕", s1, s2,s3,s4,s5, type(s5))

    # --- 2. Deletion (via reassignment) ---
    s_del = "temporary"
    del s_del  # Now s_del is gone

    # --- 3. Update (strings are immutable) ---
    s_orig = "python"
    s_updated = s_orig[:2] + "X" + s_orig[3:]
    print("Updated:", s_updated)  # → 'pyXhon'

    # --- 4. Manipulation ---
    msg = "  Hello World!  "
    print(msg.lower())             # '  hello world!  '
    print(msg.strip())             # 'Hello World!'
    print(msg.replace("World", "Python"))  # '  Hello Python!  '
    print(msg.startswith("  He"))  # True
    print(msg.endswith("!  "))     # True
    print(msg.split())             # ['Hello', 'World!']
    print("-".join(["2025", "06", "20"]))  # '2025-06-20'

    # --- 5. Format / f-strings ---
    name = "Lekhraj"
    score = 95.1234
    print(f"{name.upper()} scored {score:.2f}")  # 'LEKHRAJ scored 95.12'

    # --- 6. Escape sequences ---
    path = "C:\\Users\\lekhraj"
    quote = "He said, \"Python is fun!\""

    # --- 7. Raw strings ---
    regex = r"\d{3}-\d{2}-\d{4}"  # No escaping needed

    # --- 8. Slicing, indexing ---
    s = "abcdefgh"
    print(s[1:5])         # 'bcde'
    print(s[::-1])        # 'hgfedcba' reverse string

    # --- 9. Performance (avoid += in loop) ---
    import time
    words = ["one", "two", "three"]
    start = time.time()
    result = "".join(words)  # Faster than +=
    end = time.time()
    print("Join performance:", end - start)

    # --- 10. Tricky: reversing words in sentence ---
    sentence = "The quick brown fox"
    reversed_words = " ".join(sentence.split()[::-1])  # 'fox brown quick The'
    print("Reversed:", reversed_words)

    # --- 11. Advanced: string translation ---
    trans_table = str.maketrans("aeiou", "12345")
    print("hello world".translate(trans_table))  # h2ll4 w4rld

    # --- 12. Use case: extract domain from email ---
    email = "user@example.com"
    domain = email.split("@")[1]
    print("Domain:", domain)

    # --- 13. Use case: clean log line ---
    log = "[ERROR]   Disk full   "
    clean = log.strip(" []").lower() # space. [, ] -> strip these 3. default takes only  space
    print("Cleaned:", clean)  # error   disk full

    # --- 14. Use case: count word frequency ---
    from collections import Counter
    words = "one one two three two two".split()
    counts = Counter(words)
    print(counts)  # {'one': 2, 'two': 3, 'three': 1}

    # --- 15. Use case: detect palindrome ---
    s = "madam"
    print(f"{s} is palindrome? {s == s[::-1]}")

def str_all_2():
    print('='*10,"🔠 String Use Cases in Python\n" , '='*10)

    # ✅ Creation
    s1 = "Hello"
    s2 = str("World")
    s3 = """Multi
    Line
    String"""
    print(f"📌 Created Strings:\n{s1} | {s2} | {s3}\n")

    # ✅ Access & Slice
    print(f"🔍 Access: s1[0] = {s1[0]}, s1[-1] = {s1[-1]}")
    print(f"✂️ Slice: s2[1:4] = {s2[1:4]}\n")

    # ✅ Update (strings are immutable → use reassignment)
    s1 = s1.replace("H", "J")
    print(f"🔁 Replace H with J → {s1}")

    # ✅ Delete
    del s2  # deletes reference
    print("❌ Deleted s2 using `del s2`\n")

    # ✅ Common Manipulations
    s = " python  "
    print(f"🔧 Strip: '{s.strip()}'")
    print(f"🔠 Upper: {s.upper()}, Lower: {s.lower()}")
    print(f"🎯 Find 'th': {s.find('th')}, Replace 'py'->'my': {s.replace('py', 'my')}")
    print(f"🧩 Split: {s.split()}, Join: {'-'.join(['a','b','c'])}\n")

    # ✅ Formatting
    name = "Tim"
    age = 30
    print("🎨 Formatting:")
    print("Hello, {}. You are {}.".format(name, age))
    print(f"Hello, {name}. You are {age}.")  # f-string
    print("Pi is {:.2f}".format(3.14159))  # float formatting
    print()

    # ✅ Check Types
    print("🕵️ Checks:")
    print("123".isdigit(), "abc".isalpha(), "abc123".isalnum(), "  ".isspace())
    print("Title Case".istitle(), "lower".islower(), "UPPER".isupper())
    print()

    # ✅ Encoding & Decoding
    encoded = "hello".encode("utf-8")
    decoded = encoded.decode("utf-8")
    print(f"🔐 Encoded: {encoded}, Decoded: {decoded}\n")

    # ✅ Performance Tip (use join for concatenation in loops)
    print("🚀 Performance Tip:")
    words = ["Hello", "from", "Python"]
    print(" ".join(words))  # faster than += in loop
    print()

    # ✅ Tricky & Advanced
    print("🤯 Tricky:")
    print("a" * 5)             # Repeat
    print("abc" > "Abc")       # Lexical comparison
    print("😊".encode())       # Unicode
    print(f"Raw string: {r'C:\path\to\file'}")  # Raw string
    print()

    # ✅ f-string tricks
    pi = 3.14159
    print(f"🧪 f-string Pi (3 decimals): {pi:.3f}")
    print(f"🧾 Aligned: |{'left':<10}|{'right':>10}|{'center':^10}|")
