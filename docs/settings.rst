Available Settings
====================================

Below are the settings available for configuring django-ad-code.


``ADCODE_PLACEHOLDER_TEMPLATE``
------------------------------------

The placement model has a ``placeholder`` property. This is used to render
a placeholder image for debugging. This setting can be used to configure
the placeholder image service used.

Default: ``'http://placehold.it/{width}x{height}'``


``ADCODE_CACHE_TIMEOUT``
------------------------------------

This configures the cache timeout for the section and placement cache.

Default: 12 hours
