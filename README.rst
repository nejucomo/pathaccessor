==============
 PathAccessor
==============

This python module wraps the common "dicts-and-lists" flavor of python
data structures such that each container tracks the access path from
the root. The dicts-and-lists data structures are a common pattern,
such as the result of parsing JSON.

Example
=======

.. code:: python

   >>> from pathaccessor import MappingPathAccessor
   >>> import json
   >>>
   >>> doc = json.loads("""
   ... {
   ...   "title": "foo",
   ...   "links": [
   ...     {"text": "example", "url": "https://example.org"},
   ...     {"text": "wikipedia", "url": "https://wikipedia.org"}
   ...   ]
   ... }
   ... """)
   >>> mpa = MappingPathAccessor(doc, 'jsondoc')
   >>> print mpa["links"][1]["title"]
   Traceback (most recent call last):
      ...
   KeyError: "<MappingPathAccessor jsondoc['links'][1] {u'url': u'https://wikipedia.org', u'text': u'wikipedia'}> has no Key 'title'"


