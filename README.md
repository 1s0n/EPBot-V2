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

T̶O̶D̶O̶:̶ ̶I̶m̶p̶l̶e̶m̶e̶n̶t̶ ̶a̶n̶t̶i̶-̶t̶a̶m̶p̶e̶r̶i̶n̶g̶

T̶O̶D̶O̶:̶ ̶I̶m̶p̶l̶e̶m̶e̶n̶t̶ ̶a̶u̶t̶o̶-̶u̶p̶d̶a̶t̶e̶s̶:̶

TODO: Add server maintainence message
