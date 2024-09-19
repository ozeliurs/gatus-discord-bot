# Gatus Discord Bot

[![Quality Gate Status](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=alert_status&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)
[![Maintainability Rating](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=sqale_rating&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)
[![Reliability Rating](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=reliability_rating&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)
[![Security Rating](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=security_rating&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)

[![Coverage](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=coverage&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)
[![Technical Debt](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=sqale_index&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)
[![Lines of Code](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=ncloc&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)
[![Duplicated Lines (%)](https://sonarqube.devops-tools.apoorva64.com/api/project_badges/measure?project=Gatus-Discord-Bot&metric=duplicated_lines_density&token=sqb_a337794bbf49e6f4cf41ed9be7420fbbfd413162)](https://sonarqube.devops-tools.apoorva64.com/dashboard?id=Gatus-Discord-Bot)

This Docker image contains a Discord bot that integrates with Gatus for monitoring purposes.

## Running the Docker Image

To run this Docker image, follow these steps:

1. Pull the image from GitHub Container Registry:
   ```
   docker pull ghcr.io/ozeliurs/gatus-discord-bot:latest
   ```

2. Run the container with the required environment variables:
   ```
   docker run -d \
     -e GATUS_API_URL=<your_gatus_api_url> \
     -e DISCORD_BOT_TOKEN=<your_discord_bot_token> \
     ghcr.io/ozeliurs/gatus-discord-bot:latest
   ```

   Replace `<your_gatus_api_url>` with the URL of your Gatus API, and `<your_discord_bot_token>` with your Discord bot token.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GATUS_API_URL` | The URL of your Gatus API |
| `DISCORD_BOT_TOKEN` | Your Discord bot token |

## Notes

- Make sure you have Docker installed on your system.
- The bot will run continuously in the background. Use `docker logs` to view its output.
- To stop the bot, use `docker stop` with the container ID or name.

For more information on using this bot or contributing to the project, please refer to the full documentation or contact the repository maintainer.
