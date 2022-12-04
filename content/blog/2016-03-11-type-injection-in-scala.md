---
date: 2016-03-11
keywords: scala, type injection, injection, di, dependency injection, slick, database-agnostic, data-access
slug: type-injection-in-scala
template: post.html
title: Type Injection in Scala
---

I'm not sure if it's a good name but as we inject types into our classes, **type injection** seems a good name. I used this technic in my latest project to build a database-agnostic data-access layer on top of [Slick](http://slick.typesafe.com/) 3.

<!--more-->

In Slick 3 (the latest version at the moment) you have to be aware of the database engine you're connecting to. There is a specific API implementation for each database engine which should be imported in other to work with it.

For instance, the following code is needed to connect and work with Postgres:

```scala
// Use PostgresDriver to connect to a PostgreSQL database
import slick.driver.PostgresDriver.api._
```

On the other hand it's wise to use an in-memory DB for functional tests instead of Postgres. H2 is a perfect choice, but it's not fully compatible with Postgres and we were seeing serious issues in our tests when we just replaced the postgres connection with H2.

So, there are three options available:

1. Don't use non-h2-compatible APIs
2. Use Postgres; create a new Postgres DB before each test and drop afterward (we can use random db names to support parallel tests)
3. Make data-access layer database-agnostic and let Slick handle it

The first one feels like being in jail and the second one makes tests too slow but the third one is OK.

Slick is one of the most advanced libraries I've ever seen. It uses the most advanced features of Scala to be type-safe and strong yet simple to use.

We have to inject the slick driver API which, in fact, is a **trait** and subsequently a **type** containing various other types. For example `slick.driver.H2Driver.Table` is different than `slick.driver.PostgresDriver.Table`.

This is easily possible by injecting the `JdbcProfile` and import the driver specific types.

```scala
class PersonDAO(val profile: JdbcProfile) {
  import profile.api._
  //...
}
```

The profile can be set to Postgres for production:

```scala
class AppModule extends AbstractModule with ScalaModule {
  def configure() {
    bind[JdbcProfile].toInstance(PostgresDriver)
  }
}
```

And it can be set to H2 for tests:

```scala
  def application = {
    new GuiceApplicationBuilder()
      .overrides(bind[JdbcProfile].toInstance(H2Driver))
      .build
  }
```

Now data-access layer will switch to H2 when running tests. 

This is a sample of **type injection** in Scala.
