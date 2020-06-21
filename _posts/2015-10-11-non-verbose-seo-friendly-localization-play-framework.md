---
layout: post
title:  "Non-verbose SEO friendly internationalization for Play framework"
date:   2015-10-11 23:42
---

[Default internationalization support in Play](https://www.playframework.com/documentation/2.4.x/ScalaI18N) works with cookies which is not SEO-friendly. It would be very nice if it was possible to use route parameters instead of cookies but as Play routes are (nicely, truly and correctly) type-safe, this will come at some cost; verbosity. Albeit it's not true for smart people who code in Scala :D

<!--more-->

> I'm using the **Scala** version of the Play framework.

Play selects the preferred user language through `Accept-Language` HTTP header out of the box, but we want the user to be able to select the language which is also supported by Play as well.

## How it works by default

`Controller` has an [implicit method](https://github.com/playframework/playframework/blob/master/framework/src/play/src/main/scala/play/api/mvc/Controller.scala#L74) `request2lang` which takes an implicit `Request[A]` and provides the corresponding `Lang` object.

All of the internationalizing APIs take an implicit `Lang` object (which is now replaced by `Messages` in Play 2.4, while the concept is the same) that would be provided by `request2lang`.

By default `request2lang` tries to get the language from cookies if available, otherwise it checks `accept-language` header, and then selects the preferred language specified in the application configuration.

There are two major approach for changing the current language in Play:

* Cookies
* Explicit route parameters

## Change the language using cookie

It's simply possible to set/change the current language by calling `withLang` method on a `Result` object.

```scala
val lang = Lang("en")
Ok(Messages("hello.world")).withLang(lang)
```

Or you can clear the selected language:

```scala
Ok(Messages("hello.world")).clearingLang
```

It sets/clears the cookie (named `PLAY_LANG`) which stores the language code behind the scene.

* Pros
  * Concise
  * Easy to use
  * Built-in
* Cons
  * Not SEO friendly (I used the same approach and Google never indexed other languages)

## Use type-safe explicit route parameters

Using cookies to store the language is not a SEO friendly approach. It seems that Google crawler ignores cookies, which makes sense.

The best approach is to use route parameters as language indicators. For example `http://www.mysite.com/fa` points to the Persian version of the site and the `http://www.mysite.com/en` points to the English one.

This way we have to add language parameter to each action and its corresponding route:

```scala
GET    /$lang<[a-z]{2}>/page/:id     controllers.PageController.view(id: Int, lang: String)
```

Read more information about this approach [here](http://mariussoutier.com/blog/2012/12/11/playframework-routes-part-2-advanced/).

* Pros
  * SEO friendly
* Cons
  * Verbose
  * Pollute all action methods with extra language parameters

## Route transformation

Explicit route parameters are too verbose and cookies are not SEO friendly. Another interesting approach is to intercept the routing process. We can fetch and remove the current language from the route and create a new path to be used for routing.

So `http://www.mysite.com/en/page/1` would be transformed to `http://www.mysite.com/page/1` and the route file would be like this:

```scala
GET    /page/:id     controllers.PageController.view(id: Int)
```

But where can we store the parsed and removed language code? The best place I've found is the headers.

Here is the filter which parses the language code and stores it to the headers:

```scala

object RouteLangFilter extends Filter with Controller {
  val langRegex = "/(.{2})(/.*)?".r
  final val routeLangKey = "x-Route-Lang"

  def apply(nextFilter: (RequestHeader) => Future[Result])(requestHeader: RequestHeader): Future[Result] = {
    requestHeader.path match {
      case langRegex(lang, path) =>
        val updatedRequest = updateLangRequest(requestHeader, lang, path)
        nextFilter(updatedRequest).map(_.withLang(Lang(lang)))
      case _ =>
        nextFilter(requestHeader)
    }
  }

  def updateLangRequest(requestHeader: RequestHeader, lang: String, path: String) = {
    requestHeader.copy(
      headers = new Headers {
        val data = (
          requestHeader.headers.toMap.updated(HeaderNames.COOKIE, updateLangCookie(requestHeader.cookies, lang)) + (routeLangKey -> Seq(lang))
        ).toSeq
      },
      path = if (path == null) "/" else path
    )
  }

  private def updateLangCookie(cookies: Cookies, lang: String): Seq[String] = {
    val updatedCookies = cookies.filter(_.name != Play.langCookieName) ++ Seq(Cookie(name = Play.langCookieName, value = lang))
    Seq(Cookies.encode(updatedCookies.toSeq))
  }
}
```

I also add the custom header `x-Route-Lang` which will come handy to distinguish processed URLs from the originals.

As its not possible to transform the route by the filters, we have to override `routeRequest` method of `Global` object in Play 2.3 or `DefaultHttpRequestHandler` in Play 2.4 to do so.

```scala
override def onRouteRequest(request: RequestHeader): Option[Handler] = {
  request.path match {
    case RouteLangFilter.langRegex(lang, path) =>
      val updatedRequest = RouteLangFilter.updateLangRequest(request, lang, path)
      super.onRouteRequest(updatedRequest)
    case _ =>
      super.onRouteRequest(request)
  }
}
```

Language code will be extracted by the `Filter` and route transformation will be done by `routeRequest`. 

As we update the cookies according to the route parameter, `request2lang` method of `Controller` works as expected. 

The only thing we have to worry about is the reverse routing. There is two approach:

* Redirecting to SEO friendly URLs
* Building `Call` helpers (ex. by adding `withLang` method) which adds the language code to the original URL

I went for the first one because I'll forgot to call the specified method in second approach for all hyper links. More importantly it's not type-safe nor automated. 

All of my controllers inherit from a special controller trait which provides them a centralized action builder. So it's super easy for me to intercept all actions of a specific controller by implementing a trait.

Supposing the base controller trait has a simple action method (mine is more complicated) which is used by child controllers:

```scala
trait BaseController extends Controller {
  def action[A](block: Request[A] => Future[Result]): Future[Result] = Action.async { implicit request =>
    processRequest(block)(request)
  }
  
  protected def processRequest[A](block: Request[A] => Future[Result])(implicit request: Request[A]) = {
    ...
  }
}
```

This would be the trait which redirects all non-SEO friendly URLs of the child controller to SEO friendly ones:

```scala
trait WithRouteLang extends BaseController {
  override protected def processRequest[A](block: Request[A] => Future[Result])(implicit request: Request[A]) = {
    request.headers.get(RouteLangFilter.routeLangKey) match {
      case None if request.method == "GET" =>
        val lang = request2lang(request)
        val maybeSlash = if (request.path.startsWith("/")) "" else "/"
        val queryStringPart = if (request.rawQueryString.isEmpty) "" else "?" + request.rawQueryString
        Future.successful(Redirect("/" + lang.code + maybeSlash + request.path + queryStringPart))
      case _ =>
        super.processRequest(block)(request)
    }
  }
}
```

As you can see `x-Route-Lang` header (`RouteLangFilter.routeLangKey`) is used to find out whether we should redirect to SEO-friendly URLs or not.

Now its just enough to implement `WithRouteLang` trait for each controller you want to be SEO-friendly internationalized.

```scala
class PageController extends BaseController with WithRouteLang {
  def view(id: Int) = action { implicit request =>
    ...
  }
}
```
