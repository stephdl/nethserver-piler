# nethserver-piler

 yum install nethserver-piler

After for each domain you have to add a Bcc to send email to piler

```
db domains setprop nethservertest.org AlwaysBccAddress archive@piler.nethservertest.org  AlwaysBccStatus enabled
signal-event domain-modify nethservertest.org
```
you can login with a valid user on the server, else you have the default account (install nethserver-directory or nethserver-dc)

```
admin@local:pilerrocks
auditor@local:auditor
```

you have a `piler` wrapper to manage docker, do simply `piler` in the CLI

You can change the virtualhost of piler, else it is `piler.DefaultDomainOfServer`

```
config setprop piler Vhost sub.domain.org
signal-event nethserver-piler-update
```

Piler run with a systemd service `piler` which uses docker-compose

After the installation you might need to import all emails of your server to piler, do : `piler-import-email`

You can decide or not to archive the email that rspamd has flagged as potential SPAM (default is piler does not archive SPAM  `X-Spam-Flag: Yes`)

To archive all  Potential SPAM (between 6 to 20)

```
config setprop piler WantSpam enabled
signal-event nethserver-piler-update
```
