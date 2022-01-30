#!/bin/bash
cd /usr/local/bili
python3  start.py >>/usr/local/bili/spider.log  2>&1 &
#等待执行完继续，否则找不到文件
wait


#结果拷贝到hdp01上的采集文件夹下
DATE=$(date +%Y%m%d)
#删除第一行，否则hdfs导出到mysql会出错
#sed -i '1d' /usr/local/bili/bilibili,找不到文件
awk 'NR>2{print line}{line=$0}' bilibili.csv  >> bilibili_tmp.csv



infile=bilibili_tmp.csv
outfile=bilibili_$DATE.csv

awk -F "," 'BEGIN{
        srand();
    }
    {
        value=int(rand()*34);       
        print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11"\t"$12"\t"$13"\t"$14"\t"$15
    }' $infile > $outfile

wait


scp bilibili_$DATE.csv  hdp02:/opt/app/collect-app/logs/data
scp bilibili_$DATE.csv  hdp03:/opt/app/collect-app/logs/data
wait
rm -rf *.csv


