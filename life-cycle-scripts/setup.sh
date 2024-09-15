#!/bin/bash
echo fs.aio-max-nr=1048576 | sudo tee /etc/sysctl.d/41-aio_max_nr.conf
sudo sysctl -p /etc/sysctl.d/41-aio_max_nr.conf
