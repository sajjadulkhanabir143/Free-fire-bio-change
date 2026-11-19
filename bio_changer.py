import os
import sys
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf.descriptor_pb2 import DescriptorProto, FieldDescriptorProto
from google.protobuf.descriptor import MakeDescriptor
from google.protobuf.message_factory import GetMessageClass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = rf"""{CYAN}{BOLD}
====================================================
   ____    _       _   _   _    ____  _   _ _     
  / ___|  / \     | | | | / \  |  _ \| | | | |    
  \___ \ / _ \ _  | | | |/ _ \ | | | | | | | |    
   ___) / ___ \ |_| | |_| / ___ \| |_| | |_| | |___ 
  |____/_/   \_\___/ \___/_/   \_\____/ \___/|_____|
                                                    
             SAJJADUL KHAN ABIR - FF BIO TOOL       
===================================================={RESET}
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plain_text, AES.block_size)).hex()

def create_dynamic_protobuf():
    descriptor = DescriptorProto()
    descriptor.name = "DynamicMessage"
    
    field = descriptor.field.add()
    field.name = "field_8"
    field.number = 8
    field.label = FieldDescriptorProto.LABEL_OPTIONAL
    field.type = FieldDescriptorProto.TYPE_STRING
    
    message_descriptor = MakeDescriptor(descriptor)
    return GetMessageClass(message_descriptor)

def encode_protobuf(field_8_value):
    message_class = create_dynamic_protobuf()
    message = message_class()
    message.field_8 = field_8_value
    return message.SerializeToString().hex()

def update_bio(token, user_bio):
    if not token or not user_bio:
        return False, "Token এবং Bio দুটোই দিতে হবে।"

    encoded_bio = encode_protobuf(user_bio)
    encrypted_data = encrypt_api(f'1011{encoded_bio}5a006200')

    url = 'https://client.ind.freefiremobile.com/UpdateSocialBasicInfo'
    headers = {
        'Expect': '100-continue',
        'Authorization': f'Bearer {token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB48',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; Redmi Note 5 MIUI/V11.0.3.0.PEIMIXM)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    try:
        response = requests.post(
            url,
            data=bytes.fromhex(encrypted_data),
            headers=headers,
            verify=False,
            timeout=15
        )
        if response.status_code == 200:
            return True, "Bio সফলভাবে আপডেট হয়েছে!"
        return False, f"Request failed (HTTP {response.status_code}): {response.text}"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

def main():
    clear_screen()
    print(BANNER)

    try:
        token = input(f"{YELLOW}[+] Enter JWT Access Token: {RESET}").strip()
        if not token:
            print(f"{RED}[!] Token খালি রাখা যাবে না!{RESET}")
            sys.exit(1)

        while True:
            user_bio = input(f"\n{YELLOW}[+] Enter New Bio (বের হতে 'exit' লিখুন): {RESET}").strip()
            if user_bio.lower() == 'exit':
                print(f"{CYAN}[*] Exiting tool...{RESET}")
                break
            if not user_bio:
                print(f"{RED}[!] Bio টেক্সট দিন।{RESET}")
                continue

            print(f"{CYAN}[*] Updating bio...{RESET}")
            success, msg = update_bio(token, user_bio)
            if success:
                print(f"{GREEN}[✓] {msg}{RESET}")
            else:
                print(f"{RED}[✗] {msg}{RESET}")

    except KeyboardInterrupt:
        print(f"\n{CYAN}[*] Tool closed.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
