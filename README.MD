# FOR EDUCATIONAL AND PROOF OF CONCEPT PURPOSES ONLY.
# DBCCC C2
https://discord.gg/PTKNajTb9q
## Discord Based Command & Control Center Rat
**Warning** This project is for educational purposes only. It is not meant to harm, spread, exploit, control, attack or do any illegal activity.

** This project is presented as is. I am not liable for any damages. By using this you fully accept that you alone are responsible for the actions you do with this program / source code / application.**

## Installation

--- For testing Purpouses only---
Clone the project

```
git clone https://github.com/yourusername/project-name.git cd project-name
cd project-name
```
Install required dependencies
```
pip install -r requirements.txt
```
[Create and copy the token of an Discord Bot](#https://discord.com/developers/applications)

Create an discord server.

Enable developer mode on discord and right click your server, click COPY SERVER ID to get your Guild ID.

Use handle_cryptography.py to generate a Fernet key, encrypt your Token and Guild ID and put your token there.

Put the encrypted Guild ID in botmain file.

Run the script. Type 'help' or 'commands'.

## Study

From this study, we can learn about how the Remote Acces Tool's based off discord operate.
First they MUST contain the token, encrypted or take it from a online-source.
They must use XOR or other type's of encrpytion to protect said Token.
A combination of libraries like platform,os,shutil,fernet,requests is highly dangerous even without admin permissions.


