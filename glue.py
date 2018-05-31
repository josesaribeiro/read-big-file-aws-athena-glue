#
# The assumption is that you have already either manually (using Athena) or 
# automatically (using Glue crawler) to create a database and file object schema/table
#
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
# Specify source database/table
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "testdb", table_name = "holdings", transformation_ctx = "datasource0")
# Specify column mappings
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("objectid", "int", "objectid", "int"), ("periodid", "int", "periodid", "int"), ("securityid", "int", "securityid", "int"), ("holdingdate", "date", "holdingdate", "date"), ("flag", "byte", "flag", "byte"), ("sharesheld", "long", "sharesheld", "long"), ("optionsheld", "long", "optionsheld", "long"), ("percentportfolio", "double", "percentportfolio", "double"), ("percentoutstanding", "double", "percentoutstanding", "double"), ("shareschanged", "long", "shareschanged", "long"), ("percentshareschanged", "double", "percentshareschanged", "double"), ("ranksharesheld", "long", "ranksharesheld", "long"), ("ranksharesbought", "long", "ranksharesbought", "long"), ("ranksharessold", "long", "ranksharessold", "long")], transformation_ctx = "applymapping1")
# specify output target
# added the following to connection_options to get glue to partition on periodid 
# "partitionKeys": ["periodid"]
# Can also remove the "compression": "gzip" directive if you want plain text output
datasink2 = glueContext.write_dynamic_frame.from_options(frame = applymapping1, connection_type = "s3", connection_options = {"path": "s3://taupirho/iholding/logs",  "partitionKeys": ["periodid"], "compression": "gzip"}, format = "csv", transformation_ctx = "datasink2")
job.commit()
