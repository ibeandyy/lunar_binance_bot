# Current ruleset created on lines 11 and 28, key checker, score & check_digit_count
# Script checks the 4th value of the key (check_digit = key[3]) and must find ONLY three instances of that value
# AND the total key's ASCII value must be between 1700 and 1800. Can be expanded to create more difficult keys
# Will need threading applied if the script has to perform too many iterations to find a valid key due to difficulty.

import random


def license_check(key):
    # Create ASCII score variable + default value.
    global score
    score = 0
    # Our digit to check for - Each key's 4th value
    check_digit = key[3]
    # Digit occurrence tracker
    check_digit_count = 0
    # Split all 4-character strings into blobs split at the hyphen.
    blobs = key.split('-')

    # Iterate over all blobs created above, fail any value that isn't the proper length
    for blob in blobs:
        if len(blob) != 4:
            return False
        # Iterate over each character in the above blob checking for our pre-set # of digits to be satisfied
        for char in blob:
            if char == check_digit:
                check_digit_count += 1
            # Assign unicode value to each character to keep track of the "score"
            score += ord(char)
    # Create score constraint to limit randomly created ASCII keys that solely satisfy the check_digit_count
    if 1700 < score < 1800 and check_digit_count == 3:
        return True
    else:
        return False


# To run only when ran as the main script, LicenseMan shouldn't run otherwise, only LicenseCheck
if __name__ == '__main__':

    def license_manager():

        # Set defaults for License Key, amount of matching digits found, 4-letter "blobs",
        # and create character set for key generation.
        key = ''
        blob = ''
        alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"

        # Start creating a 25-character key
        while len(key) < 25:
            char = random.choice(alphabet)
            key += char
            blob += char
            # Add hyphens to key
            if len(blob) == 4:
                key += "-"
                blob = ''
        key = key[:-1]
        # Check if license generated is valid, if not generate another until it is.
        if license_check(key):
            print(f'Valid Key: {key}')
        else:
            license_manager()
    # Run function to obtain key, must be ran from LicenseManager.py as __main__.
    license_manager()






