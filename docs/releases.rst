Release History
====================================

Release and change history for django-ad-code

v0.4.0 (TBD)
------------------------------------

Features
_________________

- Documentation for integrating DoubleClick tags


v0.3.1 (Released 2012-05-19)
------------------------------------

Bug Fixes
_________________

- Added missing IAB sizes from the Universal Ad Package. (Issue #10)
- Fixed minor formatting issue with template syntax error message.


v0.3.0 (Released 2012-05-16)
------------------------------------

This release made a few changes to the model fields. To upgrade you should run::

    python manage.py migrate adcode

This assumes you are using South. Otherwise you should manually add the ``priority``
column to your ``adcode_section`` table.

Features
_________________

- Added width/height properties to Placement model.
- Added priority field for Sections to resolve overlapping regex patterns.
- Additional defaults for model admin clases.
- Caching and performance improvements.
- Fixture for standard IAB ad sizes.


v0.2.0 (Released 2012-05-12)
------------------------------------

Features
_________________

- Template tag for rendering section headers and individual placements.


v0.1.0 (No public release)
------------------------------------

- Initial version.

Features
_________________

- Basic ad section/placement models.
- Context processor for accessing model data in the template.
