#!/bin/bash

release="$(curl -fsSL https://api.github.com/repos/sylabs/singularity/releases/latest | jq -r .tag_name)"
codename="$(lsb_release -cs)"
arch="$(dpkg --print-architecture)"
wget -O /tmp/singularity-ce.deb https://github.com/sylabs/singularity/releases/download/$release/singularity-ce_${release#v}-${codename}_$arch.deb
sudo dpkg -i /tmp/singularity-ce.deb
sudo apt-get install -f
