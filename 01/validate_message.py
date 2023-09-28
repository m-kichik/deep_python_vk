class SomeModel:
    def predict(self, message: str) -> float:
        return int(len(message.split()) > 1)


def predict_message_mood(
    message: str,
    model: SomeModel(),
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    prediction = model.predict(message=message)

    if prediction < bad_thresholds:
        return "неуд"
    if bad_thresholds <= prediction <= good_thresholds:
        return "норм"

    return "отл"


if __name__ == "__main__":
    some_model = SomeModel()

    assert predict_message_mood("Чапаев и пустота", some_model) == "отл"
    assert predict_message_mood("Вулкан", some_model) == "неуд"
