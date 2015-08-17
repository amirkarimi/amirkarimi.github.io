---
layout: post
title:  "Why Functional Programming?"
date:   2015-08-17 23:39
---
There are plenty of reasons why functional programming are becoming mainstream, but I came across the one I think is the most visible.

<!--more-->

Several days ago we were improving the file exporting functionality of an enterprise software, specially for exporting large Excel files. 

The legacy code loads the data, creates an Excel file in memory, writes the data to the excel file and send it to the user over the HTTP.

This solution **brings the data to the code**, which is inefficient.

Instead, we decided to **bring the code to the data** which was very efficient. We could generate a 500MB CSV (as CSV is more compatible with streaming than Excel) file without using more than several kilo bytes of RAM. 

We built a function which gets an entity as input and returns a CSV row (the code), then gave it to another function which maps the data to the CSV rows using the provided function (bringing the data to the code).

This is the idea behind map/reduce and it truly is an efficient approach.

The request for such scenarios are increasing, and of course, functional programming shines here and makes everything super simple and clean. The same idea is implemented in Scala, Java, .NET, Ruby, Python, Node, etc. yet all of them are implemented with **functional programming** in mind.

This is a more advanced sample in Scala on Play using [ReactiveMongo](http://www.reactivemongo.org/) and [Iteratees](https://www.playframework.com/documentation/2.4.x/Iteratees):

{% highlight scala %}
val content = Enumerator.outputStream { output =>
  val writer = CSVWriter.open(output)
  
  // Write headers
  writer.writeRow(csvCols)
  
  // Ready to fetch
  val enumerate = purchaseOrderReportService
    .findQuery(query)
    .cursor[PurchaseOrderReportModel]
    .enumerate()
    
  val iteratee = Iteratee.foreach[PurchaseOrderReportModel] { order =>
  
    val cells = Seq(
      order.student.info.firstName,
      order.student.info.lastName,
      //...
    )

    // Write body
    writer.writeRow(cells.flatten)
  }
  
  enumerate.run(iteratee)
}

Result(
  header = ResponseHeader(200, Map(CONTENT_DISPOSITION -> s"attachment; filename=export.csv")),
  body = content
)
{% endhighlight %}

This code even controls the data follow based on the client (consumer) speed which is more advanced and hard-to-implement scenario.