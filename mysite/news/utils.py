class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()


    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:          # иначе это объект и берем его атрибут title
            return s.title.upper()