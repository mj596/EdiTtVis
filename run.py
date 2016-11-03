from modules.PrEDIction import PrEDIctionStats
from modules.PrEDIction import PrEDIctionClient
from modules.PrEDIction import PrEDIctionPrinter
import datetime

def process_client(client, data, prediction, printer):

    cut_time_options = ['8D', '15D', 'All']
    
    grouping_weekday_options = ['All']    
    grouping_options = ['1D']

    folding_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'NoWeekends']
    folding_options = ['30Min', '1H', '2H', '1D']
    
    cumsum_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'NoWeekends']
    cumsum_options = ['30Min']

    for weekday in grouping_weekday_options:
        for option in grouping_options:
            for cut_time in cut_time_options:
                client.set_weekday(weekday)
                client.set_plot_type('Grouped')
                client.set_cut_time(cut_time)
                pregrouped_data = prediction.pregroup_data(data, option, cut_time)
                prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
                grouped_data = prediction.group_data(prefiltered_data, option, client)
                printer.add_data(grouped_data)
                printer.print_grouped()
                printer.clean()
            
    for weekday in folding_weekday_options:
        for option in folding_options:
            for cut_time in cut_time_options:            
                client.set_weekday(weekday)
                client.set_plot_type('Folded')
                client.set_cut_time(cut_time)                
                pregrouped_data = prediction.pregroup_data(data, option, cut_time)
                prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
                folded_data = prediction.fold_data(prefiltered_data, option, client)
                printer.add_data(folded_data)
                printer.print_folded()
                printer.clean()

    for weekday in cumsum_weekday_options:
        for option in cumsum_options:
            for cut_time in cut_time_options:
                client.set_weekday(weekday)
                client.set_plot_type('Cumsum')
                client.set_cut_time(cut_time)                
                pregrouped_data = prediction.pregroup_data(data, option, cut_time)
                prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
                cumsumed_data = prediction.cumsum_folded_data(prefiltered_data, option)
                folded_data = prediction.fold_data(cumsumed_data, option, client)
                printer.add_data(folded_data)
                printer.print_folded()
                printer.clean()
            
def main():    
    stats = PrEDIctionStats()
    printer = PrEDIctionPrinter()
    
    stats.set_number_of_clients_limit(10)    
    all_clients = stats.get_clients('accepted')
    
    for client in all_clients:
        print('[' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '] ' + 'Working on ' + client.get_id() + ' - got ' + str(client.get_count()) + ' messages' )
        data = stats.get_client_data("accepted", client)
        process_client(client, data, stats, printer)
        client.clean()
    
if __name__ == '__main__':
    main()    
