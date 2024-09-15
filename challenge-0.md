# Welcome to ScyllaDB!

In this challenge, you will get familiar with ScyllaDB basic management commands and launch your first node.

Running our first node
===

Docker simplifies the deployment and management of ScyllaDB. By using Docker containers, you can easily create isolated ScyllaDB instances for development, testing, and production. Running ScyllaDB in Docker is the simplest way to experiment with ScyllaDB, and we highly recommend it.

In the command prompt of your scylladb [terminal](tab-0) copy and run the following command:

```run
docker run -it --rm -d --name node1 \
  --network scylla \
  -p 9042:9042 \
  scylladb/scylla:6.1.1 \
  --smp 1 --memory 1G
```

This will start a new container called "node1" in a detached mode, using the ScyllaDB image allowing it to run in the background.

## Viewing Node Logs
To view the running logs of your node, run the following command:

```run
docker logs -f node1
```

Node logs are useful for troubleshooting and support. Can you see any important messages in the log output?

## Node Status
Let's now run `nodetool status` on our `node1` container:

```run
docker exec node1 nodetool status
```

`nodetool status` is a great way to view your existing cluster topology. In other words, it allows you to check the status of every node that's part of a cluster. Some common statuses are:

- `UN` - Up and Normal - The node is operational and is able to gossip with its peers;
- `DN` - Down and Normal - The node is part of the cluster, but it is either down or unable to communicate with one of its peers (for example, a network partition);
- `UJ` - Up and Joining - The node is up and is currently joining the cluster (a bootstrap operation);
- `UL` - Up and Leaving - The node is up and is currently leaving the cluster (a decommission operation);
- `U?` - Up and Unknown - The node is up, but we aren't yet aware of its current state. It may be in a transitory state or connectivity can be flaky. Check its logs.

Other relevant details presented by `nodetool status` involve:

-  The `Datacenter` name: Defaults to `datacenter1`, and is a particularly important field specially for multi-region deployments
-  The `Address` column specifies the IP address of the node
-   The `Host ID` column has a UUID type and uniquely identifies the node in the cluster
-   The `Rack` column specifies which placement group this node is part of. In Cloud-based deployments, *rack* and *availability zone* are used interchangeable.

The `nodetool` command, of course, has plenty other variations other than simply listing your cluster status. Let's grab a shell within the `node1` container and experiment with a few more commands:

```run
docker exec -it node1 /bin/bash
```

From within the shell, the `help` command lists available subcommands to use along with `nodetool`:

```run
nodetool help
```

> [!NOTE]
> Feel free to experiment with some of these as you learn!
> You can always prepend the `help` option to learn more about a particular command.
> The [ScyllaDB documentation](https://enterprise.docs.scylladb.com/branch-2024.1/operating-scylla/nodetool.html) also provides a quick'n'easy reference of all available commands.

For example, if you'd like to retrieve only details of the current single node instead of the entire cluster, you can run `nodetool info`:

```run
nodetool info
```

Or, if you'd like to check whether the database is ready to serve application requests, you could run `nodetool statusbinary`:

```run
nodetool statusbinary
```

In the next challenge, you will get a basic application connected to your database.