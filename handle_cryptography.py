key = b'0Gp7TQ61uNsYyD8hyYE6_6wsd-dwmDFmPVvJ86-uEh8=' 
encrypted_token = b'gAAAAABpkytWai0D2IkC9BlravjBoD4B0HkyYHJ70cISgAJnAISELwyxKAvl8l6G4kRcdSOykqA56L3VBPPcK7p_68IB0C3qKSQ0a31Y3MrzQxKzaXCUUdxM89-Ia5G-2dOegBkqvUK3gjsa6qB_Q9jGqr9GLBjPI3BgkhSigCfhans8CGY6wkM=' 
encrypted_guildid = b'gAAAAABpkytWYgmIr_uQexn9dd7iYupAi6ulcabggJig2kJ-dSPXsGR60RNOljf82hEE5inpQ5QWaN-2GagijgJD0Q1wAoljZjpgjZJG5khFm0fR4CSItVQ=' 
# made : 14/02/2026
# handles cryptography by providing releveant functions


from cryptography.fernet import Fernet

main_suite = Fernet(key)

def return_token() -> str: # Proof of concept of how a attacker might hide their token.

    # token_key = b'TOKENKEY'
    # suite = Fernet(token_key)
    # return suite.decrypt(encrypted_token).decode()
    # if you want more encrption.

    return main_suite.decrypt(encrypted_token).decode()

def return_guildid() -> int:

    return int(main_suite.decrypt(encrypted_guildid).decode())

def return_decrypted(encrypted_str) -> str: # Proof of concept of how a attacker might decrypt their token.
    """
    Takes bytes or str of encrypted text returns decrypted encoded version.
    """

    suite = Fernet(key)

    if type(encrypted_str) == str:
        return suite.decrypt(encrypted_str.encode()).decode()

    return suite.decrypt(encrypted_str).decode()

def return_encrypted(text) -> str: # Proof of concept of how a attacker might encode their token.
    """
    Takes a string type text and returns a byte type encoded string.
    """

    suite = Fernet(key)

    return str(suite.encrypt(text))
