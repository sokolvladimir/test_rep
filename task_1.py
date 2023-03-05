# Дан массив связей пользователей. Вам необходимо реализовать функцию,
# которая принимает на вход три аргумента: информация о связях, как кортеж (tuple)
# кортежей, первое имя (str), второе имя (str). Функция должна возвращать True, если
# связь между любыми двумя заданными пользователями существует, например, если у
# двух пользователей есть общие друзья или у их друзей есть общие друзья и т.д., иначе
# False.

def check_relation(net: tuple, first: str, second: str) -> bool:
    """ Проверка наличия связи между двумя людьми.
     Возвращает True, если у двух пользователей есть общие друзья
     или у их друзей есть общие друзья и т.д., иначе False.
     : param net: массив связей пользователей.
     : param first: имя первого пользователя.
     : param second: имя второго пользователя.
     """

    relations = dict()
    for user_1, user_2 in net:
        if user_1 not in relations:
            relations[user_1] = set()
        relations[user_1].add(user_2)
        if user_2 not in relations:
            relations[user_2] = set()
        relations[user_2].add(user_1)

    queue = [first]
    checked_friends = set()
    while queue:
        user = queue.pop()
        if user == second:
            return True
        checked_friends.add(user)
        for friend in relations[user]:
            if friend not in checked_friends:
                queue.append(friend)

    return False


if __name__ == '__main__':
    net = (
        ("Ваня", "Лёша"), ("Лёша", "Катя"),
        ("Ваня", "Катя"), ("Вова", "Катя"),
        ("Лёша", "Лена"), ("Оля", "Петя"),
        ("Стёпа", "Оля"), ("Оля", "Настя"),
        ("Настя", "Дима"), ("Дима", "Маша")
    )
    assert check_relation(net, "Петя", "Стёпа") is True
    assert check_relation(net, "Маша", "Петя") is True
    assert check_relation(net, "Ваня", "Дима") is False
    assert check_relation(net, "Лёша", "Настя") is False
    assert check_relation(net, "Стёпа", "Маша") is True
    assert check_relation(net, "Лена", "Маша") is False
    assert check_relation(net, "Вова", "Лена") is True
