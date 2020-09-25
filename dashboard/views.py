from django.shortcuts import render
import pandas as pd


# Create your views here.
df3=pd.read_json("K:/mapchart.json")

def index(request):
    url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    confirmedGlobal=pd.read_csv(url,error_bad_lines=False)
    totalCount=confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData=barPlotData.reset_index()
    barPlotData.columns=['Country/Region','values']
    barPlotData=barPlotData.sort_values(by='values',ascending=False)
    barPlotVals=barPlotData['values'].values.tolist()
    countryNames=barPlotData['Country/Region'].values.tolist()
    dataForMap=mapDataCal(barPlotData,countryNames)
    context={'totalCount':totalCount,'countryNames' : countryNames, 'barPlotVals' : barPlotVals,'dataForMap' : dataForMap}
    return render(request,'index.html',context)

def mapDataCal(barPlotData,countryNames):
    dataForMap=[]
    for i in countryNames:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=barPlotData[barPlotData['Country/Region']==i]['values'].sum()
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    return dataForMap

def india(request):
    latestIndList,latestInd = IndTable()
    lst = indiaValue(latestInd)
    context = {'latestIndList' : latestIndList,'lst':lst}
    return render(request,'India.html',context)

def IndTable():
    india = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")
    latestInd = india[-36:]
    latestInd=latestInd.sort_values(by='Confirmed',ascending=False)
    latestIndList = latestInd.values.tolist()
    return latestIndList,latestInd

def indiaValue(latestInd):
    indiaList =latestInd['State'].values.tolist()
    indiaConList = latestInd['Confirmed'].values.tolist()
    indiaDict = {'in-py':'Puducherry','in-wb':'West Bengal','in-or':'Odisha',
            'in-br':'Bihar','in-sk':'Sikkim','in-ct':'Chhattisgarh',
            'in-tn':'Tamil Nadu','in-mp':'Madhya Pradesh',
            'in-2984':'Gujarat','in-ga':'Goa','in-nl':'Nagaland',
            'in-mn':'Manipur','in-ar':'Arunachal Pradesh',
            'in-mz':'Mizoram','in-tr':'Tripura',
            'in-3464':'Dadra and Nagar Haveli and Daman and Diu',
            'in-dl':'Delhi','in-hr':'Haryana','in-ch':'Chandigarh',
            'in-hp':'Himachal Pradesh','in-jk':'Jammu and Kashmir',
            'in-kl':'Kerala','in-ka':'Karnataka',
            'in-dn':'Dadra and Nagar Haveli and Daman and Diu',
            'in-mh':'Maharashtra','in-as':'Assam','in-ap':'Andhra Pradesh',
            'in-ml':'Meghalaya','in-pb':'Punjab','in-rj':'Rajasthan',
            'in-up':'Uttar Pradesh','in-ut':'Uttarakhand',
            'in-jh':'Jharkhand'}

    stateConDict = {indiaList[i] : indiaConList[i] for i in range(len(indiaList))}
    finalMapDict = {}
    for i in indiaDict:
        for j in stateConDict:
            if indiaDict[i] == j:
                finalMapDict[i] = stateConDict[j]

    lst = []
    for i in finalMapDict:
        lst.append([i,finalMapDict[i]])

    return lst




