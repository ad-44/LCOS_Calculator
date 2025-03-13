# Levelized cost of storage calculator

Calculator developed under python using streamlit to ease the calculation of the levelized cost of storage indicator.

![Calculator](https://github.com/ad-44/LCOS_Calculator/blob/main/screenshots/mainpage.png?raw=true)

Access Link : https://lcoscalculator-crdftwyzdozbj8e9gkjgej.streamlit.app/

## Preamble

The levelized cost of storage (LCOS) is an indicator used in the financial evaluation of energy storage technology. Based on the levelized cost of energy (LCOE), it defines the cost of energy as the profitability threshold of a technology express as a cost of generation such as : 

```math
LCOS = \frac{\sum_{n=1}^{N}[I_n + FOM_n + C^p_n] * (1+r)^{-n}}{\sum_{n=1}^{N}E^{gen}_n*(1+r)^{-n}} + \frac{\sum_{n=1}^{T}AC_n*(1+r)^{-n}}{\sum_{n=1}^{N}E^{gen}_n*(1+r)^{-n}} \; , \qquad \forall \; n \in N
```
```math
with \qquad C^p_n = \sum_{h=1}^{H}(P_{h}*E^{ch}_{h}), \qquad \forall \; n \in N
```

The levelized cost of storage is primarily influenced by the volume of discharged energy, which is available only if energy has been charged beforehand.
To optimize the indicator value, the storage operator must adjust charge and discharge cycles based on market prices, as they rely on the spot market to purchase energy. 

In order to give an approximate LCOS value, this calculator optimizes the yearly operation of a storage plant in order to maximize its profit from arbitrage on the spot market. The optimization admit a perfect forecast of market prices. Historical french spot market data are provided hourly from 2014 to 2023.

### Nomenclature

|Factors|Definition|
|:---:|:---|
|$E^{gen}$|Generated volume of energy|
|$E^{ch}$ | Charged volume of energy|
|$I$ |Investment cost|
|$FOM$| Fixed operation and maintenance costs| 
|$AC$| Adjacent costs (decommissioning, recycling...)|
|$r$ | Discount rate|
|$N$ | Storage system operating year| 
|$n$ | Current year |
|$T$ | Storage system years of exploitation|
|$P$ | SPOT Market price|
|$H$ | Number of hours in a year|
|$h$ | Current hour |
|$C^p$ | Cost of purchasing electricity|
|$LCOS$ | Levelized cost of storage|
        
## Usage
### Inputs

<img align="left" src="https://github.com/ad-44/LCOS_Calculator/blob/main/screenshots/Inputs.png?raw=true" height="800" /> &nbsp;

All user inputs are done in the sidebar of the calculator. The reset button will reset all inputs value to 0.

**Model parameters:**
- *Year to simulate* : spot market year use to optimize the storage operation
- *Optimization time window* : time window use to optimize the storage operation. If "week" is selected, the calculator will optimize the profit of the storage system over a single week, then over the next one... Until the end of the year.
- *Preload a storage profile (optional)* : load all parameters for a define storage profile.

**Storage system:**
- *Installed capacity* : nominal power of the storage system in MW
- *Storage capacity* : maximum energy that the storage system can hold in MWh
- *Round-trip efficiency* : ratio of energy put in to energy retrieved from storage in %

**Costs and lifetime:**
- *Capital expenditure* : expenses inherent to the storage acquisition in k€/MW
- *Operational expenditures* : expenses inherent to the storage operation in k€/MW
- *Lifetime* : duration of the storage system exploitation
- *Discount rate* : interest rate use to calculate the LCOS

Calculation will be launched after clicking the "Launch calculator" button on left of the main page title. All inputs need to be filled in by the user before starting the calculator.

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

### Outputs

The outputs are separated between two tabs. The data one, with all numerical data displayed in several tables.

![Data](https://github.com/ad-44/LCOS_Calculator/blob/main/screenshots/Outputs_data.png?raw=true)

The charts one, including several graphical representations of the results.

![Charts](https://github.com/ad-44/LCOS_Calculator/blob/main/screenshots/Outputs_charts.png?raw=true)

Charts can be zoomed in with the mouse by selecting a range directly in the chart: 

[streamlit_chart_data_navigation.webm](https://github.com/user-attachments/assets/848180a5-dbcf-4b4e-87f1-b8170c064a64)
