# Memcache-Client

This layer will maintain an NGINX loadbalancing proxy to your memcache
cluster either by service discovery via Juju, or by user provided config.

You can supply your own memcache hosts to this layer as a comma separated
list inside of double quotes e.g. "192.168.1.101,192.168.1.102,192.168.1.103".

If you do not supply memcache host(s) via config, this layer will wait for a
relation to memcache before setting the flag
`memcache.client.available`.

Once the flag `memcache.client.available` you can rest assured that your
application can talk to memcache via `http://127.0.0.1:11211`.


### Authors
* James Beedy <jamesbeedy@gmail.com>

### Copyright
* James Beedy (c) 2017 <jamesbeedy@gmail.com>

### License
* AGPLv3 - see `LICENSE` file
