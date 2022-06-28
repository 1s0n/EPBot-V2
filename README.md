# EPBot-V2

Payload to make new account:
```Python
payload = {"email":"jason@gmail.com", "password": "p@ssword", "license": "ikAWYTeMN7KftBHEkdbNto8ykSCtXJnL"}
```

SQL Database query:
```sql
CREATE TABLE tokens (
ind INTEGER PRIMARY KEY,
data TEXT NOT NULL,
length INTEGER NOT NULL
);

CREATE TABLE users (
ind INTEGER PRIMARY KEY,
email TEXT NOT NULL,
password TEXT NOT NULL,
enckey TEXT NOT NULL,
enckey2 TEXT NOT NULL,
expirydate INTEGER NOT NULL,
token TEXT NOT NULL
);
```
