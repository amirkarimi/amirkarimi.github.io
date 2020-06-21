---
layout: page
title: Useful Snippets
permalink: /useful_snippets/
order: 1
---

{% for useful_snippet in site.useful_snippets %}
  <a href="{{ useful_snippet.url }}">
    {{ useful_snippet.title }}
  </a>
{% endfor %}
