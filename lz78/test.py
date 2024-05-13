import random
with open("testicular.txt", "w", encoding="utf-8") as w_file:
    lst = "qwertyuiop[]asdfghjkl;'zxcvbnm,./1234567890-="
    for _ in range(1000000):
        w_file.write(random.choice(lst))
