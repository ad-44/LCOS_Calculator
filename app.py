#%% Imports
import streamlit as st
import pandas as pd
import function
from bdd import rawprices
import pyomo.environ as pyo
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Interface options
st.set_page_config(layout="wide")

#Main title
st.title("Levelized Cost of Storage Calculator")
st.divider()

#Side bar button to access documentation
with st.sidebar:
    st.link_button('Documentation','https://github.com/ad-44/LCOS_Calculator/blob/main/README.md')

#Input interface
col1, col2, col3 = st.columns([0.4,0.4,0.2], gap="large")

with col2:
    st.subheader("Inputs")

with st.container(border=True):
    col4, col5, col6 = st.columns(3, gap="large")
    
    #Inputs
    with col4: 
        st.subheader('Storage system')
        power = st.number_input('Installed capacity (MW)',0.0,2000.0)
        capacity = st.number_input('Storage capacity (MWh)',0.0,2000.0)
        eff = st.number_input('Round Trip Efficiency (%)',0,100)
    with col5:
        st.subheader('Costs and lifetime')
        capexmw = st.number_input('Capital expenditures (k€/MW)',0.0,2000.0)
        opexmw = st.number_input('Operational expenditures (k€/MW)',0.0,2000.0)
        life = st.number_input('Lifetime',0,100)
        discount = st.number_input('Discount Rate (%)',0.0,100.0,step=0.5)
    with col6:
        st.subheader('Model parameters')
        spot_year = st.selectbox(
            'Year to simulate',
            ('2014','2015','2016','2017','2018','2019','2020','2021','2022','2023'),
            index=None,
            placeholder='Select a year...'
            )
        model = st.selectbox(
            'Optimisation time window',
            ('Year','Month','Week','2 days','1 day'),
            index=None,
            placeholder='Select a model...'
            )   
    
    #Launch calculator button
    launch = st.button('Launch calculator')
    input_list = [power,capacity,eff,capexmw,opexmw,life,discount,spot_year,model]
    zero_list = [power,capacity,eff,life,discount]
    
if launch :

    #Error messages
    for item in input_list:
        if item == None:
            st.error('A parameter is missing, please check your inputs.')
            st.stop()
            
    for item in zero_list:
        if item == 0:
            st.error("Installed capacity, storage capacity, round-trip efficiency, lifetime and discount rate can't be equal to 0")
            st.stop()
            
    with st.spinner("Calculation in progress...", show_time = True):
    
        #Parameters
        stock_begin = capacity/3
        results = pd.DataFrame()
        
        if spot_year != None:
            spot_data = rawprices[spot_year]
            index_hours = pd.date_range(spot_year+"-01-01 00:00",spot_year+"-12-31 23:00",freq='h').tolist()
        else:
            pass
        
        #Time window parameters
        if model == "Year":
            periods = 1
            num_segments = len(spot_data)
            
        elif model == "Week":
            periods = 53
            num_segments = 168
            
        elif model == "1 day":
            periods = 366
            num_segments = 24 
            
        elif model == "2 days":
            periods = 183
            num_segments = 48
            
        elif model == "Month":
            periods = 12
            num_segments = 732
        
        #model 
        for period in range(periods):
            if period == periods-1 :
                segments = list(range(period*num_segments,len(spot_data)))
            else:
                segments = list(range(period*num_segments, (period + 1) * num_segments))
        
            m = pyo.ConcreteModel('LCOS optimisation')
        
            #Set and variables
            m.hours = pyo.Set(initialize=segments)
        
            #Variables 
            m.ch = pyo.Var(m.hours, domain = pyo.NonNegativeReals, bounds=(0, power))
            m.dis = pyo.Var(m.hours,domain = pyo.NonNegativeReals, bounds=(0, power))
            m.stock = pyo.Var(m.hours,domain = pyo.NonNegativeReals, bounds=(0, capacity))
            m.revenu = pyo.Var(m.hours)
            m.chcost = pyo.Var(m.hours)
            m.profit = pyo.Var(m.hours)
            m.onch = pyo.Var(m.hours, domain=pyo.Binary)
            m.ondis = pyo.Var(m.hours, domain=pyo.Binary)
            
                #Stock following for loop optimisation
            m.stock[m.hours.first()] = stock_begin
            m.stock[m.hours.first()].fix()
        
            #Constraints
            def revenu_cst(m,spot_data):
                return [m.dis[i] * spot_data[i] == m.revenu[i] for i in m.hours]
        
            def chcost_cst(m,spot_data):
                return [m.ch[i] * spot_data[i] == m.chcost[i] for i in m.hours]
        
            def profit_cst(m):
                return [m.revenu[i] - m.chcost[i] == m.profit[i] for i in m.hours]
        
            def stockfollow_cst(m,eff,capacity):
                return [m.stock[i] == stock_begin + (m.ch[i]*(math.sqrt(eff/100))-(m.dis[i]/math.sqrt(eff/100))) if i == m.hours.first() else m.stock[i] == m.stock[i-1] +(m.ch[i]*math.sqrt(eff/100))-(m.dis[i]/math.sqrt(eff/100)) for i in m.hours]
            
            def stock1_cst(m):
                return [m.ch[i] <= 10000*m.onch[i] for i in m.hours]
        
            def stock2_cst(m):
                return [m.dis[i] <= 10000*m.onch[i] for i in m.hours]
        
            def stock3_cst(m):
                return [m.ondis[i] + m.onch[i] == 1 for i in m.hours]
        
            m.revenu_cst = pyo.ConstraintList(rule=revenu_cst(m, spot_data))
            m.chcost_cst = pyo.ConstraintList(rule=chcost_cst(m, spot_data))        
            m.profit_cst = pyo.ConstraintList(rule=profit_cst(m))
            m.stockfollow_cst = pyo.ConstraintList(rule=stockfollow_cst(m, eff, capacity))
            m.stock1_cst = pyo.ConstraintList(rule=stock1_cst(m))
            m.stock2_cst = pyo.ConstraintList(rule=stock2_cst(m))
            m.stock3_cst = pyo.ConstraintList(rule=stock3_cst(m))
        
            #Objectif and solve
            def objectiv_func(m):
                obj_results = sum(m.profit[i] for i in m.hours)
                return obj_results
        
            m.obj = pyo.Objective(rule=objectiv_func,sense=pyo.maximize)
        
            solver = pyo.SolverFactory('glpk')
            solver.solve(m)
            
                #Stock following for loop optimisation
            stock_begin = pyo.value(m.stock[m.hours.last()])
            
            #Results extraction
            for v in m.component_objects(pyo.Var,active=True):
                for index in v: 
                    results.at[index, v.name] = pyo.value(v[index])
        
        #indicators calculation
        crf = function.crf_func(discount, life)
        capex = function.capex_func(power, capexmw)
        opex = function.opex_func(power, opexmw)
        sumch = sum(results['ch'])
        sumdis = sum(results['dis'])
        sumchp = sum(results['chcost'])
        sumdisp = sum(results['revenu'])
        lcos = function.lcos_func(capex, crf, sumchp, opex, sumdis)
        lcoswc = function.lcoswc_func(capex, crf, opex, sumdis)
        profit = sum(results['profit'])
        
        #model parameters df
        index_mp = ['Installed capacity (MW)','Storage capacity (MWh)','Round trip efficiency (%)','Capital expenditures (€)',
        'Operational expenditure (€)','Lifetime', 'Discount rate (%)']
        data_mp = [power,capacity,eff,capex,opex,life,discount]
        model_parameters = pd.DataFrame(data_mp,index_mp, columns=['Values'])
        
        #results synthesis df
        index_synt = ['Volume of charged energy (MWh)', 'Volume of discharged energy (MWh)','Levelized cost of storage (€/MWh)', 'Levelized cost of storage without charging cost (€/MWh)', 'Revenue (€)', 'Charging cost (€)','Profit (€)']
        data_synt = [sumch,sumdis,lcos,lcoswc,sumdisp,sumchp,profit]
        synthesis = pd.DataFrame(data_synt,index_synt,columns=['Values'])
        
        #hourly results df
           
            #Correction between bissextile years and non-bissextile one
        bis_year = ['2014','2015','2017','2018','2019','2021','2022','2023']
        if spot_year in bis_year:
            results = results.iloc[:-24]
            
        col_results = ['Charged energy (MW)', 'Discharged energy (MW)','Stock (MWh)','Revenue (€)', 'Charging cost (€)']
        results = results.drop(['ondis','onch','profit'],axis=1)
        results.columns = col_results
        results.index = index_hours
        
        #data format
        results_formatted = results + 0
        synthesis = synthesis.style.format("{:,.1f}")
        results_formatted = results_formatted.style.format("{:,.1f}")
        model_parameters = model_parameters.style.format("{:,.1f}")
        
        #Ouput display
        col7, col8, col9 = st.columns([0.4,0.4,0.2], gap="large")
            
        with col8:
            st.subheader("Outputs")
        
        Data, Charts = st.tabs(['Data','Charts'])
        
        with Data:
            
            with st.container(border=False):
                
                col10, col11 = st.columns(2,gap="large")
                
                with col10: 
                    st.subheader("Model parameters")
                    st.dataframe(model_parameters,width=500)
                with col11: 
                    st.subheader('Results synthesis')
                    st.dataframe(synthesis, width=500)
                    
                st.subheader("Hourly results")
                st.dataframe(results_formatted, width=1500)
        
        #Chart display
        with Charts:
            fig_operation = make_subplots(specs=[[{'secondary_y':True}]])
    
            fig_operation.add_trace(
                go.Scatter(x=results.index,y=results['Stock (MWh)'],fill='tozeroy',name='Stock (MWh)'),
                secondary_y=True
                )
    
            fig_operation.add_trace(
                go.Bar(x=results.index,y=results['Charged energy (MW)'], name='Charged energy (MW)'),
                secondary_y=False
                )
    
            fig_operation.add_trace(
                go.Bar(x=results.index,y=results['Discharged energy (MW)'],name='Discharged energy (MW)'),
                secondary_y=False
                )
            
            fig_operation.update_layout(
                title_text="Hourly charged, discharged and stored energy",
                yaxis = dict(
                    title=dict(text='MW'),
                    side='left',
                    range=[0,power],
                    ),
                yaxis2 = dict(
                    title=dict(text='MWh'),
                    side='right',
                    range=[0,capacity],
                    ),
                )
            
            st.plotly_chart(fig_operation,selection_mode='points')
        
            fig_profit = make_subplots()
            
            fig_profit.add_trace(
                go.Scatter(x=results.index, y=(results['Revenue (€)'] - results['Charging cost (€)']), name='Profit (€)')
                )
            
            fig_profit.update_layout(
                title_text='Hourly revenues and cost of charging',
                yaxis = dict(
                    title=dict(text='€'),
                    ),
                )
            
            st.plotly_chart(fig_profit, selection_mode='points')
else: 
    pass
