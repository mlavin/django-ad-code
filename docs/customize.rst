Customizing the Ad Templates
====================================

Setting up the templates to render your ad code is straight forward. This
section details how the appropriate templates are discovered when using
the django-ad-code template tags.


Customizing ``render_section_header`` Template
------------------------------------------------

``render_section_header`` renders the header content for the current section. If
no section was matched then it will not render anything. This template tag looks
for the template ``adcode/{{ section.slug }}/header.html`` then ``adcode/header.html``
where ``{{ section.slug }}`` is the slug of the current matched section. In most
cases it will be sufficient to define ``adcode/header.html`` to use for all
sections.

The following items are passed into the context for this template.

    - ``section``: The current adcode Section
    - ``placements``: The full list of Placements for this section
    - ``debug``: The value of ``settings.DEBUG``
    - ``MEDIA_URL``: The value of ``settings.MEDIA_URL``
    - ``STATIC_URL``: The value of ``settings.STATIC_URL``


Customizing ``render_placement`` Template
------------------------------------------------

``render_placement`` renders a given placement by the slug. If the placement could
not be found then it will not render anything. The template search order is
``adcode/{{ section.slug }}/{{ placement.slug }}-placement.html``,
``adcode/{{ section.slug }}/placement.html`` then ``adcode/placement.html``. This
allows you to customize each placement individually if needed or on a section or
simply a global basis. Many use cases will only require defining ``adcode/placement.html``.

The following items are passed into the context for this template.

    - ``section``: The current adcode Section
    - ``placement``: The current Placement to be rendered
    - ``debug``: The value of ``settings.DEBUG``
    - ``MEDIA_URL``: The value of ``settings.MEDIA_URL``
    - ``STATIC_URL``: The value of ``settings.STATIC_URL``

The Placement model contains a ``placeholder`` property that can be used for local
development to test the layout. An example ``adcode/placement.html`` might look
something like below.

    .. code-block:: html

        {% if debug %}
            <img alt="{{ placement }}" title="{{ placement }}" src="{{ placement.placeholder }}">
        {% else %}
            <!-- Here you would put the actual ad code needed -->
        {% endif %}

This placeholder image will match the size of the placement. By default this will
use `Placehold.it <http://placehold.it/>`_ but you are free to customize it with
the ``ADCODE_PLACEHOLDER_TEMPLATE`` setting.

    .. code-block:: python

        # Default setting (not required in settings.py)
        ADCODE_PLACEHOLDER_TEMPLATE = 'http://placehold.it/{width}x{height}'

        # Use placekitten instead
        ADCODE_PLACEHOLDER_TEMPLATE = 'http://placekitten.com/{width}/{height}'
