# Cloudflare Provisioner

This is a serverless project that allows to create Cloudflare resources (DNS Records) with AWS CloudFormation

## Getting started

1. Add an API token to a secret in secrets manager (`solutions/cloudflare/api-token`)
2. Deploy the serverless application
```
$ sls deploy
```
3. Create a custom resource in CloudFormation:
```yaml
Resources:
  TestDnsRecord:
    Type: Custom::CloudflareDnsRecord
    Properties:
      ServiceToken: <lambda-function-arn>
      Name: test.example.com
      Type: CNAME
      Content: load-balancer-dns.amazonaws.com
      ZoneId: 8059d39ea71c44813c40008d479856e4
      Comment: A test record
```

## Custom resource syntax

The CloudFormation custom resource syntax is the following:

```json
{
  "ServiceToken": "string",
  "Name": "string",
  "Type": "string",
  "Content": "string",
  "ZoneId": "string",
  "Comment": "string",
  "Proxied": "bool",
  "Ttl": "int",
}
```

|Field|Description|Required|Default|
|-----|-----------|--------|-------|
|`Name`|The name of the DNS record|yes|`n/a`|
|`Type`|The type of DNS record (`A`, `AA`, `AAAA`, `CNAME`)|yes|`n/a`|
|`Content`|The content of the DNS record|yes|`n/a`|
|`ZoneId`|The cloudflare zone id| yes|`n/a`|
|`Comment`|A comment for the DNS record | no|`n/a`|
|`Proxied`|Wether the DNS record should be proxied|no|`false`|
|`Ttl`|The time to live for the DNS record|no|`600`|
