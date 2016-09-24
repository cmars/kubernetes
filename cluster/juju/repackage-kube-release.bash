#!/bin/bash

# This script packages a kubernetes release for the charms

SCRIPT_DIR=$PWD

if [ -z $1 ]; then
  echo "Provide a full path to the source tar file."
  read RELEASE_TAR
else
  RELEASE_TAR=$1
fi

TMP_DIR=/tmp/kubernetes_release
mkdir $TMP_DIR
SERVER_TAR=kubernetes/server/kubernetes-server-linux-amd64.tar.gz
tar -xvzf $RELEASE_TAR -C $TMP_DIR $SERVER_TAR

mkdir $TMP_DIR/server

tar -xvzf $TMP_DIR/kubernetes/server/kubernetes-server-linux-amd64.tar.gz -C $TMP_DIR/server

cd $TMP_DIR/server/kubernetes/server/bin
MASTER_BINS=(kube-apiserver kube-controller-manager kubectl kube-dns kube-scheduler)
tar -cvzf $SCRIPT_DIR/kubernetes-master.tar.gz ${MASTER_BINS[*]} 
WORKER_BINS=(kubectl kubelet kube-proxy)
tar -cvzf $SCRIPT_DIR/kubernetes-worker.tar.gz ${WORKER_BINS[*]}

cd $SCRIPT_DIR

rm -rf $TMP_DIR
