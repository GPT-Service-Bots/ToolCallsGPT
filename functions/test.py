from functions.registry import register


@register
def accept_test_values(value_one: str, value_two: str, value_three: str) -> dict:
    """
    Функция принимает пару тестовых значений.

    Параметры:
      value_one (str): Первое тестовое значение.
      value_two (str): Второе тестовое значение.

    Возвращает:
      dict: Словарь с ключами 'value_one' и 'value_two' и соответствующими значениями.
    """
    # Дополнительная проверка типов (опционально, для обеспечения строгой типизации)
    if not isinstance(value_one, str):
        raise TypeError("value_one должно быть строкой")
    if not isinstance(value_two, str):
        raise TypeError("value_two должно быть строкой")
    if not isinstance(value_three, str):
        raise TypeError("value_three должно быть строкой")

    return {"value_one": value_one, "value_two": value_two, "value_three": value_three}
