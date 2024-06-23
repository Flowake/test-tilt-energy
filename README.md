# Test Tilt Energy

## Running

To run the frontend and backend, just run the following command:

```bash
docker compose up
```

The platform will be available at `http://localhost:3000`.

## Technologies

This project uses [SvelteKit](https://kit.svelte.dev/) for the frontend
and [FastAPI](https://fastapi.tiangolo.com/) for the backend,
as well as PostgreSQL as the database.

## Choices

It is wanted that users can choose the same appliance multiple times,
and this is accounted when computing the consumption per appliance.

The displayed consumption is for all the appliances of the same type combined.

As the results page can be used to display any previous simulation,
in real-world scenario there might be bad actors that could
scrap the results of other users. It would be possible to use very
long ids to prevent it.

The user email is not returned from any endpoints to prevent leaking
personal information.
