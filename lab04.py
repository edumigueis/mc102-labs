def format_to_string(list):
    ret = ""
    for item in list:
        ret += item + ", "
    return ret[0:-2]


def get_fights(n):
    ret = []
    for f in range(n):
        fight = input().split(" ")
        ret.append((fight[0], fight[1]))
    return ret


def get_fight_count(fights, pets):
    count = 0
    for pss_fight in fights:
        if pss_fight[0] in pets and pss_fight[1] in pets:
            count += 1
    return count


def get_procedures(line):
    split_line = line.split(" ")
    ret = {}
    for f in range(0, len(split_line), 2):
        ret[split_line[f]] = split_line[f+1]
    return ret


def get_pet_procedures(n):
    ret = {}
    for f in range(n):
        fight = input().split(" ")
        ret[fight[0]] = fight[1]
    return ret


def build_unavailable_proc_msg(pets):
    msg = ""
    for pet in pets:
        msg += "Animal " + pet + " solicitou procedimento não disponível.\n"
    return msg


def generate_report(day, n_fights, procedures, pet_procedures):
    print("Dia: " + str(day))
    print("Brigas: " + str(n_fights))
    pets_treated = []
    pets_missing_proc = []
    pets_untreated = []

    for key in pet_procedures:
        try:
            if procedures[pet_procedures[key]] == 0:
                pets_untreated.append(key)
            else:
                procedures[pet_procedures[key]] = int(
                    procedures[pet_procedures[key]]) - 1
                pets_treated.append(key)
        except:
            pets_missing_proc.append(key)

    if len(pets_treated) > 0:
        print("Animais atendidos: " + format_to_string(pets_treated))
    if len(pets_untreated) > 0:
        print("Animais não atendidos: " + format_to_string(pets_untreated))
    print(build_unavailable_proc_msg(pets_missing_proc))


def main():
    day_count = int(input())
    for day in range(day_count):
        n_fights_inp = int(input())
        fights = get_fights(n_fights_inp)
        procedures = get_procedures(input())
        pets_present = int(input())
        pet_procedures = get_pet_procedures(pets_present)
        n_fights = get_fight_count(fights, [key for key in pet_procedures])
        generate_report(day + 1, n_fights, procedures, pet_procedures)


main()
