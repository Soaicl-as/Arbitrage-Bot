# Arbitrage Bot

A bot to detect and alert arbitrage betting opportunities across multiple platforms.

## Setup

1. Clone the repository.
2. Add your environment variables to `.env`.
3. Run `./build.sh` to set up the environment.
4. Run `./start.sh` to start the bot.

## Deployment on Render

1. Push the code to a Git repository.
2. Create a new **Worker** service on Render.
3. Connect your repository and configure the service using `render.yaml`.
4. Add environment variables in the Render dashboard.
5. Deploy the service.