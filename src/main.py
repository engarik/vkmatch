# TODO: Separate in different files
import src.utils
from src.values import api_version, token
import vk
import requests
import os
import time
from datetime import datetime
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


class Data(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.age = 0
        self.county = 0
        self.city = 0
        self.sex = 0
        self.political = 0
        self.religion = 0
        self.people_main = 0
        self.life_main = 0
        self.smoking = 0
        self.alcohol = 0
        self.schools = []
        self.universities = []
        self.tolerance = 0

    def set_age(self, age, tolerance=0):
        self.age = age
        self.tolerance = tolerance

    def set_country_and_city(self, country, city):
        self.county = country
        self.city = city

    def set_sex(self, sex):
        self.sex = sex

    def set_personal(self, political, religion, people_main, life_main, smoking, alcohol):
        self.political = political
        self.religion = religion
        self.people_main = people_main
        self.life_main = life_main
        self.smoking = smoking
        self.alcohol = alcohol

    def set_education(self, schools, universities):
        self.schools = schools
        self.universities = universities

    def compare(self, user):
        if self.age != 0 and user.age != 0:
            if abs(self.age - user.age) < 5:
                print('Age diff is ok')
            else:
                print('Age is not so ok')
        else:
            print('No age data')

        if self.county == user.county:
            print('Same country')
        else:
            print('Diff countries or no data')

        if self.city == user.city:
            print('same city')
        else:
            print('Diff cities or no data')

        common = get_common(self.schools, user.schools)
        if len(common) > 0:
            print('Found common schools')
            for c in common:
                print(c)
        else:
            print('No common or no data s')
        common = get_common(self.universities, user.universities)
        if len(common) > 0:
            print('Found common universities')
            for c in common:
                print(c)
        else:
            print('No common or no data u')

    def compare_for_group(self, user):
        if self.age != 0 and user.age != 0:
            if abs(self.age - user.age) <= self.tolerance:
                pass
            else:
                return False
        else:
            return False
        if self.sex != 0 and user.sex != 0:
            if self.sex == user.sex:
                pass
            else:
                return False
        else:
            return False
        if self.county != 0 and user.county != 0:
            if self.county == user.county:
                pass
            else:
                return False
        else:
            return False
        if self.city != 0 and user.city != 0:
            if self.city == user.city:
                pass
            else:
                return False
        else:
            return False
        return True

    def print_for_group(self):
        if src.values.debug:
            print('id', self.user_id, 'age', self.age, 'sex', self.sex, 'country', self.county,
                  'city', self.city)


session = vk.Session(token)
api = vk.API(session)

my_user = Data(api.users.get(v=api_version)[0]['id'])


def get_common_groups(researched_user):
    out = open('data\\users\\id%d\\common.txt' % researched_user.user_id, 'w')

    my_subs = api.users.getSubscriptions(user_id=my_user.user_id, extended=0, v=api_version)
    user_subs = api.users.getSubscriptions(user_id=researched_user.user_id, extended=0, v=api_version)

    my_public_subs_list = my_subs['groups']['items']
    users_public_subs_list = user_subs['groups']['items']

    common_public_subs = get_common(my_public_subs_list, users_public_subs_list)
    ids = ''

    for group in common_public_subs:
        ids += str(group) + ','

    if len(ids) != 0:
        common_public_subs_names = api.groups.getById(group_ids=ids, v=api_version)

        for name in common_public_subs_names:
            out.write(str(name['name']))
            out.write('\n')
            out.write(str(name['id']))
            out.write('\n')
    else:
        out.write('No common groups with this user')
    out.close()


def get_account_info(user):
    # TODO: Add collecting more info. Optimize number of requests.

    data = open('data/users/id%d/info.txt' % user.user_id, 'w')
    fields = 'bdate,sex,contacts,connections,country,city,personal,schools,universities'
    request = api.users.get(user_ids=user.user_id, fields=fields, v=api_version)[0]

    # general information

    data.write('Information\n')
    data.write(make_str(parse(request, 'id'), 'id'))
    data.write(make_str(parse(request, 'first_name'), 'first_name'))
    data.write(make_str(parse(request, 'last_name'), 'last_name'))
    data.write(make_str(parse(request, 'sex'), 'sex'))
    data.write(make_str(parse(request, 'bdate'), 'bdate'))

    age = get_age(request)
    user.set_age(age)
    data.write(make_str(age, 'age'))
    data.write('\n')

    # contacts

    data.write('Contacts\n')
    data.write(make_str(parse(request, 'mobile_phone'), 'mobile_phone'))
    data.write(make_str(parse(request, 'home_phone'), 'home_phone'))
    data.write(make_str(parse(request, 'instagram'), 'instagram'))
    data.write(make_str(parse(request, 'facebook'), 'facebook'))
    data.write(make_str(parse(request, 'twitter'), 'twitter'))
    data.write(make_str(parse(request, 'skype'), 'skype'))
    data.write(make_str(parse(request, 'livejournal'), 'livejournal'))
    data.write('\n')

    # to compare information

    data.write('To compare\n')
    country = parse(request, 'country', 'id')
    city = parse(request, 'city', 'id')
    user.set_country_and_city(country, city)
    data.write(make_str(parse(request, 'country', 'id'), 'country_id'))
    data.write(make_str(parse(request, 'city', 'id'), 'city_id'))
    data.write('\n')

    # life views and interests
    data.write('Personal\n')
    try:
        pers = request['personal']
    except KeyError:
        pers = {}

    political = parse(pers, 'political')
    religion = parse(pers, 'religion')
    people_main = parse(pers, 'people_main')
    life_main = parse(pers, 'life_main')
    smoking = parse(pers, 'smoking')
    alcohol = parse(pers, 'alcohol')

    user.set_personal(political, religion, people_main, life_main, smoking, alcohol)

    data.write(make_str(user.political, 'political'))
    data.write(make_str(user.religion, 'religion'))
    data.write(make_str(user.people_main, 'people_main'))
    data.write(make_str(user.life_main, 'life_main'))
    data.write(make_str(user.smoking, 'smoking'))
    data.write(make_str(user.alcohol, 'alcohol'))

    data.write('\n')

    #   education
    # schools
    data.write('Education\n')
    try:
        s_req = request['schools']
    except KeyError:
        s_req = {}
    s_count = 0
    schools = []

    for school in s_req:
        school_id = school['id']
        schools.append(school_id)
        s_count += 1

    # universities
    try:
        u_req = request['universities']
    except KeyError:
        u_req = {}
    u_count = 0
    universities = []

    for university in u_req:
        university_id = university['id']
        universities.append(university_id)
        u_count += 1

    user.set_education(schools, universities)

    data.write('Schools\n')
    data.write(str(s_count) + '\n')
    for school in user.schools:
        data.write(str(school) + '\n')

    data.write('Universities\n')
    data.write(str(u_count) + '\n')
    for university in user.universities:
        data.write(str(university) + '\n')
    data.write('\n')

    data.close()


def get_account_info_for_group(user, to_check):
    sex = parse(to_check, 'sex')
    user.set_sex(int(sex))

    age = get_age(to_check)
    user.set_age(age)

    country = parse(to_check, 'country', 'id')
    city = parse(to_check, 'city', 'id')
    user.set_country_and_city(country, city)


def get_common(array_a, array_b):
    common = []
    array_a.sort()
    array_b.sort()
    for element_a in array_a:
        for element_b in array_b:
            if element_a == element_b:
                common.append(element_a)
    return common


def get_photos(user):
    api_version_local = 5.80  # TODO: Update to the current api version
    response = api.photos.getAll(owner_id=user.user_id, extended=0, count=200, v=api_version_local)
    print(response)
    photos = response['items']
    print(photos)
    count = int(response['count'])
    path = "data/users/id" + str(user.user_id) + "/images/"
    print(count)

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    if count > 200:
        rem = count
        n = 0
        while rem > 0:
            if rem > 200:
                response = api.photos.getAll(owner_id=user.user_id, extended=0, offset=200 * n, count=200,
                                             v=api_version_local)
                num = 200
            else:
                response = api.photos.getAll(owner_id=user.user_id, extended=0, offset=200 * n, count=rem,
                                             v=api_version_local)
                num = rem

            photos = response['items']
            for i in range(num):
                p = requests.get(photos[i]['photo_130'])
                out = open(path + "img_" + str(i + 200 * n) + ".jpg", "wb")
                out.write(p.content)
                out.close()
            rem -= 200
            n += 1
    else:
        for i in range(count):
            p = requests.get(photos[i]['photo_130'])
            out = open(path + "img_" + str(i) + ".jpg", "wb")
            out.write(p.content)
            out.close()


def parse(to_parse, key, extra_key=''):
    try:
        if to_parse[key] != '' and to_parse[key] != []:
            if extra_key != '':
                return to_parse[key][extra_key]
            else:
                return to_parse[key]
        else:
            return 0
    except KeyError:
        return 0


def make_str(to_str, key):
    return key + '\t' + str(to_str) + '\n'


def get_age(res):
    try:
        date = res['bdate']
        if len(date) > 5:
            try:
                today = datetime.today()
                b_day = datetime.strptime(date, "%d.%m.%Y")
                return (today - b_day).days // 365
            except ValueError:
                print(date)
                return 0
        else:
            return 0
    except KeyError:
        return 0


def scan(group_id):
    result = open('data\\groups\\result_%s.txt' % group_id, 'w')
    result.write(group_id)
    result.write('\n')
    group_members = int(api.groups.getMembers(group_id=group_id, count=0, v=api_version)['count'])
    flag = True
    time.sleep(0.5)
    offset = 0
    new_len = 0
    prev_len = 0

    progressbar["value"] = 0
    progressbar["maximum"] = group_members

    start = time.time()
    if abs(group_members - len(group_response)) > 20 or len(group_response) == 0:
        print(abs(group_members - len(group_response)))
        group_response.clear()
        if src.values.debug:
            print('debug mem', group_members)
            print('debug len', len(group_response))
        if group_members > 500:
            count = 500
        else:
            count = group_members
        while flag:
            code = '''
                var group_id = "%s";
                var offset = %d;
                var count = %d;
                var size = count;
                var res = API.groups.getMembers({ "group_id":group_id , "sort": "id_asc", "offset": offset, "count": count, "fields":"sex,city,country,bdate"});
                var members = res["count"];
                res = res["items"];
                var loop = 1;
                offset = offset + 1000;
    
                while(loop <= 24 && offset + count <= members)
                {
                loop = loop + 1;
                size = size + 1000;
                offset = offset + count;
                res = res + API.groups.getMembers({ "group_id":group_id , "sort": "id_asc", "offset": offset, "count": count, "fields":"sex,city,country,bdate"})["items"];
                }
    
    
                return res;''' % (group_id, offset, count)

            before = time.time()
            response = api.execute(code=code, v=api_version)
            try:
                group_response.extend(response)
            except TypeError:
                response = []

            if src.values.debug:
                print("Took time", time.time() - before)

            new_len += len(response)
            progressbar["value"] = new_len
            progressbar.update()
            offset += new_len - prev_len
            prev_len = new_len
            if offset + count > group_members:
                count = offset - group_members
            if abs(new_len - group_members) < 20:
                flag = False
    if src.values.debug:
        print(len(group_response))

        print('total', time.time() - start)

    match = []
    progressbar["value"] = 0

    for person in group_response:
        to_match = Data(person['id'])
        get_account_info_for_group(to_match, person)
        if ideal_user.compare_for_group(to_match):
            to_match.print_for_group()
            match.append(to_match.user_id)

    result.write(str(len(match)))
    result.write('\n')
    result.write("sex:%d age:%d tolerance:%d country:%d city:%d\n" % (
        ideal_user.sex, ideal_user.age, ideal_user.tolerance, ideal_user.county, ideal_user.city))
    for match_id in match:
        result.write('https://vk.com/id' + str(match_id))
        result.write('\n')
    print('match', len(match))


def click_button_start_group():
    print('clicked')
    group = group_txt_msg.get()
    print('group', group_txt_msg.get())

    ideal_user.set_age(int(age_txt_msg.get()), int(tol_txt_msg.get()))
    print('age', age_txt_msg.get())
    print('tol', tol_txt_msg.get())

    ideal_user.set_country_and_city(int(country_txt_msg.get()), int(city_txt_msg.get()))
    print('country', country_txt_msg.get())
    print('city', city_txt_msg.get())

    ideal_user.set_sex(int(sex_val.get()))
    print('sex', sex_val.get())
    ideal_user.print_for_group()
    scan(group)
    messagebox.showinfo("Success", "You can find result in data/groups directory")


def click_button_start_user():
    user_id = src.utils.get_user_id(user_txt_msg.get(), api)
    researched_user = Data(user_id)

    try:
        os.mkdir("data\\users\\id" + str(researched_user.user_id))
    except FileExistsError:
        pass

    get_common_groups(researched_user)
    get_account_info(researched_user)
    get_photos(researched_user)
    messagebox.showinfo("Success", "You can find result in data/users directory")


window = Tk()
window.title("Vk Match")
window.geometry('300x260')
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Group')
tab_control.add(tab2, text='Person')
tab_control.pack(expand=1, fill='both')

group_lbl = Label(tab1, text="Group id:", font=("Open sans", 15))
group_lbl.grid(column=0, row=0, columnspan=2)

group_txt_msg = StringVar()
group_txt = Entry(tab1, textvariable=group_txt_msg, width=22, font=("Open sans", 12))
group_txt.grid(column=2, row=0, columnspan=2)
group_txt.focus()

sex_lbl = Label(tab1, text="Sex:", font=("Open sans", 15))
sex_lbl.grid(column=0, row=1, columnspan=2)

sex_val = IntVar()
sex_m_chk = Radiobutton(tab1, value=2, variable=sex_val, text='Man', font=("Open sans", 12))  # , var=chk_state
sex_m_chk.grid(column=2, row=1)

sex_w_chk = Radiobutton(tab1, value=1, variable=sex_val, text='Woman', font=("Open sans", 12))  # , var=chk_state
sex_w_chk.grid(column=3, row=1)

age_lbl = Label(tab1, text="Age:", font=("Open sans", 15))
age_lbl.grid(column=0, row=2)

age_txt_msg = StringVar()
age_txt = Entry(tab1, textvariable=age_txt_msg, width=3, font=("Open sans", 12))
age_txt.grid(column=1, row=2)
age_txt.insert(0, '0')

tol_lbl = Label(tab1, text="Tolerance:", font=("Open sans", 15))
tol_lbl.grid(column=2, row=2)

tol_txt_msg = StringVar()
tol_txt = Entry(tab1, textvariable=tol_txt_msg, width=3, font=("Open sans", 12))
tol_txt.grid(column=3, row=2)
tol_txt.insert(0, '0')

country_lbl = Label(tab1, text="Country:", font=("Open sans", 15))
country_lbl.grid(column=0, row=3, columnspan=2)

country_txt_msg = StringVar()
country_txt = Entry(tab1, textvariable=country_txt_msg, width=22, font=("Open sans", 12))
country_txt.grid(column=2, row=3, columnspan=2)
country_txt.insert(0, '0')

city_lbl = Label(tab1, text="City:", font=("Open sans", 15))
city_lbl.grid(column=0, row=4, columnspan=2)

city_txt_msg = StringVar()
city_txt = Entry(tab1, textvariable=city_txt_msg, width=22, font=("Open sans", 12))
city_txt.grid(column=2, row=4, columnspan=2)
city_txt.insert(0, '0')

start = Button(tab1, text="Start", font=("Open sans", 15), command=click_button_start_group)
start.grid(column=0, row=11, columnspan=4)

progressbar = ttk.Progressbar(tab1, orient="horizontal", length=300, mode="determinate")
current_value = 0
max_value = 100
progressbar["value"] = current_value
progressbar["maximum"] = max_value
progressbar.grid(column=0, row=12, columnspan=4)

user_lbl = Label(tab2, text="User id:", font=("Open sans", 15))
user_lbl.grid(column=0, row=0, columnspan=2)

user_txt_msg = StringVar()
user_txt = Entry(tab2, textvariable=user_txt_msg, width=24, font=("Open sans", 12))
user_txt.grid(column=2, row=0, columnspan=2)
user_txt.focus()

get_photos_bool = IntVar()
get_photos_checkbutton = Checkbutton(tab2, text="Photos", font=("Open sans", 12), variable=get_photos_bool)
get_photos_checkbutton.grid(column=0, row=1, columnspan=2)

get_cmn_groups_bool = IntVar()
get_cmn_groups_bool.set(1)
get_cmn_groups_checkbutton = Checkbutton(tab2, text="Common groups", font=("Open sans", 12),
                                         variable=get_cmn_groups_bool)
get_cmn_groups_checkbutton.grid(column=2, row=1, columnspan=2)

group_btn = Button(tab2, text="Get info", font=("Open sans", 15), command=click_button_start_user)
group_btn.grid(column=0, row=2, columnspan=4)

ideal_user = Data(0)
group_response = []

window.focus_force()
window.mainloop()
