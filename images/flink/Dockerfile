ARG FLINK_VERSION

FROM flink:${FLINK_VERSION}-java17

ARG PAIMON_VERSION
ARG FLINK_VERSION
ARG FLINK_STREAMING
ARG FLINK_POSTGRES_CDC
ARG FLINK_CORE
ARG FLINK_TABLE_BRIDGE
ARG KAFKA_CLIENTS

# Download Paimon JARs
RUN set -eux; \
    curl -L -o /opt/flink/lib/paimon-flink-${FLINK_VERSION}-${PAIMON_VERSION}.jar \
      https://repo1.maven.org/maven2/org/apache/paimon/paimon-flink-${FLINK_VERSION}/${PAIMON_VERSION}/paimon-flink-${FLINK_VERSION}-${PAIMON_VERSION}.jar; \
    curl -L -o /opt/flink/lib/paimon-s3-${PAIMON_VERSION}.jar \
      https://repo1.maven.org/maven2/org/apache/paimon/paimon-s3/${PAIMON_VERSION}/paimon-s3-${PAIMON_VERSION}.jar; \
    curl -L -o /opt/flink/lib/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar; \
    curl -L -o /opt/flink/lib/flink-sql-connector-postgres-cdc-${FLINK_POSTGRES_CDC}.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-postgres-cdc/${FLINK_POSTGRES_CDC}/flink-sql-connector-postgres-cdc-${FLINK_POSTGRES_CDC}.jar; \
    curl -L -o /opt/flink/lib/flink-streaming-java-${FLINK_STREAMING}.jar \
      https://repo1.maven.org/maven2/org/apache/flink/flink-streaming-java/${FLINK_STREAMING}/flink-streaming-java-${FLINK_STREAMING}.jar; \
    curl -L -o /opt/flink/lib/kafka-clients-${KAFKA_CLIENTS}.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_CLIENTS}/kafka-clients-${KAFKA_CLIENTS}.jar

# Set proper ownership
RUN chown flink:flink /opt/flink/lib/*

# Verify JARs were downloaded
RUN ls -la /opt/flink/lib/paimon-* /opt/flink/lib/flink-shaded-hadoop-*