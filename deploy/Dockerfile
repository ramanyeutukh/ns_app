FROM bitnami/spark:3.5.1 as prod

ENV POETRY_HOME=/opt/poetry
ENV POETRY_CONFIG_DIR="$POETRY_HOME/.config"
ENV POETRY_CACHE_DIR="$POETRY_HOME/.cache"
ENV PATH="$POETRY_HOME/bin:$PATH"

USER root
RUN apt-get update && apt-get install -y \
  gcc curl \
  && rm -rf /var/lib/apt/lists/*
USER 1001

RUN pip uninstall pyspark
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.950/aws-java-sdk-bundle-1.11.950.jar -o /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.11.950.jar
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar -o /opt/bitnami/spark/jars/hadoop-aws-3.3.1.jar
RUN curl https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.5/postgresql-42.2.5.jar -o /opt/bitnami/spark/jars/postgresql-42.2.5.jar

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
USER root
RUN poetry install --only main
# Removing packages
RUN apt-get purge -y \
  gcc curl \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main
