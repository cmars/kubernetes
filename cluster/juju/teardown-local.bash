#!/bin/bash -ex

for m in $(uvt-kvm list | grep ^kub); do
	uvt-kvm destroy ${m} || true
done

(juju controllers --format json | jq -r '.controllers|keys|.[]' | grep k8s) || exit 0

juju switch k8s
for m in $(juju models --format json | jq -r '.models|.[].name' | grep ^k8s); do
	juju destroy-model -y ${m} || true
done

