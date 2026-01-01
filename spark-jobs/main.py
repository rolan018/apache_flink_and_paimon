from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("SimpleJob")
         .config("spark.jars", "/opt/bitnami/spark/jars/paimon-spark-3.5-1.3.1.jar")
         .config("spark.sql.extensions", "org.apache.paimon.spark.extensions.PaimonSparkSessionExtensions")
         .config("spark.sql.catalog.paimon", "org.apache.paimon.spark.SparkCatalog")
         .config("spark.sql.catalog.paimon.warehouse", "s3a://warehouse/paimon/")
         .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
         .config("spark.hadoop.fs.s3a.access.key", "admin")
         .config("spark.hadoop.fs.s3a.secret.key", "password")
         .config("spark.hadoop.fs.s3a.path.style.access", "true")
         .config("spark.hadoop.fs.s3a.connection.timeout", "200000")
         .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
         .getOrCreate())

# Установка уровня логирования
# sc = spark.sparkContext
# sc.setLogLevel("DEBUG")


# 1 Способ чтения
spark.sql("USE paimon.flink")
spark.sql("select * from user_log").show()

# 2 Способ чтения
location = "s3a://warehouse/paimon/flink.db/user_log"
spark.read.format("paimon").load(location).show()


spark.stop()
