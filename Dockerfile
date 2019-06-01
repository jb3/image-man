FROM nikaro/poetry

WORKDIR /bot

COPY poetry.lock /bot
COPY pyproject.toml /bot

RUN poetry install

COPY . /bot

CMD ["poetry", "run", "python", "bot.py"]
