# FastJWS

Using this module you can quickly and easily perform JWT authentication.
The main advantage is the use of the RSA-256 algorithm for signing tokens.
The library is also great for small microservices.

## Install
#### pip:

![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=pip+install+fastjws)
#### poetry:

![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=poetry+add+fastjws)

## Speed tests
|Action       |   Time   |
|:-----------:|:--------:|
| Create token| 0.11 sec |
| Verify      | 0.10 sec |

## Examples of using

```python
from fastapi import FastAPI, Depends
from fastjws import SingJWT, AuthJWT
from pydantic import BaseModel
import datetime

# Open keys !!!not necessarily like here)
private_key = open('rs256.rsa', "r").read()
public_key = open('rs256.rsa.pub', "r").read()

# Creating an instance of a class.
jwt_sing = SingJWT(private_key)
jwt_auth = AuthJWT(public_key)

# Pydantic model for example, this is optional)
class AuthScheme(BaseModel):
    fake_login: str
    fake_password: str

app = FastAPI()

@app.post("/token")
def token(fake_data: AuthScheme):
    # Retrieving data from a database.
    fake_user: dict = fake_database
    # Selecting the token lifetime.
    expire = datetime.timedelta(minutes=15)
    # Receiving a token!)
    token: str = jwt_sing(fake_user, expire)

@app.get("/data")
async def get_data(token_data = Depends(jwt_auth)):
    return token_data
```
