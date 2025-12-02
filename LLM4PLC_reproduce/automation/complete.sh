#!/bin/bash
# 从 generation 文件夹中的每个文件中随机截取一定比例的行，并将这些截取的内容保存到 completion 文件夹中的对应文件中
shopt -s globstar
f="./generation/*"

#echo $f

filearray=($f)

for FILE in ${filearray[@]}
do


  lnct=$(cat $FILE | wc -l)
  #echo "has $lnct lines"

  c=$(bc -l <<< "scale=4 ; ${RANDOM}/32767")
  z=$(bc -l <<< "scale=4 ; $lnct*$c")
  y=$(printf "%.0f" $z)

  echo "using $y/$lnct lines"
  
  nf=$(echo $FILE | sed 's/generation/completion/')

  echo "$FILE -> $nf"

  #out=$(head -n $y $FILE)

  #cat ./preamble_completion > $nf
  #echo "[CODE_START]" >> $nf
  head -n $y $FILE | sed -e "s/\r//g" > $nf
  #echo "[CODE_END]" >> $nf

  echo

done

