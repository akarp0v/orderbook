class TypesValidator:
    def __set_name__(self, owner, property_name):
        self.property_name = property_name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        key = "_" + self.property_name
        return getattr(instance, key, None)


class IntValidator(TypesValidator):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f'<{self.property_name}> must be Integer')

        if value <= 0:
            raise ValueError(f'<{self.property_name}> must be bigger than Zero')

        key = "_" + self.property_name
        setattr(instance, key, value)


class FloatValidator(TypesValidator):
    def __set__(self, instance, value):
        if not isinstance(value, (float, int)):
            raise ValueError(f'<{self.property_name}> must be Float or Integer')

        if isinstance(value, float):
            value = round(value, 2)

        if value <= 0:
            raise ValueError(f'<{self.property_name}> must be bigger than Zero')

        key = "_" + self.property_name
        setattr(instance, key, value)
