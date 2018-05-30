# read-big-file-aws-athena

Reading a big data file with Amazon Athena

The fifth part of a case study on how I got on reading a big file with C, Python, spark-python, AWS elastic map-reduce and 
this - AWS Athena

As a reminder, I'm trying to read the same big file (21 Gbytes) we read before with C, python, spark-python and aws elastic map reduce 
but this time using AWS Athena. Just thought it would be interesting to try it out to see how the timings would differ. Just to recap, the data file is about 21 Gigabtyes long and holds approximately 335 Million pipe separated records. The first 10 records are shown below:


```
18511|1|2587198|2004-03-31|0|100000|0|1.97|0.49988|100000||||
18511|2|2587198|2004-06-30|0|160000|0|3.2|0.79669|60000|60|||
18511|3|2587198|2004-09-30|0|160000|0|2.17|0.79279|0|0|||
18511|4|2587198|2004-09-30|0|160000|0|1.72|0.79118|0|0|||
18511|5|2587198|2005-03-31|0|0|0|0|0|-160000|-100|||19
18511|6|2587940|2004-03-31|0|240000|0|0.78|0.27327|240000||||
18511|7|2587940|2004-06-30|0|560000|0|1.59|0.63576|320000|133.33||24|
18511|8|2587940|2004-09-30|0|560000|0|1.13|0.50704|0|0|||
18511|9|2587940|2004-09-30|0|560000|0|0.96|0.50704|0|0|||
18511|10|2587940|2005-03-31|0|0|0|0|0|-560000|-100|||14

```

The second field in the above file can range between 1 and 56 and the goal was to split up the original 
file so that all the records with the same value for the second field would be grouped together in the same file. i.e we 
would end up with 56 separate files, period1.txt, period2.txt ... period56.txt each containing approximately 6 million records.

Just off the bat I will say this about AWS Athena - WOW!! it's blisteringly fast, read on to find out just how fast.

A little bit about Athena first. Athena is a relatively new service from AWS and is based on the Presto MPP SQL engine 
originally developed by Facebook. It is a serverless data processing tool that enables you to perform SQL queries on data files 
stored in AWS S3 buckets. It is fully managed and serverless which means it can scale automatically to handle HUGE data sets. 
It also means that you don't have to worry about infrastructure and can focus solely on creating SQL statements. To start using 
Athena you basically describe the location and format of the data file that you want to query. This involves creating an external 
schema/table in an Athena database that lets Athena know a) the bucket name where the data file(s) are stored, b) the format of 
the file e.g whether it's text, CSV, AVRO, Parquet etc ...  and c) the fields in the file including the field separator , field name 
and field type e.g Float, SmallInt, Date and so on. Note that you can either create this Athena table manually or by using an 
AWS Glue via a crawler. In either case once it's created sucessfully you can simply run queries against 
it as you would a regular database table. It's also possible to hook up Athena to ODBC and JDBC for programmatic control. So, here are 
my timimngs.

**NB Athena stores query outputs automatically into S3 either to a default or user-specified location**

As a reminder, here are the timings I got using the other methods in this case-study:-

```
C program on a openVMS Alpha server (Dual 1.33Ghz processors, 32 GB Ram) :- 54 minutes
Python 3.6 program on a Quad 3.4 GHz Intel Core i7-3770 windows 7 PC with 16GB RAM : 18 minutes
Spark-Python 3.5 program on a Quad 3.4 GHz Intel Core i7-3770 windows 7 PC with 16GB RAM : 36 minutes
Spark-Scala 2.1  program on a Quad 3.4 GHz Intel Core i7-3770 windows 7 PC with 16GB RAM : 48 minutes
Visual Studio C++ program on a Quad 3.4 GHz Intel Core i7-3770 windows 7 PC with 16GB RAM : 59 minutes
AWS elastic map-reduce: 1 hour
```

Here are my AWS Athena timings (remember this is querying a 21Gb, 335 million record data file):

select count(*), periodid from holdings group by periodid    : 15.83 seconds

select count(*) from holdings where periodid = 56      :   14.37 seconds to return 7,841,105 records

/* return the SUM of the numeric sixth field in my file */

select sum(sharesheld) from holdings    : 19.68 seconds to return the number 170,237,428,853,225,337

select * from holdings where periodid = 56      :  42 seconds

Note that the last query above produces an S3 file with the required data I was looking for. Obviously I would have to repeat 
this for all 56 periodid's to get the data for each periodid in a separate file but even so the total time taken would 
be well under 40 minutes. Must admit to being pretty impressed by Athena.




