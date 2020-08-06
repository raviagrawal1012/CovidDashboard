from django.shortcuts import render
import pandas as pd

# Create your views here.
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
    context={'totalCount':totalCount,'countryNames' : countryNames, 'barPlotVals' : barPlotVals}
    return render(request,'index.html',context)