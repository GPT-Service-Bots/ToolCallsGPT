from functions.registry import register


@register
def generate_test_function_1(param_1_1: str, param_1_2: float, param_1_3: bool) -> str:
    """
    Сгенерированная тестовая функция №1.

    :param param_1_1: Тестовый параметр номер 1.1 (строка)
    :param param_1_2: Тестовый параметр номер 1.2 (число)
    :param param_1_3: Тестовый параметр номер 1.3 (булево)
    :return: Строка с результатом обработки
    """
    result = f"Параметры получены: строка='{param_1_1}', число={param_1_2}, логическое={param_1_3}"

    if param_1_3:
        result += " — логическое значение активно"
    else:
        result += " — логическое значение неактивно"

    return result


@register
def calculate_discounted_price(price: float, discount_percent: float) -> float:
    discount = price * (discount_percent / 100)
    return price - discount


@register
def apply_tax(price_with_discount: float, tax_percent: float = 20.0) -> float:
    tax = price_with_discount * (tax_percent / 100)
    return price_with_discount + tax
