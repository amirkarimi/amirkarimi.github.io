---
layout:   post
title:    "Don’t listen to them, learn Cats this way"
date:     2018-01-29
keywords: "functional programming, FP, cats, scalaz, scala, monad transformers"
---

![](https://cdn-images-1.medium.com/max/800/1*Tj-wz2CtiiX2RtQutVKLOA.png){: .center-image }

OK, you came to the conclusion that type-safety is good. It helps you get things
done in a safer manner, at least for whatever you’re working on at the moment.
So you started using types more than before to describe what a piece of code
does without the need to run. In another word, to bring forward unwanted errors.

<!--more-->

One of the first things you might have found quite handy when started using
Scala is `Option` type, after which it simply no longer makes sense to deal with
`null`s.

Have a look at this piece of code for instance:

```scala
def getUser(id: Int): Option[User] = ???

getUser(10) match {
    case None => println("User not found")
    case Some(user) => println(s"User: $user")
}
```

It obviously feels safer than a null checking `if` block. The author of
`getUser` method lets the consumer know what they should expect to happen when
they call it. The result would be either a `User` object or nothing. On the
other hand, thanks to the pattern matching, the consumer would be able to handle
the possible results in an elegant way. Even better, the compiler would warn you
(which can be converted to an error) if you forget to check all possible cases.

From a pragmatic point of view, one would argue that Scala is all about
scalability and asynchronous programming is one of the fundamentals of
scalability.

Instead of having some fancy keywords, magic and hiding things (like C# 5 and
others), Scala has chosen a direct answer; `Future` type. As a result, it’s more
likely that you’ll see methods returning `Future` of something in real-world
idiomatic Scala codebases:

```scala
def getUser(id: Int): Future[Option[User]] = ???

getUser(10).map {
    case None => println("User not found")
    case Some(user) => println(s"User: $user")
}
```

Again, method signature explains everything. The only difference is that it’s
async and the consumer uses `map` to match the result. So far so good.

We always see this kind of cool and small code samples in fancy programming
languages but real-world software is not that simple and isolated. You always
need to combine things together and that is where those lovely code samples
don’t look shiny anymore.

Consider the following example where we want to find the user country by its ID
asynchronously:

```scala
def getUser(id: Int): Future[Option[User]] = ???
def getCity(user: User): Future[Option[City]] = ???
def getCountry(city: City): Future[Option[Country]] = ???

def getCountryByUserId(id: Int): Future[Option[Country]] = {
    getUser(id) flatMap {
    case None => Future.successful(None)
    case Some(user) => 
        getCity(user) flatMap {
        case None => Future.successful(None)
        case Some(city) => getCountry(city)
        }
    }
}
```

Despite the method signatures expressiveness, it’s not that beautiful anymore.
Although there is a pattern here, it doesn’t look like as smooth and readable as
before.

This is one of the most common situations for a developer who is new to
functional programming where a library like Cats comes in handy.

Meet `OptionT`. It basically is a container type wrapping two other types;
another container type like `Future` and a generic type like `User`
(`OptionT[Future, User]`). And it provides more abstraction. Let’s rewrite the
above sample with `OptionT`:

```scala
def getCountryByUserId(id: Int): Future[Option[Country]] = {
    val result = for {
    user <- OptionT(getUser(id))
    city <- OptionT(getCity(user))
    country <- OptionT(getCountry(city))
    } yield {
    country
    }
    result.value
}
```

Far more beautiful, concise and readable.

Now if we go a little bit further, we can do the same with `Either`. There has
always been an argument about using `Either` vs exceptions when dealing with
`Future`. I don’t believe that all exceptions should be modelled as `Either`,
but even for those which makes sense, many developers would argue that `Either`
increases the complexity as you need to extract inner types to have access to
the inner values. Which is true when you’re dealing with real-world
applications. But the good news is that Cats support the same concept for
`Either` by `EitherT`.

So the following code:

```scala
def getUser(id: Int): Future[Either[String, User]] = ???
def getCity(user: User): Future[Either[String, City]] = ???
def getCountry(city: City): Future[Either[String, Country]] = ???

def getCountryByUserId(id: Int): Future[Either[String, Country]] = {
    getUser(id) flatMap {
    case Left(err) => Future.successful(Left(err))
    case Right(user) => 
        getCity(user) flatMap {
        case Left(err) => Future.successful(Left(err))
        case Right(city) => getCountry(city)
        }
    }
}
```

Can be rewritten using `EitherT` like this:

```scala
def getCountryByUserId(id: Int): Future[Either[String, Country]] = {
    val result = for {
    user <- EitherT(getUser(id))
    city <- EitherT(getCity(user))
    country <- EitherT(getCountry(city))
    } yield {
    country
    } 
    result.value
}
```

I’d say `Future[Either[String, Option[User]]` would be a more realistic type to
deal with, but it needs its own separate blog post which will also show that
Cats or Scalaz are not always the answer to everything and sometimes there are
simpler ways to make the code clean and readable.

### Conclusion

You don’t need to know about monads and category theory to start using Cats.
Types like `OptionT` and `EitherT` are called monad transformers but you don’t
need to know their names before start using them.

This doesn’t mean that you should ignore those theory concepts. The rule of thumb 
for learning abstract concepts is to use metaphors, and you tell me, what metaphor 
can be better than the real-world use cases of that abstract concept? Note that it's 
not just about Cats or Scalaz; most of the time, we start with the solutions rather 
than starting with a firm understanding of the actual problem.

> This post is published at [Cake Solutions blog](https://www.cakesolutions.net/teamblogs/dont-listen-to-them-learn-cats-this-way)