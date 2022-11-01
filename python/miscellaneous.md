### Create virtualenv fast

Dependencies:
- python3.10-venv

```
python3 -m venv env
. ./env/bin/activate
```


### Get today's date as a string

```py
from datetime import datetime
datetime.today().strftime("%m-%d-%Y, %H:%M:%S")
```
