from django import template

register = template.Library()


@register.filter()
def roman_number(number):
    if number:
        number = int(number)
        ints = (
            (1000, 'M'),
            (900, 'CM'),
            (500, 'D'),
            (400, 'CD'),
            (100, 'C'),
            (90, 'XC'),
            (50, 'L'),
            (40, 'XL'),
            (10, 'X'),
            (9, 'IX'),
            (5, 'V'),
            (4, 'IV'),
            (1, 'I'),
        )
        result = ""
        for value, num in ints:
            count = int(number / value)
            result += num * count
            number -= value * count
        return result
