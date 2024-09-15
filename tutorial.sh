docker network create --driver bridge scylla

docker run -it --rm -d --name node1 \
  --network scylla \
  scylladb/scylla:6.1.1 \
  --smp 1 --memory 1G

cd scylla-monitoring

cat << EOF > prometheus/scylla.yml
- targets:
    - node1
  labels:
    cluster: cluster1
    dc: datacenter1
EOF

./start-all.sh -v 5.4 -s prometheus/scylla.yml \
  --no-loki --no-alertmanager --no-renderer \
  -D "--network scylla"