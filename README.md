# paste.rj1.su

personal *bin clone

## usage

```
cat paste.py | curl -F 'paste=<-' https://paste.rj1.su/
```

## setup

### database

```
sqlite3 paste.db < schema.sql
```

### uwsgi

```
[uwsgi]
socket = 127.0.0.1:55555
chdir = /usr/home/rj1/web/paste.rj1.su
wsgi-file = paste.py
```

