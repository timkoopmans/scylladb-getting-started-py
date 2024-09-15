In this challenge, you will add 2 more nodes to your cluster.

Adding more nodes
===

Now that you have a single node clustger running with your demonstration application writing to it, let's add more nodes to the cluster to increase the replication factor and overall availability of your data.

In the command prompt of your scylladb [terminal](tab-0) copy and run the following command:

```run
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
```

This will start new containers called "node2" and "node3" in a detached mode which will automatically join the cluster started by "node1".

## Node Status
As we did earlier, let's run `nodetool status` on our `node1` container:

```run
docker exec node1 nodetool status
```

You should see something that looks like this when the cluster is ready:

```
You should see something that looks like this:

```
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
-- Address    Load      Tokens Owns Host ID                              Rack
UN 172.21.0.2 187.05 KB 256    ?    857b7116-02c2-4982-b5fa-1a21ea774471 rack1
UN 172.21.0.3 388.73 KB 256    ?    a0d4957b-c099-4a2b-b1ce-4b69a6f3389c rack1
UN 172.21.0.4 382.35 KB 256    ?    33298ddc-21c6-4ddd-9b13-2068a10d0004 rack1
```

Updating replicaction factor
===


In the next challenge, we will setup ScyllaDB's monitoring stack to take a look at what's happening on the cluster.