def convert_grade(grade):
    result = -1
    if grade >= 90:
        result = 5
    elif grade >= 80:
        result = 4
    elif grade >= 70:
        result = 3
    elif grade >= 60:
        result = 2
    else:
        result = 1
    return result


grade = int(input('Введите вашу отметку по 100-балльной системе: '))
print(convert_grade(grade))