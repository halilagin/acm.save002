this is a rest api call to predict newly arrived data.

run command below

```
wget localhost:8450/acm/ml/classification/lr
```

and see the message below.

+--------------+--------+------------------------------+-----+----------+
|      Descript|Category|                   probability|label|prediction|
+--------------+--------+------------------------------+-----+----------+
|WARRANT ARREST|WARRANTS|[0.07824634322136563,0.0991...|  7.0|       7.0|
+--------------+--------+------------------------------+-----+----------+


prediction values should be the same, as 7 here.
