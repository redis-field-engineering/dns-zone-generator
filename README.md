# DNS Zone Generator

Generate DNS settings for Redis Enterprise zone delegation and detail troublshooting steps


### Zone Generation

You can generate configurations for the following DNS servers/services with screenshots
- Bind
- Azure (graphical)
- Azure Terraform
- AWS Route53 Terraform
- AWS Route53 (graphical)
- Google Cloud CLI
- Google Cloud (graphical)
- Google Cloud Terraform

### Troubleshooting

Provides step-by-step troubleshooting of DNS Zone delegation to ensure ease of use.


## Running Locally

Use [docker compose](https://docs.docker.com/compose/install/)

```
docker-compose up
```

Use your browser to [connect](http://localhost:8080)

## Development

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

