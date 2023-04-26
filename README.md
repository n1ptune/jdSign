The sign directory include all the code to generate a sign.

The emu directory include emulate code for some function.

1_5136b9e5ca2e2c9394c097d2bd2521d6.apk is the orign  apk

# How to use

```python
from jdSign import getSign

functionId = "switchQuery"
clientVersion = "11.8.3"
client = "android"
uuid = "uuid"
body = "aaaabbbb"
getSign(functionId, body, uuid, client, clientVersion)
```

