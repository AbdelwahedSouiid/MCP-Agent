# Dockerfile optimisé - SOLUTION FINALE
FROM python:3.12-slim

WORKDIR /app

# Installer uv (plus rapide que pip)
RUN pip install uv

# Copier SEULEMENT pyproject.toml d'abord (pour cache optimal)
COPY pyproject.toml ./

# Installer les dépendances avec cache
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Copier le reste du code APRÈS l'installation des dépendances
COPY . .

# Configurer l'environnement
ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/.venv"

EXPOSE 8089

CMD ["uv","run","python", "-m", "app"]