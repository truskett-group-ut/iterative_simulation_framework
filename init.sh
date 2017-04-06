#!/bin/bash
#
# first check to find the last completed step
#
STEP_PRE=step_
i=999
j=999
OLD_DIR=$STEP_PRE$j
while [ ! -d $OLD_DIR ] && [ $i -gt 0 ]; do
    let i-=1
    printf -v j "%03g" $i
    OLD_DIR=$STEP_PRE$j
done
if [ $i -eq 0 ]; then
    if [ ! -d $OLD_DIR ]; then
        mkdir $OLD_DIR
    fi
    if [ -f params_val.json ]; then
        cp params_val.json $OLD_DIR/params_val_out.json
    elif [ -f $OLD_DIR/params_val.json ]; then
        cp $OLD_DIR/params_val.json $OLD_DIR/params_val_out.json
    fi    
fi
if [ ! -f $STEP_PRE"000"/done.txt ]; then
    touch $STEP_PRE"000"/done.txt
fi
while [ -z ${NEW_DIR+x} ]; do
    if [ -s $OLD_DIR/params_val_out.json ]; then
        let i+=1
        printf -v j "%03g" $i
        NEW_DIR=$STEP_PRE$j
    else
        if [ -f $OLD_DIR/done.txt ]; then
            NEW_DIR=$OLD_DIR
        else 
            d=$(date +%F-%T)
            mv $OLD_DIR $OLD_DIR-$d
            let i-=1
            printf -v j "%03g" $i
            OLD_DIR=$STEP_PRE$j
        fi
    fi
done
if [ ! -s $OLD_DIR/params_val.json ] && [ ! -s $OLD_DIR/params_val_out.json ]; then
    echo "need initial parameters in file" $OLD_DIR
    exit 1    
fi
echo $OLD_DIR
echo $NEW_DIR
