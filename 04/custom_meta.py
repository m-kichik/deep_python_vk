from typing import Any, Callable


class CustomMeta(type):
    def __new__(mcs: Any, name: str, bases: tuple, namespace: dict):
        private_pattern = f"_{name}__"

        def define_custom_name(_attr_name: str) -> str:
            if _attr_name.startswith("__") and _attr_name.endswith("__"):
                return _attr_name
            elif private_pattern in _attr_name:
                return (
                    private_pattern + "custom_" + _attr_name.split(private_pattern)[1]
                )
            elif _attr_name.startswith("__"):
                return "__custom_" + _attr_name[2:]
            elif _attr_name.startswith("_"):
                return "_custom_" + _attr_name[1:]
            else:
                return "custom_" + _attr_name

        def custom_setattr(setattr_method: Callable):
            def inner(_cls, _name, _value):
                return setattr_method(_cls, define_custom_name(_name), _value)

            return inner

        names = list(namespace.keys())
        for attr_name in names:
            new_attr_name = define_custom_name(attr_name)
            value = namespace.pop(attr_name)
            namespace[new_attr_name] = value

        class_ = super().__new__(mcs, name, bases, namespace)
        class_.__setattr__ = custom_setattr(class_.__setattr__)
        return class_


if __name__ == "__main__":
    SomeClass = CustomMeta("SomeClass", (), {"value": 42})
    assert SomeClass.custom_value == 42
