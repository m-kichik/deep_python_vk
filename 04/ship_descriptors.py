from typing import Any


class NameDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.name = f"name_descr_{name}"

    def __get__(self, obj: Any, objtype: type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj: str, value: str):
        if type(value) is not str:
            raise TypeError(
                f"Name have to be str, {value} of type {type(value)} was set."
            )

        return setattr(obj, self.name, value)


class ShipClassDescriptor:
    def __init__(self):
        self.allowed_classes = [
            "Frigate",
            "Brig",
            "Corvette",
            "Bomb Vessel",
            "Sloop",
            "Galleon",
            "Ship of the line",
            "Cruiser",
            "Destroyer",
        ]

    def __set_name__(self, owner: Any, name: str):
        self.name = f"ship_class_descr_{name}"

    def __get__(self, obj: Any, objtype: type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj: str, value: str):
        if type(value) is not str:
            raise TypeError(
                f"Ship class have to be str, {value} of type {type(value)} was set."
            )

        if value not in self.allowed_classes:
            raise ValueError(
                "Ship class have to be one of "
                + f"{', '.join(self.allowed_classes)}, {value} was set."
            )

        return setattr(obj, self.name, value)


class YearDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.name = f"year_descr_{name}"

    def __get__(self, obj: Any, objtype: type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj: str, value: int):
        if type(value) is not int:
            raise TypeError(
                f"Year have to be int, {value} of type {type(value)} was set."
            )

        return setattr(obj, self.name, value)


class CrewSizeDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.name = f"ship_crew_size_descr_{name}"

    def __get__(self, obj: Any, objtype: type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj: str, value: int):
        if type(value) is not int:
            raise TypeError(
                f"Crew size have to be int, {value} of type {type(value)} was set."
            )

        if value < 2:
            raise ValueError(f"Crew must contain at least 2 people, {value} was set.")

        return setattr(obj, self.name, value)


class ExpeditionStateDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.name = f"expedition_state_descr_{name}"

    def __get__(self, obj: Any, objtype: type):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj: str, value: bool):
        if type(value) is not bool:
            raise TypeError(
                f"Expedition state have to be bool, {value} of type {type(value)} was set."
            )

        return setattr(obj, self.name, value)


class Ship:
    name: NameDescriptor = NameDescriptor()
    ship_class: ShipClassDescriptor = ShipClassDescriptor()
    build_year: YearDescriptor = YearDescriptor()
    crew_size: CrewSizeDescriptor = CrewSizeDescriptor()
    in_expedition: ExpeditionStateDescriptor = ExpeditionStateDescriptor()

    def __init__(
        self,
        name: str,
        ship_class: str,
        build_year: int,
        crew_size: int,
        in_expedition: bool,
    ):
        self.name = name
        self.ship_class = ship_class
        self.build_year = build_year
        self.crew_size = crew_size
        self.in_expedition = in_expedition

    def __str__(self):
        return (
            f"Ship name: {self.name}, class: {self.ship_class}, "
            + f"year of construction: {self.build_year}, crew size: {self.crew_size}, "
            + ("now in expedition." if self.in_expedition else ".")
        )


if __name__ == "__main__":
    terror = Ship("Terror", "Bomb Vessel", 1813, 67, True)
    print(terror)
