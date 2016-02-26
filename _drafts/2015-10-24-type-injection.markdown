---
layout: post
title:  "Type Injection"
date:   2015-10-24 17:12
---

It may sound crazy but I did **Type Injection** for my latest project to build a clean database-agnostic data-access layer on top of Slick 3.1.0.

<!--more-->

Our project is on top of Scala, Play and Slick. In Slick 3.0 (the latest one at the moment) you have to know which database you're going to connect to before importing the API.

For connecting to Postgres we had to use the following code:

{% highlight scala %}
// Use PostgresDriver to connect to a PostgreSQL database
import slick.driver.PostgresDriver.api._
{% endhighlight %}

But as H2 database is not fully compatible with Postgres we were seeing serious issues in our tests. We had three options:

1. Don't use non-h2-compatible APIs
1. Create a new Postgres DB before each test and drop afterward (we can use random db names to support parallel tests)
1. Make data-access layer database-agnostic

The first one feels like being in jail and the second one makes tests too slow but the third one seems wise!

Slick is one of the most advanced libraries I've ever seen. It uses the most advanced features of Scala to be type-safe and strong and yet simple to use.

Building a simple, abstract and database-agnostic CRUD trait on top of Slick is not easy. On the other hand we are not going to implement CRUD methods for each table by hand!

The problem is that we have to inject the slick driver API which, in fact, is a **trait** and subsequently a **type** containing various other types. For example `slick.driver.H2Driver.Table` is different than `slick.driver.PostgresDriver.Table`. 

So we have to inject a type into our classes.

...

