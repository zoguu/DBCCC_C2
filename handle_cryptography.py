key = b'key' 
encrypted_token = b'token' 
encrypted_guildid = b'guildid' 
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
