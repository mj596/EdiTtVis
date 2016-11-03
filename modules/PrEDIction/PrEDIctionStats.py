import numpy as np
import datetime
import pandas as pd
from modules.DBConnector import DBConnector
from . import PrEDIctionData
from . import PrEDIctionClient
from ..TimeUtils import TimeUtils

class PrEDIctionStats:
    
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

        if len(data) == 0:
            raise Exception('No data returned for selected criteria')
        else:
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

        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'EDITT')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        
        clients_data = np.array(data[:self.number_of_clients_limit])
        clients = []
        for client_data in clients_data:
            client = PrEDIctionClient.PrEDIctionClient()
            client.set_client(client_data[0])
            client.set_application(client_data[1])
            client.set_count(client_data[2])
            clients.append(client)

        return clients

    def get_client_data(self, type, client, from_date=None, to_date=None):
        client_1 = '''select l1.transmission_date
                      from editt.editt_level1 l1
                      join editt.editt_level2 l2
                      on l2.id_lvl1 = l1.id
                      where l2.line_message_status = '''
        client_2 = ''' and nvl(l1.edi_client_desc, 'none') = '''
        client_3 = ''' and nvl(l1.application, 'none') = '''

        optional_dates = ""
        if from_date is not None:
            optional_dates += ' and l1.transmission_date >= TO_DATE(\'' + from_date + '\', \'YYYY-MM-DD HH24:MI:SS\') '

#select * from (select l1.ID_TRANSMISSION "[wire] Transmission ID", l1.TRANSMISSION_DATE "[wire] Transmission date", l1.PROTOCOL "[wire] Protocol", l1.MESSAGE_FORMAT "[wire] Message format", l1.MESSAGE_STATUS_DESC "[wire] Message status", l1.EDI_CLIENT_DESC "[wire] Client description", l1.AUTHENTICATION_ID "[wire] Authentication ID", l1.APPLICATION "[wire] Application ID", l1.DOCTYPE_NAME "[wire] Document type", l2.GROUP_REFERENCE "[biz] Group reference", l2.ORDER_REFERENCE "[biz] Order reference", l2.MAIN_REFERENCE "[biz] Main reference", l2.INTERNAL_NUMBER "[biz] Internal number", l2.ID "[biz] ID", l2.ERROR_CODE "[biz] Error code", l2.ERROR_DESC "[biz] Error", cl.EDI_CLIENT_SENDER "[client] Sender", cl.EDI_CLIENT_RECEIVER "[client] Receiver" from editt.editt_level1 l1 left join editt.editt_level2 l2 on l2.id_lvl1 = l1.id left join editt.editt_clients cl on cl.id_client = l2.line_edi_client_id  where l1.TRANSMISSION_DATE = TO_DATE('2016-11-03-11:12','YYYY-MM-DD-HH24:MI') order by l1.transmission_date desc) where rowNum <= 100 

#l1.transmission_date <= TO_DATE('2016-11-03 11:14:14', 'YYYY-MM-DD HH24:MI')
#l1.TRANSMISSION_DATE = TO_DATE('2016-11-03-11:12','YYYY-MM-DD-HH24:MI')

        if to_date is not None:
            optional_dates += ' and l1.transmission_date <= TO_DATE(\'' + to_date + '\', \'YYYY-MM-DD HH24:MI:SS\') '
            
        client_end = ''' order by l1.transmission_date desc'''

        if type == 'accepted':
            type = '\'FULLY_ACCEPTED\''
        elif type == 'rejected':
            type = '\'FULLY_REJECTED\''

        if from_date is not None or to_date is not None:
            client_query = client_1 + type + client_2 + '\'' + client.get_client() + '\'' + client_3 + '\'' + client.get_application() + '\'' + optional_dates + client_end
        else:
            client_query = client_1 + type + client_2 + '\'' + client.get_client() + '\'' + client_3 + '\'' + client.get_application() + '\'' + client_end

        print(client_query)
        try:
            data = self.get_data(client_query)
            return data            
        except Exception as e:
            raise Exception(e)
    
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
            print(cut_time + ' ' + str(start_time) + ' - ' + str(data_frame.index.max()))
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
        
        df.name = client.get_client() + '_' + client.get_application() + '_' + type + '_' + client.get_weekday() + '_' + str(data.index.min()) + '_' + str(data.index.max()) + '_' + str(client.get_plot_type()) + '_' + str(client.get_cut_time())

        grouped_data = { 'delta': [] }
        grouped_data['delta'].append(pd.Timedelta(type))
        df['delta'] = pd.Series(grouped_data['delta'], index=df.index)
        
        return df

    def cumsum_folded_data(self, data, type):
        if 'D' in type:
            cumsum_data = data.groupby( pd.TimeGrouper(freq='W'))
        if 'H' in type or 'Min' in type:
            cumsum_data = data.groupby( pd.TimeGrouper(freq='D'))
            
        return pd.DataFrame( data=cumsum_data['amount'].cumsum().values, index=data.index, columns = ['amount'] )

    def fold_data(self, data, type, client):
        if 'D' in type:
            df = pd.DataFrame(index=np.int_(np.linspace(0,6,7)))
        else:
            df = pd.DataFrame(index=pd.date_range("00:00", "23:59", freq=type).time)
            
        df.name = client.get_client() + '_' + client.get_application() + '_' + type + '_' + client.get_weekday() + '_' + str(data.index.min()) + '_' + str(data.index.max()) + '_' + str(client.get_plot_type()) + '_' + str(client.get_cut_time())

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

            if 'D' in type:
                selected = data[data.index.weekday == start].values.transpose()[0]
            else:
                selected = data.between_time(start, end, include_start=True, include_end=False).values.transpose()[0]

            if len(selected) > 0:
                folded_data['delta'].append(pd.Timedelta(type))
                folded_data['mean'].append(selected.mean())
                folded_data['std'].append(selected.std())
                folded_data['min'].append(selected.min())
                folded_data['max'].append(selected.max())
                folded_data['values'].append(selected)
            else:
                folded_data['delta'].append(pd.Timedelta(type))
                folded_data['mean'].append(0)
                folded_data['std'].append(0)
                folded_data['min'].append(0)
                folded_data['max'].append(0)
                folded_data['values'].append(selected)                
            
        df['delta'] = pd.Series(folded_data['delta'], index=df.index)            
        df['mean'] = pd.Series(folded_data['mean'], index=df.index)
        df['std'] = pd.Series(folded_data['std'], index=df.index)
        df['min'] = pd.Series(folded_data['min'], index=df.index)
        df['max'] = pd.Series(folded_data['max'], index=df.index)
        df['values'] = pd.Series(folded_data['values'], index=df.index)        
        
        return df
