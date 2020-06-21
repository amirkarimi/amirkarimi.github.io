---
layout: page
date: 2020-05-20
title: AWS CLI Useful Scripts
---

## List users who haven't enabled MFA

```python
import boto3

iam = boto3.resource('iam')

for user in iam.users.all():
  has_any = any(user.mfa_devices.all())
  if not has_any:
    print(f"{user.name}")
```
