#!/bin/bash
#########################################################################
# File Name: install_lib.sh
# Author: meetbill
# mail: meetbill@163.com
# Created Time: 2017-10-21 00:18:40
#########################################################################
CUR_DIR=$(cd `dirname $0`; pwd)
cd ${CUR_DIR}
if [[ ! -e "/usr/lib64/libslang.so.2"  ]]
then
    echo "this system not have libslang.so.2 lib"
    cp -d ./w_lib64/libslang.so.2 /usr/lib64/
    cp ./w_lib64/libslang.so.2.2.1 /usr/lib64/
    chmod 777 /usr/lib64/libslang.so.2
fi

if [[ ! -e "/usr/lib64/libnewt.so.0.52" ]]
then
    echo "this system not have libnewt.so.0.52"
    cp -d ./w_lib64/libnewt.so.0.52 /usr/lib64/
    cp ./w_lib64/libnewt.so.0.52.11 /usr/lib64/
fi


