import pandas as pd
import numpy as np
import os
import math
from matplotlib import pyplot as plt
from scipy import stats

DATA_PATH = 'C:/Users/bulia/Desktop/final project data mining'

# load datasets
expb2019a = pd.read_csv(os.path.join(DATA_PATH, r'expb2019a.csv'), encoding='iso-8859-8',
                        index_col='שם ישוב').sort_index()
expc2019a = pd.read_csv(os.path.join(DATA_PATH, r'expc2019a.csv'), encoding='iso-8859-8',
                        index_col='שם ישוב').sort_index()
expb2019b = pd.read_csv(os.path.join(DATA_PATH, r'expb2019b.csv'), encoding='iso-8859-8',
                        index_col='שם ישוב').sort_index()
expc2019b = pd.read_csv(os.path.join(DATA_PATH, r'expc2019b.csv'), encoding='iso-8859-8',
                        index_col='שם ישוב').sort_index()
expb2020 = pd.read_csv(os.path.join(DATA_PATH, r'expb2020.csv'), encoding='iso-8859-8',
                       index_col='שם ישוב').sort_index()
expc2020 = pd.read_csv(os.path.join(DATA_PATH, r'expc2020.csv'), encoding='iso-8859-8',
                       index_col='שם ישוב').sort_index()
avtala = pd.read_csv(os.path.join(DATA_PATH, r'avtala.csv'), index_col='חודש',).sort_index()

hevrati = pd.read_csv(os.path.join(DATA_PATH, r'hevrati_yeshuv.csv'), index_col='רשות מקומית').sort_index()
df_hev = pd.read_table(os.path.join(DATA_PATH, r'HevratiCalcaliYeshuvim.txt'), index_col='רשות מקומית').sort_index()

hev_only_pop_sem = hevrati
#
# col_nms_drop = []
# for col in hevrati.columns:
#     col_nms_drop.append(col)


for col in hev_only_pop_sem.columns:
    if col != 'אוכלוסייה' and col != 'סמל ישוב':
        hev_only_pop_sem = hev_only_pop_sem.drop([col], axis=1)


def show_dst_bar_plt(df_dist, df_cities, avg_vec, title_fig, title_x, title_y, names_lst, width, ylim=None):
    rmse_lst = []

    for obs in df_dist.iloc:
        dist = (obs-avg_vec)**2
        mse = dist.sum(axis=0)
        rmse = math.sqrt(mse)
        rmse_lst.append(rmse)

    df_cities['rmse'] = rmse_lst
    df_cities = df_cities.sort_values(by='rmse')
    df_dst = df_cities.head(10)
    print(df_dst)
    vec_dst = 1 / df_dst['rmse']
    cts_rmse = np.array(vec_dst)
    rev_names = [name[::-1] for name in names_lst]

    fig, ax = plt.subplots()
    city_bar = ax.bar(names_lst, cts_rmse, width, color='mediumseagreen')

    ax.set_ylabel(title_y, size = 15)
    ax.set_xlabel(title_x, size = 15)
    ax.set_title(title_fig, size = 20)
    ax.set_xticklabels(rev_names)
    if ylim:
        ax.set_ylim(ylim[0],ylim[1])
    plt.xticks(rotation=30, size = 14)
    plt.show()


#### analisys on avtala df

col_names_avtala = ['גברים', 'נשים', 'אקדמאים', 'אינם אקדמאים',
                    'הבטחת הכנסה', 'דורשי עבודה שאינם עובדים', 'השמות מתוך הפניות']
avt_norm = avtala
avtala_print = avtala

for col in avt_norm.columns:
    if col in col_names_avtala:
        temp = avt_norm[col] / avt_norm['סה"כ דורשי עבודה']
        avt_norm[col] = temp

col_for_drop = ['מחוז למ"ס', 'יישוב', 'יישוב / מועצה איזורית']
for col in col_for_drop:
    avt_norm = avt_norm.drop([col], axis=1)

vec_semel = avt_norm['סמל ישוב']
vec_semel = set(np.array(vec_semel))

avg_list = []
avt_dist = pd.DataFrame()

for city in vec_semel:
    temp_df = avt_norm[avt_norm['סמל ישוב'] == city]
    if len(temp_df) >= 30:
        for col in temp_df:
            if col != 'סמל ישוב':
                avg_col = temp_df[col].sum(axis=0)/len(temp_df)
                avg_list.append(avg_col)
        avg_list.insert(0, city)
        avt_dist = avt_dist.append(pd.Series(avg_list), ignore_index= True )
        avg_list = []


names = []
for col in avt_norm.columns:
    names.append(col)
nam_dict = {}

for i in range(10):
    nam_dict[i] = names[i]

avt_dist = avt_dist.rename(columns= nam_dict)
merged_hev_avt = pd.merge(hev_only_pop_sem,avt_dist, on='סמל ישוב', )
merged_hev_avt = merged_hev_avt.set_index('סמל ישוב')

merged_hev_avt2 = merged_hev_avt.copy()
index_lst_merged = []
for i in range(len(merged_hev_avt)):
    if merged_hev_avt.iloc[i]['אוכלוסייה'] < 5000:
        index_lst_merged.append(i)
avt_dist = merged_hev_avt2.drop(merged_hev_avt2.index[index_lst_merged])
avt_dist = avt_dist.drop('אוכלוסייה',axis=1)

avg_avt = []
for col in avt_dist:
    avg = avt_dist[col].sum(axis=0)/len(avt_dist)
    avg_avt.append(avg)

avg_avt = avg_avt[1:]

avt_dist = avt_dist.drop(['סה"כ דורשי עבודה'], axis=1)



ctsnams_lst = ['קריית ביאליק','אשדוד','ערד','קריית מוצקין','קריית אתא','אשקלון','קצרין','עפולה','מעלות-תרשיחא','נצרת עילית']
x_avt_ttl = 'City'
y_avt_ttl = '1/Rmse'
title_avt = '10th closest cities for israelies average of unemployment'
#show_dst_bar_plt(avt_dist,avt_dist,avg_avt,title_avt,x_avt_ttl,y_avt_ttl,ctsnams_lst,0.3)




#### analisys on hevraty df

hevrati2 = hevrati.copy()
index_lst_hev = []
for i in range(len(hevrati)):
    if hevrati.iloc[i]['אוכלוסייה'] < 5000:
        index_lst_hev.append(i)
hevrati2 = hevrati2.drop(hevrati2.index[index_lst_hev])


hevrati = hevrati2
avg_gini = hevrati['מדד גיני'].sum(axis= 0)/len(hevrati)
avg_indic = hevrati['מדד חברתי'].sum(axis= 0 )/ len(hevrati)

vec_avg_hev = np.array([avg_gini,avg_indic])

col_names_hevrati = []
for col in hevrati.columns:
    col_names_hevrati.append(col)

df_hev_for_dist = hevrati

for i in range(7):
    df_hev_for_dist.drop(col_names_hevrati[i], axis= 'columns', inplace= True)

ctsnams_lst_hev = ['כפר יאסיף','קריית ים','פקיעין','עפולה','אשקלון','עיילבון','טירת הכרמל','נוף הגליל','אשדוד', 'גבעת זאב']
x_hev_ttle = 'City'
y_hev_ttle = '1/Rmse'
hev_title = '10th closest cities for israelies average of gini indicator and eshkol hevrati'
#show_dst_bar_plt(df_hev_for_dist,hevrati,vec_avg_hev,hev_title,x_hev_ttle,y_hev_ttle,ctsnams_lst_hev,0.3,(2.472,2.48))


##only gini
df_hev_only_gini = df_hev_for_dist.drop('מדד חברתי', axis= 'columns')
hev_title_gini = '10th closest cities for israelies average of gini indicator only'
ctsnams_lst_gini = ['כפר יאסיף','ראמה','מראר','חריש','קריית ים','בני ברק','חולון','גוליס','פקיעין', 'טבריה']

#show_dst_bar_plt(df_hev_only_gini,hevrati,vec_avg_hev[0],hev_title_gini,x_hev_ttle,y_hev_ttle,ctsnams_lst_gini,0.3)

corr_gini_eskol = stats.pearsonr(hevrati['מדד גיני'],hevrati['מדד חברתי']) ##cor - 0.75

###analisys between elections and socio-economy status

parties_dict ={'אמת' : "העבודה", 'ג' : "יהדות התורה", 'ודעם'  : "המשותפת", 'טב'  : "ימינה", 'כף'  : "עוצמה", 'ל'  : "ישראל ביתנו", 'מחל'  : "ליכוד", 'מרצ'  : "מרצ", 'פה'  : "כחולבן", 'שס'  : "שס"}

big_parties_names = [parties_dict[n][::-1] for n in parties_dict]


analysis = 'city'  # ballot

df_sep_19 = expc2019b.drop('סמל ועדה', axis=1)  # new column added in Sep 2019
df_sep_19 = df_sep_19[df_sep_19.index != 'מעטפות חיצוניות'] #removes # מעטפות חיצוניות
all_legal_vots = df_sep_19['כשרים']
if analysis == 'city':
    first_col = 5
else:
    first_col = 9
df_sep_19 = df_sep_19[df_sep_19.columns[first_col:]]  # removing "metadata" columns
df_sep_19_2 = expc2019b[expc2019b.index != 'מעטפות חיצוניות']


p = df_sep_19.sum() / df_sep_19.sum().sum()
big_parties = p[p>0.005].keys()
df_sep_all_prtys = df_sep_19.copy()
df_sep_19 = df_sep_19[big_parties]
#################
#################


def q_one(df_cits, df_hev):
    new_df = pd.concat([df_cits, df_hev], axis=1, join='inner')
    citys_num_equal = len(new_df)  # 183 rows
    citys_equal_nams = list(new_df['אמת'].keys())
    new_df_big_parties = new_df[big_parties]
    lgl_vts_vec_gini = all_legal_vots[citys_equal_nams].sum()
    lst_prty_prsnt_gini = []
    lst_prty_prsnt = []
    for prty in new_df_big_parties:
        lst_prty_prsnt_gini.append(new_df_big_parties[prty].sum() / lgl_vts_vec_gini)
        lst_prty_prsnt.append(df_cits[prty].sum() / all_legal_vots.sum())

    prsnts_df = pd.DataFrame([lst_prty_prsnt_gini, lst_prty_prsnt],columns=list(new_df_big_parties.keys()))
    #make_bar(prsnts_df)
    return new_df

def make_bar(prsnts_df):
    all_prsnts = prsnts_df.iloc[1].sort_values()[::-1]
    gini_prsnts = prsnts_df.iloc[0][all_prsnts.keys()]


    width = 0.3
    n = len(gini_prsnts)  # number of parties (10)
    names = gini_prsnts.keys()
    rev_names = [parties_dict[name][::-1] for name in list(names)]

    fig, ax = plt.subplots()    #plt.subplots()

    frst_bar = ax.bar(np.arange(n), list(all_prsnts), width, color='violet')
    scnd_bar = ax.bar(np.arange(n)+width, list(gini_prsnts), width, color='teal')

    ax.set_ylabel('אחוזי הצבעה'[::-1])
    title = ' השוואת אחוז הצבעה ארצי מול אחוז הצבעה בערים עם נתונים על מדד חברתי' [::-1]
    ax.set_title(title)
    ax.set_xticks(np.arange(n))
    ax.set_xticklabels(rev_names, rotation=90)
    ax.legend((frst_bar[0], scnd_bar[0]), ("מדד ארצי"[::-1],"מדד חברתי"[::-1]))
    plt.show()
    return fig, ax


#new_df = q_one(df_sep_19, df_hev)



def make_subplot(new_df):
    new_df_big_prtys = new_df[parties_dict.keys()]
    prsnts_pet_hev_lst = []
    for i in range(10):
        true_false_cur_city  =new_df['מדד חברתי-'] == str(i+1)
        cur_city = new_df['מחוז'][true_false_cur_city].keys()
        cur_df = new_df_big_prtys.loc[cur_city]
        prsnts_pet_hev_lst.append((cur_df.sum() / cur_df.sum().sum()).sort_values()[::-1])


    names = list(prsnts_pet_hev_lst[0].keys())
    rev_names = [parties_dict[name][::-1] for name in list(names)]



    nrow=2
    ncol=5
    fig, axes = plt.subplots(nrow, ncol)
    count=0
    title = "התפלגות הצבעה במדד חברתי: "[::-1]
    for r in range(nrow):
        for c in range(ncol):
            prsnts_pet_hev_lst[count].plot(ax=axes[r, c], kind='bar', figsize=(16,10))

            axes[r, c].set_xticklabels([parties_dict[name][::-1] for name in list(prsnts_pet_hev_lst[count].keys())],
                                       rotation=70, size=10)
            #axes[r,c].set_yticks(np.arange(5))
            axes[r, c].set_title(str(count+1) + title)
            count+=1

    fig.tight_layout()
    custom_ylim = (0, 0.6)
    plt.setp(axes, ylim=custom_ylim)

    plt.show()


#make_subplot(new_df)



def make_subplot_per_prty(new_df):
    new_df_big_prtys = new_df[parties_dict.keys()]

    pesnts_per_prty = []
    for prty in parties_dict:
        prty_lst = []
        for i in range(10):
            true_false_cur_city = new_df['מדד חברתי-'] == str(i + 1)
            cur_city = new_df['מחוז'][true_false_cur_city].keys()
            cur_df = new_df_big_prtys.loc[cur_city]
            prty_lst.append(cur_df[prty].sum() / cur_df.sum().sum())
        pesnts_per_prty.append(prty_lst)

    names = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    nrow = 2
    ncol = 5
    fig, axes = plt.subplots(nrow, ncol)
    count = 0
    title = " התפלגות לפי מדד חברתי: "[::-1]
    for r in range(nrow):
        for c in range(ncol):
            pd.DataFrame(pesnts_per_prty[count])[0].plot(ax=axes[r, c], kind='bar', figsize=(16, 10))
            axes[r, c].set_xticklabels(names, size=14, rotation=0)
            # axes[r,c].set_yticks(np.arange(5))
            axes[r, c].set_title(parties_dict[list(parties_dict)[count]][::-1] + title)
            count += 1
    fig.tight_layout()
    custom_ylim = (0,0.6)
    plt.setp(axes, ylim=custom_ylim)

    plt.show()


#make_subplot_per_prty(new_df)


### distance on elections data sets

def make_elc_dst_df(df,df2,title_fig , title_x, title_y,names_lst,width, ylim = None):
    df = df[df.columns[7:]] #just parties
    all_sum_prties = df.sum() #all votes per party
    all_votes_num = sum(all_sum_prties) #all votes
    all_sum_prties_prcnt = all_sum_prties/ all_votes_num #votes prcnt
    lst = []
    for i in range(len(df)):
        sttlmnt_sum_prties_prcnt = df.iloc[i] / sum(df.iloc[i])
        dffrnt = all_sum_prties_prcnt - sttlmnt_sum_prties_prcnt
        sqar = sum(dffrnt * dffrnt)
        lst.append(sqar)
    df2 = df2[df2.columns[7:]]  # just parties
    all_sum_prties2 = df2.sum()  # all votes per party
    all_votes_num2 = sum(all_sum_prties2)  # all votes
    all_sum_prties_prcnt2 = all_sum_prties2 / all_votes_num2  # votes prcnt
    lst2 = []
    for i in range(len(df2)):
        sttlmnt_sum_prties_prcnt2 = df2.iloc[i] / sum(df2.iloc[i])
        dffrnt2 = all_sum_prties_prcnt2 - sttlmnt_sum_prties_prcnt2
        sqar2 = sum(dffrnt2 * dffrnt2)
        lst2.append(sqar2)
    lst = np.array(lst)
    lst2 = np.array(lst2)
    avg_two_elections = (lst+lst2)/2
    df['rmse'] = avg_two_elections
    df_cities = df.sort_values(by='rmse')
    df_dst = df_cities.head(10)
    print(df_dst)

    vec_dst = 1 / df_dst['rmse']
    cts_rmse = np.array(vec_dst)
    rev_names = [name[::-1] for name in names_lst]

    fig, ax = plt.subplots()
    city_bar = ax.bar(names_lst, cts_rmse, width, color='mediumseagreen')

    ax.set_ylabel(title_y, size = 15)
    ax.set_xlabel(title_x, size = 15)
    ax.set_title(title_fig, size = 20)
    ax.set_xticklabels(rev_names)
    if ylim:
        ax.set_ylim(ylim[0], ylim[1])
    plt.xticks(rotation=30, size = 15)
    plt.show()

##removes less than 5000 population

expc2019a_2 = expc2019a.copy()
index_lsta = []
for  i in range(len(expc2019a)):
    if expc2019a.iloc[i]['בזב'] < 2777:
        index_lsta.append(i)
expc2019a_2 = expc2019a_2.drop(expc2019a_2.index[index_lsta])

expc2019b_2 = expc2019b.copy()
index_lstb = []
for  i in range(len(expc2019b)):
    if expc2019a.iloc[i]['בזב'] < 2777: #5000*5/9 because bazab is not all population
        index_lstb.append(i)
expc2019b_2 = expc2019b_2.drop(expc2019b_2.index[index_lstb])

ctsnames_2019b = ['רחובות','פתח תקווה','חיפה','נתניה','אזור','חדרה','חולון','ראש העין','צור הדסה','נשר']
expc2019b_ttle = "10 closest cities to the average elections results in 2019"
expc2019b_ttle_x = 'City'
expc2019b_ttle_y = '1/Rmse'
#make_elc_dst_df(expc2019b_2,expc2019a_2, expc2019b_ttle, expc2019b_ttle_x, expc2019b_ttle_y,ctsnames_2019b, 0.3 )

