import keyboard, time
import scipy.stats

def average_list(list):
    time_sum = 0.0
    for time_wait in list:
        time_sum += float(str(time_wait))
    time_average = time_sum / len(list)
    return time_average

def user_page():
    print("\n================================================")
    print("=============You successfully login=============")
    print("================================================")
    exit(0)

def click(time_pre_up, passwd, deley):
    a = keyboard.read_event()
    if a.event_type == "down":
        t = time.time()
        b = keyboard.read_event()
        while not b.event_type == "up" and b.name == a.name:
            b = keyboard.read_event()
        time_up = time.time()
        wait_time = t - time_pre_up
        if len(passwd) != 0:
            deley.append(wait_time)
        passwd.append(a.name)
    return time_up, passwd, deley


def reader(password, n):
    list_deleys = []
    for i in range(n): # if log n = 5, if sign up n = 10
        deley = []
        passwd = []
        time_up = time.time()
        for i in range(len(password)):
            time_up, passwd, deley = click(time_up, passwd, deley)
        passwd1 = ''
        for i in passwd:
            passwd1 += i
        if passwd1 == password:
            list_deleys.append(deley)
        else:

            while passwd1 != password:
                print("password not correct")
                deley = []
                passwd = []
                time_up = time.time()
                for i in range(len(password)):
                    time_up, passwd, deley = click(time_up, passwd, deley)
                passwd1 = ''
                for i in passwd:
                    passwd1 += i
            list_deleys.append(deley)
    return list_deleys

def Stydent_kef(list_deleys):
    clear_list = []
    for deley in list_deleys:
        min_list = []
        tt = abs(scipy.stats.t.ppf(0.05, len(deley) - 1))
        for i in range(len(deley)):
            templ = []
            for j in deley:
                templ.append(j)
            yi = templ.pop(i)
            sum = 0
            for znach in templ:
                sum = sum + float(znach)
            math_exp = sum / len(templ)
            disp2 = 0
            for k in range(len(templ)):
                disp2 += (templ[k] - math_exp) ** 2
            disp2 = disp2 / (len(templ) - 1)
            disp = disp2 ** 0.5
            tp = abs((yi - math_exp) / disp)
            if tp <= tt:
                min_list.append(deley[i])
        clear_list.append(min_list)
    return clear_list

def Fisher(list_deleys):
    time_average = []
    for i in list_deleys:
        t = average_list(i)
        time_average.append(t)
    time_average_seq = []
    for time in time_average:
        time = time ** 2
        time_average_seq.append(time)
    s_max = max(time_average_seq)
    s_min = min(time_average_seq)
    Fp = s_max / s_min
    Ft = abs(scipy.stats.t.ppf(0.05, len(time_average)-1))
    if Fp > Ft:
        print("\nNot autentificate")
        exit(0)
    else:
        user_page()

def sign_up():
    name = input("Enter name:")
    password = input("Enter password: ")
    list_deleys = reader(password, 10)
    new_delay = []
    list_deleys = Stydent_kef(list_deleys)
    for deley in list_deleys:
        a = average_list(deley)
        new_delay.append(a)
    average_time = average_list(new_delay)
    line = []
    line.append(name)
    line.append(password)
    line.append(str(average_time))
    with open(name + '.txt', 'a') as file:
        for i in line:
            file.write('%s\n' % i)
    from_file_data = []
    with open(name + '.txt', 'r') as file:
        for lines in file:
            cur = lines[:-1]
            from_file_data.append(cur)
    print("Your account is created!")

def login():
    name = input("Enter name: ")
    print("Repeat your password 5 times: ")
    from_file_data = []
    with open(name + '.txt', 'r') as file:
        for lines in file:
            cur = lines[:-1]
            from_file_data.append(cur)
    list_deleys = reader(from_file_data[1], 5)
    Fisher(list_deleys)

def main():
    a = input("1. Login \n2. Sign up\n")
    if a == "1":
        login()
    elif a == "2":
        sign_up()
    else:
        main()

if __name__ == "__main__":
    main()