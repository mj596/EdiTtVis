from modules.PrEDIction import PrEDIctionStats
from modules.PrEDIction import PrEDIctionClient
from modules.PrEDIction import PrEDIctionPrinter
import datetime
import web
from modules.TimeUtils import TimeUtils
        
def prediction_create_image(client, application, plot_type, cut_time, group_type, weekday):
    print( 'Getting' )
    print( 'Client: ' + client )
    print( 'Application: ' + application )
    print( 'PlotType: ' + plot_type )
    print( 'CutTime: ' + cut_time )
    print( 'GroupType: ' + group_type )
    print( 'Weekday: ' + weekday )
    
class get_image:

    def __init__(self):
        pass
        
    def print_data(self, input):
        info = 'Client: ' + input.client + '\n' + 'Application: ' + input.application + '\n' + 'PlotType: ' + input.plot_type + '\n' + 'CutTime: ' + input.cut_time + '\n' + 'GroupType: ' + input.group_type + '\n' + 'Weekday: ' + input.weekday + '\n'

        return info
        
    def GET(self):
        
        input = web.input(plot_type = 'Grouped', weekday = 'All', group_type = '1D', cut_time = 'All', from_time = None, to_time = None)
        
        time = TimeUtils()

        if input.cut_time == 'All':
            from_time = None
            to_time = None
        else:
            input.cut_time == 'All'
            from_time = time.get_past(input.cut_time)
            to_time = time.get_now()
            print( 'FromTime: ' + str(from_time) )
            print( 'ToTime: ' + str(to_time) )
            
        stats = PrEDIctionStats()
        printer = PrEDIctionPrinter()
        client = PrEDIctionClient()

        client.set_client( str(input.client) )
        client.set_application(input.application)
        client.set_plot_type(input.plot_type)
        client.set_weekday(input.weekday)
        client.set_cut_time(input.cut_time)           
        
        print( self.print_data(input) )
        print('[' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '] ' + 'Working on ' + client.get_id())

        try:
            data = stats.get_client_data("accepted", client, from_date=from_time, to_date=to_time)
                
            pregrouped_data = stats.pregroup_data(data, input.group_type, input.cut_time)
            prefiltered_data = stats.prefilter_data_by_weekday(pregrouped_data, input.weekday)
            
            if input.plot_type == 'Grouped':
                grouped_data = stats.group_data(prefiltered_data, input.group_type, client)
                printer.add_data(grouped_data)
                printer.print_grouped()
            
            if input.plot_type == 'Folded':
                folded_data = stats.fold_data(prefiltered_data, input.group_type, client)
                printer.add_data(folded_data)            
                printer.print_folded()            

            if input.plot_type == 'Cumsum':
                cumsumed_data = stats.cumsum_folded_data(prefiltered_data, input.group_type)
                folded_data = stats.fold_data(cumsumed_data, input.group_type, client)
                printer.add_data(folded_data)            
                printer.print_folded()            
                
            printer.clean()
            client.clean()
            
            web.header("Content-Type", "images/png")
            web.header("Content-disposition", "filename=image.png")
        
            return open(printer.get_filename(),"rb").read()
            
        except Exception as e:
            web.header("Content-Type", "text/plain")
            return(str(e) + '\n' + self.print_data(input))
        
def main():

    urls = (
        '/image', 'get_image'
    )

    app = web.application(urls, globals())


    app.run()

if __name__ == '__main__':    
    main()    
