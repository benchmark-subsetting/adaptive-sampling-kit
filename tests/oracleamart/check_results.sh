#!/bin/sh

result=`wc -l output/requested0000*.data |tail -n1`
[ "$result" = "100 total" ]
