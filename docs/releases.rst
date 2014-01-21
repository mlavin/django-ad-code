Release History
====================================

Release and change history for django-ad-code


v0.5.0 (Released TBD)
------------------------------------

- Dropped Django 1.3 support. Minimum version is now Django 1.4.2


v0.4.1 (Released 2013-06-08)
------------------------------------

- Reorganized test suite to ensure compatibility with test runner in Django 1.6
- Refactored Travis CI integration


v0.4.0 (Released 2012-12-19)
------------------------------------

A fairly minor release and users should feel safe to upgrade. Beyond some helpful
new documentation there is experimental support for Python 3.2+. This requires
using Django 1.5 or higher.

Features
_________________

- Documentation for integrating DoubleClick tags
- Documentation for integrating OpenX tags
- Travis CI integration
- Experimental Python 3 (3.2+) support


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
