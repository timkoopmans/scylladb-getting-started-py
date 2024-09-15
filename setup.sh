# increase the maximum number of asynchronous I/O requests
echo fs.aio-max-nr=1048576 | sudo tee /etc/sysctl.d/41-aio_max_nr.conf
sudo sysctl -p /etc/sysctl.d/41-aio_max_nr.conf

# create a new network
docker network create --driver bridge scylla

# start a ScyllaDB node
docker run -it --rm -d --name node1 \
  --network scylla \
  -p 9042:9042 \
  scylladb/scylla:6.1.1 \
  --smp 1 --memory 1G

# clone the repository
ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts
git clone https://github.com/timkoopmans/scylladb-getting-started-py.git

# install the requirements
cd scylladb-getting-started-py
pip install -r requirements.txt

# setup monitoring
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

# add more nodes
docker run -it --rm -d --name node2 \
  --network scylla \
  scylladb/scylla:6.1.1 \
  --smp 1 --memory 1G \
	--seeds="node1"

docker run -it --rm -d --name node3 \
  --network scylla \
  scylladb/scylla:6.1.1 \
  --smp 1 --memory 1G \
	--seeds="node1"