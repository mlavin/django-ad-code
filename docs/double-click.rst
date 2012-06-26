Using django-ad-code with DoubleClick
===========================================

`DoubleClick <http://www.google.com/doubleclick/index.html>`_ is an ad serving and ad
management tool owned and run by `Google <https://www.google.com/>`_. There is also a 
`DoubleClick for Publishers (DFP) Small Business <http://www.google.com/dfp/info/sb/index.html>`_.
This section details using django-ad-code to work with the asynchronous Google Publisher Tag
code.

This not meant to be a comprehensive guide on using DoubleClick only a guide on
integrating your DoubleClick inventory with django-ad-code.

.. note::

    This documentation is primarily for example purposes and should not be
    taken as an endorsement of DoubleClick.


Header Template
-------------------------------------------

The ``adcode/header.html`` should contain the asynchronous googletag code as well
as define the slots for your page based on the current set of placements. An
example of what this might look like is given below.

    .. code-block:: html

        {% if section and placements and not debug %}
        <script>
            var googletag = googletag || {};
            googletag.cmd = googletag.cmd || [];
            (function() {
            var gads = document.createElement('script');
            gads.async = true;
            gads.type = 'text/javascript';
            var useSSL = 'https:' == document.location.protocol;
            gads.src = (useSSL ? 'https:' : 'http:') + 
            '//www.googletagservices.com/tag/js/gpt.js';
            var node = document.getElementsByTagName('script')[0];
            node.parentNode.insertBefore(gads, node);
            })();
        </script>
        <script>
            googletag.cmd.push(function() {
                {% for placement in placements %}
                googletag.defineSlot(
                    '{{ placement.remote_id }}', [{{ placement.width }}, {{ placement.height }}], 'div-gpt-ad-{{ placement.id }}'
                ).addService(googletag.pubads());
                {% endfor %}
                googletag.pubads().enableSingleRequest();
                googletag.enableServices();
            });
        </script>
        {% endif %}

Here you can see that the ``Placement.remote_id`` stores the ad unit name.
You can adapt this to fit your needs to include additional targetting. See the prior
section on customizing the header template.


Placement Template
-------------------------------------------

The ``adcode/placement.html`` is responsible for rendering the individual placements
in the body content. The element ``id`` needs to match the ``id`` given in ``defineSlot``
call in the header. In this example we used ``'div-gpt-ad-{{ placement.id }}'`` so
we will be consistant in the placement template.

    .. code-block:: html

        <div id="div-gpt-ad-{{ placement.id }}">
            {% if debug %}
                <img alt="{{ placement }}" src="{{ placement.placeholder }}">
            {% else %}
                <script type="text/javascript">
                    googletag.cmd.push(function() {
                        googletag.display("div-gpt-ad-{{ placement.id }}"); 
                    });
                </script>
            {% endif %}
        </div>

This will render the placeholder image if ``DEBUG=True``. If necessary this can
be customized on a per section or per placement basis.

