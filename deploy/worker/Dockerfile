FROM python:3.11.8-bullseye as prod

ENV SRC /app/src
ENV SPARK_VERSION 3.5.1
ENV SPARK_HOME /opt/spark

RUN mkdir -p $SPARK_HOME
RUN mkdir -p $SPARK_HOME/jars

RUN apt update && apt install -y \
  openjdk-11-jdk curl rsync procps \
  && rm -rf /var/lib/apt/lists/*

RUN curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}.tgz -o spark-${SPARK_VERSION}.tgz \
&& tar xvzf spark-${SPARK_VERSION}.tgz --directory ${SPARK_HOME} --strip-components 1 \
&& rm -rf spark-${SPARK_VERSION}.tgz


# RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.950/aws-java-sdk-bundle-1.11.950.jar -o $SPARK_HOME/jars/aws-java-sdk-bundle-1.11.950.jar
# RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar -o $SPARK_HOME/jars/hadoop-aws-3.3.1.jar
# RUN curl https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.5/postgresql-42.2.5.jar -o $SPARK_HOME/jars/postgresql-42.2.5.jar



# Setup Spark related environment variables


# RUN apt-get update && apt-get install -y \
#   gcc \
#   && rm -rf /var/lib/apt/lists/*


# RUN pip install poetry==1.4.2

# # Configuring poetry
# RUN poetry config virtualenvs.create false

# # Copying requirements of a project
# COPY pyproject.toml poetry.lock /app/src/
# WORKDIR /app/src

# # Installing requirements
# RUN poetry install --only main
# # Removing gcc
# RUN apt-get purge -y \
#   gcc \
#   && rm -rf /var/lib/apt/lists/*

# # Copying actuall application
# COPY . /app/src/
# RUN poetry install --only main

CMD ["tail", "-f", "/dev/null"]
