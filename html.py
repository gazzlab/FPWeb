from xml.etree.ElementTree import Element, SubElement, tostring


class HTML(object):

    def __init__(self, element=None):
        if element is None:
            element = Element('html')
        self.root = self.element = element
        self.prev = None

    def __getattr__(self, tag):
        e = SubElement(self.element, tag)
        e.root = self.root
        return HTML(e)

    def __iadd__(self, other):
        return self._append(self.element, other)

    def _append(self, to, other):
        if isinstance(other, basestring):
            if to.text is None:
                to.text = other
            else:
                to.text += other
        elif isinstance(other, Element):
            to.append(other)
        elif isinstance(other, HTML):
            if other.root == self.root:
                raise ValueError('What are you doing?', other)
            to.append(other.current)
        else:
            raise ValueError('Must only add strings or Elements', other)
        return self

    def __call__(self, *content, **kw):
        for it in content:
            self._append(self.element, it)
        self.element.attrib.update((k.rstrip('_'), v) for k, v in kw.iteritems())
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

    def __repr__(self):
        return '<HTML:%r 0x%x>' % (self.element, id(self))

    def _stringify(self, str_type):
        return tostring(self.root, method='html')

    def __str__(self):
        return self._stringify(str)

    def __unicode__(self):
        return self._stringify(unicode)

    def __iter__(self):
        return iter([str(self)])


if __name__ == '__main__':
    ht = HTML()
    with ht.head as h:
        h.title('Bananas')
    print ht
