import random


def license_check(key):
    global score
    score = 0

    check_digit = key[3]
    check_digit_count = 0
    blobs = key.split('-')

    for blob in blobs:
        if len(blob) != 4:
            return False

        for char in blob:
            if char == check_digit:
                check_digit_count += 1
            score += ord(char)

    if 1700 < score < 1800 and check_digit_count == 3:
        return True
    else:
        return False


def license_manager():
    key = ''
    blob = ''
    check_digit_count = 0
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'

    while len(key) < 25:
        char = random.choice(alphabet)
        key += char
        blob += char

        if len(blob) == 4:
            key += "-"
            blob = ''
    key = key[:-1]

    #print(key)

    if license_check(key):
        print(f'Valid Key: {key}')
    else:

        license_manager()


new_key = license_manager()


