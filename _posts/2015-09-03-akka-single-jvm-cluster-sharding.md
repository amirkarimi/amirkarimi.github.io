---
layout: post
title:  "Akka: Integration Tests for Single Node Cluster Sharding"
date:   2015-09-03 21:42
---

[Multi-JVM tests](https://github.com/typesafehub/activator-akka-cluster-sharding-scala/tree/master/src/multi-jvm/scala/sample/blog) are the default way of testing an Akka cluster sharding application. But sometimes you just need the sharding functionality where multi-JVM tests are just overkill. I didn't find any sample or guide describing the best practices for this situation.

<!--more-->

I just found out that it's not a bad idea to use Akka cluster sharding even if you don't need the real clustering features. But if you follow the default recommended way of integration tests you will ended up with the multi-jvm tests which are rather slow and complicated.

Another issue with the cluster sharding tests is the persistence. You have to use in-memory persistence plug-in or tests must not be run in parallel.

## Solution

I've build a simple test kit to be used as a Specs2 scope:

```scala
object ClusterTestKit {
  def storageLocations(system: ActorSystem) = List(
    "akka.persistence.journal.leveldb.dir",
    "akka.persistence.journal.leveldb-shared.store.dir",
    "akka.persistence.snapshot-store.local.dir").map(s => new File(system.settings.config.getString(s)))

  def deletePersistenceFiles(system: ActorSystem) = {
    storageLocations(system).foreach(dir => FileUtils.deleteDirectory(dir))
  }
}

abstract class IsolatedCluster(_system: ActorSystem)
  extends TestKit(_system) with DefaultTimeout
  with Around with ImplicitSender {

  import ClusterTestKit._

  def this() = this(TestActorSystemManager.getSystem(tempPersistence = true))

  override def around[T: AsResult](t: => T): Result = {
    try {
      AsResult.effectively(t)
    } finally {
      TestKit.shutdownActorSystem(system)
      deletePersistenceFiles(system)
    }
  }
}
```

`IsolatedCluster` class provides an isolated actor system cluster which makes tests easier. It also removes the persistence files.

As you can see `TestActorSystemManager` is the responsible for building the actor system and setting up cluster sharding with a single node:
```scala
object TestActorSystemManager {

  def getSystem(tempPersistence: Boolean) = {
    val system = getSystemWithoutSharding(tempPersistence)
    setupSharding(system)
    system
  }

  def getSystemWithoutSharding(tempPersistence: Boolean) = {
    val pathPrefix = "test" + (if (tempPersistence) Random.alphanumeric.take(5).mkString else "")

    val config = ConfigFactory.parseString(s"""
      akka {
        loglevel = "INFO"

        cluster.metrics.enabled=off
        actor.provider = "akka.cluster.ClusterActorRefProvider"

        persistence.journal.leveldb {
          native = off
          dir = "target/${pathPrefix}-journal"
        }

        remote {
          log-remote-lifecycle-events = off
          netty.tcp {
            hostname = "127.0.0.1"
            port = 0
          }
        }

        persistence.snapshot-store.plugin = "akka.persistence.snapshot-store.local"
        persistence.snapshot-store.local.dir = "target/${pathPrefix}-snapshots"
      }
    """)

    ActorSystem(ActorSystemManager.SystemName, config)
  }

  def setupSharding(system: ActorSystem) = {
    // Join cluster
    val cluster = Cluster(system)
    cluster.join(cluster.selfAddress)

    // Start sharding
    ActorSystemManager.startSharding(system)
  }
}
```

Note that I didn't use in-memory persistence plugin. Instead, the path of snapshots and journal stores are set randomly which allows tests to be run in parallel while I keep the production persistence plugin.

This made the tests over 400% faster.

And here is the integration test:

```scala
class SampleActorSpec extends Specification with Matchers {
  "Sample actor" >> {
    "send back info" >> new IsolatedCluster {
      val sampleRegion = ClusterSharding(system).shardRegion(SampleActor.shardName)
      sampleRegion ! GetInfo("actor1")
      expectMsg(SampleInfo("actor1", SampleActorState()))
    }
  }
}
```

Everything is like the default cluster sharding samples except that we have a single node. This way we can start simple and increase the node numbers and even scale-out the system, when necessary.