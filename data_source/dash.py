import streamlit as st
import pandas as pd
import openpyxl
import plotly.express as px
from ummalqura.hijri_date import HijriDate


st.set_page_config(page_title="لوحة بيانات حج 1444هـ")
st.title("Dashboard|لوحة البيانات")
st.subheader("لوحة معلومات أعداد الحجاج لعام 1444هـ")



def date_slider(start_date,end_date):
    global df_filterd_dates 
    global df_filterd_gender
    global df_filterd_port
    global df_day_age

    df_filterd_dates = df_day[df_day[entry_date] >= start_date]
    df_filterd_dates = df_filterd_dates[df_day[entry_date] <= end_date]

    df_filterd_gender = df_gender[df_gender[entry_date] >= start_date]
    df_filterd_gender = df_filterd_gender[df_gender[entry_date] <= end_date]

    df_filterd_port = df_port[df_port[entry_date] >= start_date]
    df_filterd_port = df_filterd_port[df_port[entry_date] <= end_date]

    df_day_age = df_day[df_day[entry_date] >= start_date]
    df_day_age = df_day_age[df_day_age[entry_date] <= end_date]
    


st.sidebar.write(""" لوحة معلومات أعداد الحجاج لعام 1444هـ  \n  حسب تاريخ الدخول ونوع المنفذ والفئة العمرية و الجنس  \n  تم إستخدام ثلاث مصادر للبيانات من البيانات المفتوحة لوزارة الحج والعمرة  \n  يمكنك الإطلاع على المصادر من الأسفل  \n  وايضاً الإطلاع على الكود المصدر من Github


""")
st.sidebar.write(""" Data Source -  [Data_1](https://od.data.gov.sa/Data/ar/dataset/numbers-of-pilgrims-entering-the-year-1444-by-port-per-day) - 
[Data_2](https://od.data.gov.sa/Data/ar/dataset/numbers-of-pilgrims-entering-the-year-1444-by-age-group-by-day) - 
[Data_3](https://od.data.gov.sa/Data/ar/dataset/number-of-pilgrims-entering-the-year-1444-by-gender-per-day)\n
od.data.gov.sa
""")
st.sidebar.write("---")
st.sidebar.write("بواسطة : أحمد السريحي ")
st.sidebar.write("""Contact: [Linkedin](https://www.linkedin.com/in/ahmed-a-alsuraihi-574a04207) - [Twitter](http://twitter.com/adsecu) - 
[Github](https://github.com/ADsecu)""")

df_day = pd.read_excel('data_source/day.xlsx')
df_gender = pd.read_excel('data_source/gender.xlsx')
df_port = pd.read_excel('data_source/port.xlsx')

entry_date = 'تاريخ الدخول'
entry_date_gr = 'تاريخ الدخول ميلادي'
count = 'عدد الحجاج'
male = 'الذكور'
female = 'الاناث'
age_bin = 'الفئة العمرية'
port = 'نوع المنفذ'
total = 'المجموع'

df_day[entry_date_gr] = df_day[entry_date]
df_gender[entry_date_gr] = df_day[entry_date]
df_port[entry_date_gr] = df_day[entry_date]
for i in df_day[entry_date_gr]:
    dd = i.split("-")
    um = HijriDate(int(dd[0]),int(dd[1]),int(dd[2]))
    gr_date = "{}-{}-{}".format(um.year_gr, um.month_gr , um.day_gr)
    df_day[entry_date_gr] = df_day[entry_date_gr].replace(i,"{}".format(gr_date))

for i in df_gender[entry_date_gr]:
    dd = i.split("-")
    um = HijriDate(int(dd[0]),int(dd[1]),int(dd[2]))
    gr_date = "{}-{}-{}".format(um.year_gr, um.month_gr , um.day_gr)
    df_gender[entry_date_gr] = df_gender[entry_date_gr].replace(i,"{}".format(gr_date))

for i in df_port[entry_date_gr]:
    dd = i.split("-")
    um = HijriDate(int(dd[0]),int(dd[1]),int(dd[2]))
    gr_date = "{}-{}-{}".format(um.year_gr, um.month_gr , um.day_gr)
    df_port[entry_date_gr] = df_port[entry_date_gr].replace(i,"{}".format(gr_date))








with st.expander("-", expanded=True):
    f_port_1 = df_port[df_port[port] == 'برا']
    f_port_2 = df_port[df_port[port] == 'بحر']
    f_port_3 = df_port[df_port[port] == 'جوا']
    max_day = df_day[df_day[count] == df_day[count].max()]
    min_day = df_day[df_day[count] == df_day[count].min()]
    
    
    

    col1,col2,col3 = st.columns(3)
    with col1:
        
        st.info("أول دخول من الجو **{}**".format(f_port_3[entry_date].min()), icon='✈️')

    with col2:
       
        st.info("أول دخول من البر **{}**".format(f_port_1[entry_date].min()), icon='🚌')
    with col3:
       
        st.info("أول دخول من البحر **{}**".format(f_port_2[entry_date].min()), icon='🚢')
max1,max2,max3 = st.columns(3)
with max1:
    with st.expander("**أعلى عدد حجاج باليوم**", expanded=True):
        st.success("**{:,}**".format(max_day[count].max()))
        st.write("بتاريخ **{}**".format(str(max_day[entry_date].min())))
with max2:
    with st.expander("**أقل عدد حجاج باليوم**",expanded=True):
        
        st.success("**{:,}**".format(min_day[count].min()))
        st.write("بتاريخ **{}**".format(min_day[entry_date].min()))
with max3:
    with st.expander("**متوسط عدد الحجاج باليوم**", expanded=True):
        st.success("**{:,}**".format(round(df_day[count].mean())))
        st.write(" None ")
        

with st.expander("-", expanded=True):

    start_date,end_date = st.select_slider("تاريخ الدخول - الخط الزمني {} يوم".format(len(df_day[entry_date].unique())),options=sorted(df_day[entry_date].unique()) , 
                            value=(df_day[entry_date].min(), df_day[entry_date].max()))
    date_slider(start_date,end_date)
    port_1 = df_filterd_port[df_filterd_port[port] == 'برا']
    port_2 = df_filterd_port[df_filterd_port[port] == 'بحر']
    port_3 = df_filterd_port[df_filterd_port[port] == 'جوا']


    

    #df_day_age = df_day_age[df_day_age[sorted(age_bin)]]

    
    col1,col2,col3,col4, = st.columns(4,gap='small')
    p_male = df_filterd_gender[male].sum() / df_filterd_dates[count].sum() *100
    p_female = df_filterd_gender[female].sum() / df_filterd_dates[count].sum() *100
    
    with col1:
        st.metric("**إجمالي الحجاج**","{:,}".format(df_filterd_dates[count].sum()))



    with col2:
        st.metric(':airplane_arriving: المنفذ الجوي',"{:,}".format(port_3[count].sum()))
    with col3:
        st.metric(":bus: المنفذ البري","{:,}".format(port_1[count].sum()))
    with col4:
        st.metric(':ship: المنفذ البحري',"{:,}".format(port_2[count].sum()))

        
chart1,chart2 = st.columns(2)
with chart1:
    with st.expander("📊", expanded=True):
        age_bin_checkbox = None
        if st.checkbox("الفئات العمرية"):
            age_bin_checkbox = age_bin
            
        fig = px.bar(df_day, x=entry_date_gr ,y=count,color=age_bin_checkbox,)
        fig.update_layout(
    title=dict(text="الرسم البياني لإجمالي الحجاج", font=dict(size=28), automargin=True)
)
        st.plotly_chart(fig,use_container_width=True)
    with chart2:
        with st.expander("📊", expanded=True):

            fig = px.bar(df_day_age, x=age_bin ,y=count,color=age_bin)
            fig.update_layout(
    title=dict(text="الفئة العمرية", font=dict(size=28), automargin=True)
)
            st.plotly_chart(fig,use_container_width=True)

col1,col2 = st.columns(2)
with col1:
    with st.expander("📊", expanded=True):
        fig = px.line(df_filterd_port, x=entry_date_gr ,y=count, color=port)
        fig.update_layout(
    title=dict(text="الرسم البياني حسب المنفذ", font=dict(size=28), automargin=True)
)
        st.plotly_chart(fig,use_container_width=True)
        st.write("{}")

with col2:
    with st.expander("📊", expanded=True):
        
        fig = px.pie(df_filterd_gender, values=[p_male,p_female], names=[male,female], hole= .5)
        fig.update_layout(
    title=dict(text="حسب الجنس", font=dict(size=28), automargin=True)
)
        st.plotly_chart(fig,use_container_width=True)
            







