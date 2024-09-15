docker network create --driver bridge scylla

docker run -it --rm -d --name node1 \
  --network scylla \
  -p 9042:9042 \
  scylladb/scylla:6.1.1 \
  --smp 1 --memory 1G


ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts
git clone https://github.com/timkoopmans/scylladb-getting-started-py.git
cd scylladb-getting-started-py
pip install -r requirements.txt


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