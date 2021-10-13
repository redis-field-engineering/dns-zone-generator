# DNS Zone Generator

## Running

### Startup Docker Redis

```
docker run -p 6379:6379 redislabs/redismod:edge
```

### Setup python environment

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Startup Application

```
python3 app.py
```

### Connect using browser

https://localhost:8080

