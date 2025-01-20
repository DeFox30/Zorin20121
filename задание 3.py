def santa_users(users):
    users_slovar = {}

    for user in users:
        name = user[0]

        if len(user)>1:
            index = user[1]
        else:
            index = None

        users_slovar[name] = index

    return users_slovar

users_list = [["Максим Нан", 12345], ["Александр сан"], ["Радик тян", 12354], ["Господин Павел", 14532]]
res=santa_users(users_list)
print(res)
