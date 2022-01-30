#!/bin/sh
# filename: start-flume-agent.sh
# desc: 启动采集数据的flume agent,agent名字a1
# date: 2020-04-28
FLUME_HOME=/usr/local/flume/

${FLUME_HOME}/bin/flume-ng agent -c ${FLUME_HOME}/conf -f ${FLUME_HOME}/conf/collect-app-agent.conf -n a1 -Dflume.root.logger=INFO,console -Dflume.monitoring.type=http -Dflume.monitoring.port=31001
