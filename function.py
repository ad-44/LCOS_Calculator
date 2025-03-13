def capex_func(power,capexmw): 
    capex = power * capexmw * 1000
    return capex

def opex_func(power,opexmw):
    opex = power * opexmw * 1000
    return opex

def crf_func(discount,life):
    crf = ((discount/100)*((1+(discount/100))**life))/(((1+(discount/100))**life)-1)
    return crf

def lcos_func(capex,crf,sumchp,opex,sumdis):
    lcos = ((capex*crf)+sumchp+opex)/sumdis
    return lcos

def lcoswc_func(capex,crf,opex,sumdis):
    lcoswc = ((capex*crf)+opex)/sumdis
    return lcoswc
    
def ltp(crf,profit):
    lifetime_profit = profit + (profit/crf)
    return lifetime_profit
