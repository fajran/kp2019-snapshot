#!/bin/bash

B=$(cd $(dirname $0); pwd)
cd $B

set -x

curl https://kawal-c1.appspot.com/api/c/0 > 0.json

cat 0.json | jq '.children[][0]' > 0_children_ids.txt

cat 0_children_ids.txt | while read cid
do
  curl https://kawal-c1.appspot.com/api/c/$cid > $cid.json
done

git add "*.json" "*.txt"
git commit -m "$(date -R)"
git push origin master

