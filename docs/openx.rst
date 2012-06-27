Using django-ad-code with OpenX
===========================================

`OpenX <http://www.openx.com/publisher/enterprise-ad-server>`_ is an ad server
solution with both enterprise/managed and open source editions. It integrates
with the OpenX Market for advertisers to bid on your available ad space. Here
we will detail how you can configure django-ad-code to work with the OpenX
single page call configuration based on http://www.openx.com/docs/2.8/userguide/single%20page%20call.

This will not cover setting a managed OpenX account or a self-managed server. It
will only cover integrating an existing OpenX setup with django-ad-code. It is
primarily based on using the managed OpenX server.

.. note::

    This documentation is primarily for example purposes and should not be
    taken as an endorsement of OpenX.


Header Template
-------------------------------------------

The ``adcode/header.html`` should contain the ``spcjs.php`` script tag including
the account id. The below example is using a managed OpenX account server.

    .. code-block:: html

        {% if section and placements and not debug %}
        <script type='text/javascript' src='http://d1.openx.org/spcjs.php?id=XXXX'></script>
        {% endif %}

Here ``XXXX`` is account id for the managed account id. There are additional options
that can be configured with this script tag. See *Websites & Zones -> Website properties -> 
Invocation Code* tab for more options.


Placement Template
-------------------------------------------

The ``adcode/placement.html`` is responsible for rendering the individual placements
in the body content. These placements are called zones in the OpenX documentation.

    .. code-block:: html

        <div id="div-openx-ad-{{ placement.id }}">
            {% if debug %}
                <img alt="{{ placement }}" src="{{ placement.placeholder }}">
            {% else %}
                <script type="text/javascript"><!--// <![CDATA[
                    OA_show({{ placement.remote_id }});
                // ]]> --></script>
            {% endif %}
        </div>

Here you can see the ``remote_id`` in the Placement model corresponds to the OpenX
zone id. More options exist for generating this tag which could be included in this
placement template such as a ``noscript`` option. See the *Zones > Invocation Code* tab
for a full list of these options.
