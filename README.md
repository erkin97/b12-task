# Flight Optimizer

Find the destination with the cheapest dollars-per-kilometer flight using
Kiwi.com's Tequila API.

- **CLI**: `./flight-optimizer --from <city> --to <city> [<city> ...]`
- **Web app**: a React frontend on top of a Django + django-ninja backend

## Run it

Pick one of three ways. All three start the backend on `:8000` and the
frontend on `:5173`. Open http://localhost:5173.

### A. Docker

Requires Docker with Compose.

```bash
docker compose up --build
```

### B. Make

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/), and Node.js 20+.

```bash
make setup       # one-time: venv, Python deps, npm install
make backend     # terminal 1
make frontend    # terminal 2
```

Other targets: `make test`, `make lint`, `make help`.

### C. Scripts directly

Same as Make, just calling the scripts:

```bash
./scripts/bootstrap.sh
./scripts/dev_backend.sh
./scripts/dev_frontend.sh
```

## CLI

After setup:

```bash
uv run ./flight-optimizer --from London --to Paris Berlin Rome
```

Output:

```
Rome
$0.04/km
```

## Tests

```bash
uv run pytest                    # 15 tests
cd web/frontend && npm test      # 1 test on the API client
```

No backend tests are written per the brief.

## API key

`KIWI_API_KEY` must be set to your Kiwi.com Tequila API key. Two ways:

Shell (current terminal only):

```bash
export KIWI_API_KEY=<your-key>
```

`.env` file:

```bash
cp .env.example .env
# edit .env and set KIWI_API_KEY
```

For the Make and script paths, either export the variable or `source .env`
once per terminal.

## Project layout

```
flight-optimizer            CLI entrypoint
flight_optimizer/           Python package, shared by CLI and backend
tests/                      pytest suite
scripts/                    bootstrap, dev_backend, dev_frontend, smoke_kiwi
web/backend/                Django + django-ninja, single endpoint
web/frontend/               React + Vite + TypeScript + Tailwind
docker-compose.yml          containers for backend and frontend
Makefile                    targets that wrap the scripts
```
