ARG SPARK_VERSION

FROM bitnamilegacy/spark:${SPARK_VERSION}.0

ARG PAIMON_VERSION
ARG SPARK_VERSION


USER root

RUN apt-get update \
    && apt-get install -y curl jq

USER 1001

# Download Paimon JARs
RUN set -eux; \
    curl -L -o /opt/bitnami/spark/jars/paimon-spark-${SPARK_VERSION}-${PAIMON_VERSION}.jar \
      https://repo1.maven.org/maven2/org/apache/paimon/paimon-spark-${SPARK_VERSION}/${PAIMON_VERSION}/paimon-spark-${SPARK_VERSION}-${PAIMON_VERSION}.jar; \
    curl -L -o /opt/bitnami/spark/jars/paimon-format-${PAIMON_VERSION}.jar \
      https://repo1.maven.org/maven2/org/apache/paimon/paimon-format/${PAIMON_VERSION}/paimon-format-${PAIMON_VERSION}.jar;
