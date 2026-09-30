# Testing suite

## Build

```sh
# docker compose -f docker-compose-testing.yml -f docker-compose-testing.override.yml build --no-cache
```

## Run

Copy `env_testing_example` to `.env_testing` and change variables for testing environment

```sh
# docker compose -f docker-compose-testing.yml -f docker-compose-testing.override.yml up --force-recreate --abort-on-container-exit && docker compose rm -f
```
