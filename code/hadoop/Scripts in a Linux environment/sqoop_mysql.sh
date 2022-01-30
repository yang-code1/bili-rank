#!/bin/sh

sqoop export --connect 'jdbc:mysql://hdp03:3306/bili?useUnicode=true&characterEncoding=utf-8' --username root --password 123456 --table bili_data --driver com.mysql.jdbc.Driver --export-dir '/spooldir/files/*' -m 1 --input-fields-terminated-by '\t'
