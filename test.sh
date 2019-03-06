#!/bin/sh

for a in tests/*; do
   PYTHONPATH=. $a && continue
   echo $a
   break
done
