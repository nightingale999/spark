#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx

Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10
"""
from __future__ import print_function

import re
import sys
from operator import add

from pyspark.sql import SparkSession

import asyncio


def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]

async def runPageRank(spark, filename):
    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    lines = spark.read.text(filename).rdd.map(lambda r: r[0])

    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[1])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    # Collects all URL ranks and dump them to console.
    for (link, rank) in ranks.collect():
        print("%s has rank: %s." % (link, rank))


def runPageRankInterleaved(spark, filenames):
    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    ranksArr = []
    for fil in filenames:
        lines = spark.read.text(fil).rdd.map(lambda r: r[0])
        # Loads all URLs from input file and initialize their neighbors.
        links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()
        # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
        ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))
        ranksArr.append(ranks)

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[1])):
        for ranks in ranksArr:
            # Calculates URL contributions to the rank of other URLs.
            contribs = links.join(ranks).flatMap(
                lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))
            # Re-calculates URL ranks based on neighbor contributions.
            ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    for ranks in ranksArr:
        # Collects all URL ranks and dump them to console.
        for (link, rank) in ranks.collect():
            print("%s has rank: %s." % (link, rank))



if __name__ == "__main__":
    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank--v2")\
        .getOrCreate()
    
    workDir = "/home/a239/chiaRock/sampleWork"

#    asyncio.run(runPageRank(spark, workDir + "/" + "sampleWebGraph_10_20_1.txt"))
#    asyncio.run(runPageRank(spark, workDir + "/" + "sampleWebGraph_100_1000_1.txt"))
#    asyncio.run(runPageRank(spark, workDir + "/" + "sampleWebGraph_1000_100000_1.txt"))
##    runPageRank(spark, workDir + "/" + "sampleWebGraph_100_1000_0.txt")
##    runPageRank(spark, workDir + "/" + "sampleWebGraph_10000_10000000_1.txt")
##    runPageRank(spark, workDir + "/" + "sampleWebGraph_2000_1000000_1.txt")
##    runPageRank(spark, workDir + "/" + "sampleWebGraph_3000_1000000_1.txt")
##    runPageRankInterleaved(spark, 
##        [workDir + "/" + "sampleWebGraph_10_20_1.txt", 
##         workDir + "/" + "sampleWebGraph_100_1000_1.txt",
##         workDir + "/" + "sampleWebGraph_1000_100000_1.txt",
##         workDir + "/" + "sampleWebGraph_3000_1000000_1.txt"])
    

    runPageRankInterleaved(spark, 
        [workDir + "/" + "sampleWebGraph_3000_1000000_1.txt"])
    

    spark.stop()
