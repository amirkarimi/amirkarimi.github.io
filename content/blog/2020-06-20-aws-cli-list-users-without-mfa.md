---
category: Useful Snippets
date: 2020-06-20
keywords: useful snippets, aws, boto3, AWS IAM, script
slug: aws-cli-list-users-without-mfa
template: post.html
title: List AWS Users Without MFA
---

To list users who haven't enabled MFA on their AWS accounts:

<!--more-->

Install `boto3`:

```bash
pip install boto3
```

And run:

```python
import boto3

iam = boto3.resource('iam')

for user in iam.users.all():
  has_any = any(user.mfa_devices.all())
  if not has_any:
    print(user.name)
```
