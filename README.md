<<<<<<< Updated upstream
# ping-and-ring
Autonomous AI agent capable of both text chatting (ping) and real-time voice calling (ring).
=======
# ping-and-ring
Autonomous AI agent capable of both text chatting (ping) and real-time voice calling (ring).

## Development

Open the repository in VS Code with the Dev Containers extension and choose **Reopen in Container**. The container uses Python 3.13 and installs the locked project and development dependencies with `uv` when it is created.

Before running the agent, copy `.env.example` to `.env` and add your API keys. The `.env` file stays local and is not included in the container image or Git.

Run the sample graph from the integrated terminal:

```sh
uv run python -m ping_and_ring.agent.graph
```

Run checks with:

```sh
uv run ruff check .
uv run pytest
```
>>>>>>> Stashed changes
