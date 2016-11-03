import numpy as np
import datetime
import pandas as pd
from modules.DBConnector import DBConnector
from . import PrEDIctionData
from ..TimeUtils import TimeUtils

class PrEDIction:
    
    def __init__(self):
        self.number_of_clients_limit = 5
        self.timeUtils = TimeUtils()
        
    def set_number_of_clients_limit(self, clients):
        self.number_of_clients_limit = clients
        
    def get_data(self, query):
        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'EDITT')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        return_data = np.array(data).transpose()[0].transpose()
        
        return return_data

    def get_clients(self, type):
        accepted_clients = '''select l1.edi_client_desc, l1.application, count(*) "count"
                              from editt.editt_level1 l1
                              join editt.editt_level2 l2
                              on l2.id_lvl1 = l1.id
                              where l2.line_message_status = 'FULLY_ACCEPTED'
                              group by l1.edi_client_desc, l1.application
                              order by "count" desc'''

        if type == 'accepted':
            query = accepted_clients
        else:
            query = None

        print(query)
        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'EDITT')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        return_data = np.array(data[:self.number_of_clients_limit])
        print('test')
        print(return_data[0])
        
        return return_data
    
    def filter_weekends(self, data):
        returnData = []

        for item in data:
            if( self.timeUtils.getWeekday(item) != 'Saturday' and self.timeUtils.getWeekday(item) != 'Sunday' ):
                returnData.append(item)

        return returnData

    def filter_weekday(self, data, weekday):
        returnData = []

        for item in data:
            if( self.timeUtils.getWeekday(item) == weekday ):
                returnData.append(item)

        return returnData

    def pregroup_data(self, data, type, cut_time):
        data_frame = pd.DataFrame( data=np.ones(len(data)), index=data, columns = ['amount'] )
        if cut_time == 'All':
            cut_data_frame = data_frame
        else:
            start_time = data_frame.index.max()-pd.Timedelta(cut_time)
            cut_data_frame = data_frame[data_frame.index > start_time]
            
        grouped = cut_data_frame.groupby( pd.TimeGrouper(freq=type) ).count()
        return grouped
    
    def prefilter_data_by_weekday(self, data, weekday):
        if weekday == 'All':
            filtered = data
        elif weekday == 'NoWeekends':
            no_weekends_array = np.bool_( (np.sum([[data.index.weekday == 0], [data.index.weekday == 1], [data.index.weekday == 2], [data.index.weekday == 3], [data.index.weekday == 4]], axis=0))[0] )
            filtered = data[no_weekends_array]            
        else:
            weekday_number = self.timeUtils.get_weekday_number(weekday)
            filtered = data[data.index.weekday == weekday_number]

        return filtered
    
    def group_data(self, data, type, client):
        df = pd.DataFrame( data )
        
        df.name = client.get_desc() + '_' + client.get_document_type() + '_' + type + '_' + client.get_weekday() + '_' + str(data.index.min()) + '_' + str(data.index.max()) + '_' + str(client.get_plot_type()) + '_' + str(client.get_cut_time())

        grouped_data = { 'delta': [] }
        grouped_data['delta'].append(pd.Timedelta(type))
        df['delta'] = pd.Series(grouped_data['delta'], index=df.index)
        
        return df

    def cumsum_folded_data(self, data):        
        cumsum_data = data.groupby( pd.TimeGrouper(freq='D'))
        return pd.DataFrame( data=cumsum_data['amount'].cumsum().values, index=data.index, columns = ['amount'] )

    def fold_data(self, data, type, client):
        df = pd.DataFrame(index=pd.date_range("00:00", "23:59", freq=type).time)
        df.name = client.get_desc() + '_' + client.get_document_type() + '_' + type + '_' + client.get_weekday() + '_' + str(data.index.min()) + '_' + str(data.index.max()) + '_' + str(client.get_plot_type()) + '_' + str(client.get_cut_time())
        
        folded_data = { 'delta': [],
                        'mean': [],
                        'std': [],
                        'min': [],
                        'max': [],
                        'values': [] }
        
        for i in range(len(df.index.values)):
            start = df.index.values[i]
                       
            if i == len(df.index.values)-1:
                end = df.index.values[0]
            else:
                end = df.index.values[i+1]

            selected = data.between_time(start, end, include_start=True, include_end=False).values.transpose()[0]
            folded_data['delta'].append(pd.Timedelta(type))
            folded_data['mean'].append(selected.mean())
            folded_data['std'].append(selected.std())
            folded_data['min'].append(selected.min())
            folded_data['max'].append(selected.max())
            folded_data['values'].append(selected)

        df['delta'] = pd.Series(folded_data['delta'], index=df.index)            
        df['mean'] = pd.Series(folded_data['mean'], index=df.index)
        df['std'] = pd.Series(folded_data['std'], index=df.index)
        df['min'] = pd.Series(folded_data['min'], index=df.index)
        df['max'] = pd.Series(folded_data['max'], index=df.index)
        df['values'] = pd.Series(folded_data['values'], index=df.index)        
        
        return df
