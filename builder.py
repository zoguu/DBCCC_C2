from cryptography.fernet import Fernet

token = input("Token : ")
guild_id = input("Guild ID : ")

key = Fernet.generate_key()
suite = Fernet(key)

encrypted_token = suite.encrypt(token.encode())
encrypted_guild_id = suite.encrypt(guild_id.encode())

file = "handle_cryptography.py"

with open(file,"r") as file:
    lines = file.readlines()

lines[0] = f"key = {key} \n"
lines[1] = f"encrypted_token = {encrypted_token} \n"
lines[2] = f"encrypted_guildid = {encrypted_guild_id} \n"

with open("handle_cryptography.py","w") as file:
    file.writelines(lines)

print(
f"""
Encrypted Token : {encrypted_token}
Encrypted Guild ID : {encrypted_guild_id}
Key : {key}
"""
)

input("Press any ENTER to exit.....")
