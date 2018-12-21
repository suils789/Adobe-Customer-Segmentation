
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import PCA
from pyspark.ml.clustering import BisectingKMeans
from pyspark.mllib.linalg.distributed import RowMatrix
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.util import MLUtils
from pyspark.ml.linalg import DenseVector
from pyspark.sql.functions import col
from pyspark.ml.linalg import VectorUDT
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

# load data
spark = SparkSession.builder.master("local[*]").appName("Capstone").getOrCreate()
data = spark.read.csv('sampled.csv', header=True, inferSchema=True)


# create sparse matrix
cols = [x for x in data.columns if x != '_c0']
vecAssembler = VectorAssembler(inputCols = cols, outputCol='features')
sparse_matrix = vecAssembler.transform(data).select('_c0', 'features').withColumnRenamed('_c0', 'id')


# create PCA components
pca = PCA(k=50, inputCol='features', outputCol='pca_features')
pca_model = pca.fit(sparse_matrix)


# create RowMatrix to perform SVD
df = MLUtils.convertVectorColumnsFromML(sparse_matrix, 'features')
mat = RowMatrix(df.select('features').rdd.map(lambda line: line[0])) 
svd = mat.computeSVD(50, True)
# get SVD latent factors
svd_latent_vec = svd.U.rows.map(lambda x: (x,)).toDF().select(col('_1').alias('svd_latent_vector'))
as_ml = udf(lambda v: v.asML() if v is not None else None, VectorUDT())

# convert it back to pyspark.ml dense vectors
result = svd_latent_vec.withColumn('svd', as_ml('svd_latent_vector'))

# Run Kmeans on the original dataset
bkm = BisectingKMeans(k=5, seed=1)
kmeans = bkm.fit(sparse_matrix)
kmeans_label = kmeans.transform(sparse_matrix)

# Run Kmeans on PCA features
bkm2 = BisectingKMeans(k=5, featuresCol='pca_features', predictionCol='pca_prediction', seed=1)
kmeans2 = bkm2.fit(result)
pca_label = kmeans2.transform(result)

# Run Kmeans on SVD latent factors
bkm3 = BisectingKMeans(k=5, featuresCol='svd', predictionCol='svd_prediction')
kmeans3 = bkm3.fit(result.select('svd'))
svd_label = kmeans3.transform(result.select('svd'))


# Extract PCA Components
def get_pca_component(v, i):
  a = DenseVector(v)
  return float(a[i])

pca = udf(get_pca_component, FloatType())

pca_label = pca_label.withColumn('pca1', pca(col('pca_features'), 1)).withColumn('pca2', pca(col('pca_features'), 2)).select('pca1', 'pca2', 'pca_prediction')

