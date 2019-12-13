runWitLog() {
	bin/spark-submit --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank.py ../sampleWork/sampleWebGraph_10_20_1.txt 10&
	bin/spark-submit --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank.py ../sampleWork/sampleWebGraph_10_20_1.txt 10&
	bin/spark-submit --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank.py ../sampleWork/sampleWebGraph_10_20_1.txt 10&
	bin/spark-submit --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank.py ../sampleWork/sampleWebGraph_10_20_1.txt 10

}

runWith10Threads() {
	bin/spark-submit --master local[10] --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank.py ../sampleWork/sampleWebGraph_10_20_1.txt 10&

}


run() {
  bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 --spark.eventLog.enabled=true 2> ../tmp1.log&
  bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 --spark.eventLog.enabled=true 2> ../tmp2.log&
  bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 --spark.eventLog.enabled=true 2> ../tmp3.log& 
  bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 --spark.eventLog.enabled=true 2> ../tmp4.log&

  #bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 2> ../tmp1.log&
  #bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 2> ../tmp2.log&
  #bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 2> ../tmp3.log& 
  #bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10 2> ../tmp4.log&
}

runPageRankV2() {
  bin/spark-submit --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank2.py 10&
#  bin/spark-submit --conf spark.scheduler.mode="FAIR" --conf spark.shuffle.service.enabled=true --conf spark.eventLog.dir=file:/tmp/spark-events --conf spark.eventLog.enabled=true  examples/src/main/python/pagerank.py /home/a239/chiaRock/sampleWork/sampleWebGraph_2000_1000000_1.txt 10&
}


show() {
  grep 'took ' ../tmp1.log
  grep 'took ' ../tmp2.log
  grep 'took ' ../tmp3.log
  grep 'took ' ../tmp4.log
}

# runWithLog

#show

#runWith10Threads

runPageRankV2

