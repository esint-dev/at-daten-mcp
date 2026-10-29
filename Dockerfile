FROM python:3.12-slim
LABEL io.modelcontextprotocol.server.name="io.github.esint-dev/at-daten-mcp"
WORKDIR /app
COPY esint_at_daten ./esint_at_daten
ENTRYPOINT ["python","-m","esint_at_daten.server"]
