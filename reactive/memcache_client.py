from charmhelpers.core import unitdata
from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
)

from charms.reactive import (
    when,
    when_any,
    when_not,
    set_state,
    remove_state
)

from charms.layer.nginx import configure_site


kv = unitdata.kv()


@when_not('manual.memcache.check.available')
def check_user_provided_memcache():
    status_set('maintenance', 'Checking for memcache config')
    if not config('memcache-hosts'):
        remove_state('manual.memcache.available')
        log('Manual memcache not configured')
        status_set('active',
                   'Memcache manual configuration NOT available')
    else:
        kv.set('memcache_hosts', config('memcache-hosts').split(","))
        set_state('manual.memcache.available')
        remove_state('memcache.client.proxy.available')
        status_set('active', 'Memcache manual configuration available')
    set_state('manual.memcache.check.available')


@when('memcache.available')
def render_memcache_lb(memcache):
    """Write render memcache cluster loadbalancer
    """
    status_set('maintenance',
               'Configuring application for memcache')

    kv.set('memcache_hosts', memcache.memcache_hosts())

    status_set('active', 'Memcache available')

    remove_state('memcache.client.proxy.available')
    set_state('juju.memcache.available')


@when('nginx.available')
@when_any('juju.memcache.available',
          'manual.memcache.available')
@when_not('memcache.client.proxy.available')
def configure_memcache_proxy_hosts():
    """Write out the nginx config containing the memcache servers
    """

    memcache_servers = [{'host': host, 'port': "11211"} for host in
                        kv.get('memcache_hosts')]

    configure_site('memcache_cluster', 'memcache_cluster.conf.tmpl',
                   memcache_servers=memcache_servers)

    set_state('memcache.client.proxy.available')


@when('memcache.client.proxy.available')
@when_not('memcache.lb.proxy.available')
def render_memcache_lb_proxy():
    """Write out memcache lb proxy
    """
    status_set('maintenance', 'Configuring Memcache loadbalancing proxy')
    configure_site('memcache_lb_proxy', 'memcache_lb_proxy.conf.tmpl')
    status_set('active', 'Memcache loadbalancer/proxy configured')
    set_state('memcache.lb.proxy.available')
    set_state('memcache.client.available')


@when('memcache.client.available')
      'config.changed.memcache-hosts')
def modify_memcache_state():
    remove_state('manual.memcache.check.available')
    remove_state('juju.memcache.available')
    remove_state('memcache.client.proxy.available')
