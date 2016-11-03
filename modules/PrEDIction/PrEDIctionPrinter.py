import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import os
import pandas as pd
from matplotlib.font_manager import FontProperties

class PrEDIctionPrinter:
    
    weekdayLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    font = FontProperties()
    font.set_family('sans-serif')
    font.set_variant('small-caps')
    font.set_size(8)
    font.set_family('monospace')
    
    def __init__(self):
        self.data = None
        self.filename = 'test_filename'
        self.folder = 'printer_out/test_folder'
        
    def add_data(self, tsdc):
        self.data = tsdc

    def clean(self):
        self.data = None

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename
        
    def set_folder(self, folder):
        self.folder = 'printer_out/' + folder

    def print_folded(self):        
        plt.clf()
        with plt.style.context(('ggplot')):

            client_desc = (self.data.name.split('_')[0]).replace('\'','')
            client_document_type = (self.data.name.split('_')[1]).replace('\'','')
            client_type = self.data.name.split('_')[2]
            client_weekday = self.data.name.split('_')[3]
            time_range_start = self.data.name.split('_')[4]
            time_range_end = self.data.name.split('_')[5]            
            plot_type = self.data.name.split('_')[6]
            cut_time = self.data.name.split('_')[7]
            
            time = []

            for i in self.data.index:
                if 'D' in client_type:
                    time.append( i )
                else:
                    time.append( datetime.datetime.combine(datetime.datetime.now().date(), i) )

            if 'D' in client_type:
                time_error = (0.5*int(self.data['delta'].values[0])/(1e9*86400)) * np.ones(len(self.data['delta'].values))
            else:
                time_error = datetime.timedelta( seconds=0.5*int(self.data['delta'].values[0])/1e9 ) * np.ones(len(self.data['delta'].values))             
            
            plt.errorbar(time, self.data['mean'], xerr=time_error, yerr=self.data['std'], fmt='b.', capsize=0, label='mean +- std deviation')
            plt.errorbar(time, self.data['min'], xerr=time_error, fmt='r.', markersize=0, capsize=0, label='min/max')
            plt.errorbar(time, self.data['max'], xerr=time_error, fmt='r.', markersize=0, capsize=0, label=None)
            
            for key in self.data.index:
                if 'D' in client_type:
                    time = [key for i in self.data['values'][key]]
                else:
                    time = [datetime.datetime.combine(datetime.datetime.now().date(), key) for i in self.data['values'][key]]
                plt.plot(time, self.data['values'][key], 'go', alpha=0.1)
            
            ax = plt.gca()

            if 'D' in client_type:
                text_location = {'x': 0.7, 'y': 0.8}
            else:
                text_location = {'x': 0.05, 'y': 0.7}
                
            plt.text(text_location['x'], text_location['y'], 'Client: ' + client_desc + '\n' + 'Application: ' + client_document_type + '\n' + 'Weekday: ' + client_weekday + '\n' + 'Grouped by: ' + client_type + '\n' + 'From: ' + time_range_start + '\n' + 'To: ' + time_range_end + '\n' + 'PlotType: ' + plot_type + '\n' + 'TimeCut: ' + cut_time, fontproperties=self.font, transform=ax.transAxes)
      
            plt.ylim([-1, 1.1*self.data['max'].max()])

            plt.legend(loc=2, prop=self.font, fancybox=None, frameon=None)

            plt.xticks(rotation=20, fontproperties=self.font)
            plt.yticks(fontproperties=self.font)
            plt.ylabel('Number of EDI transmissions', fontproperties=self.font)

            self.folder = 'printer_out' + '/' + plot_type + '/' + 'Client' + client_desc + 'Application' + client_document_type
            self.filename = self.folder + '/' + 'Client' + client_desc + 'Application' + client_document_type + 'Weekday' + client_weekday + 'GroupedBy' + client_type + 'PlotType' + plot_type + 'CutTime' + cut_time + '.png'
        
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            
        plt.savefig(self.filename, dpi=100)
        
    def print_grouped(self):
        plt.clf()

        time_error = datetime.timedelta( seconds=int(self.data['delta'].values[0])/1e9 ) * np.ones(len(self.data['delta'].values))
        histogram_width_in_days = time_error[0].total_seconds()/(3600*24)
        
        with plt.style.context(('ggplot')):
            plt.bar(self.data.index, self.data['amount'], width=histogram_width_in_days, alpha=0.5)
            plt.plot()
            
            client_desc = (self.data.name.split('_')[0]).replace('\'','')
            client_document_type = (self.data.name.split('_')[1]).replace('\'','')
            client_type = self.data.name.split('_')[2]
            client_weekday = self.data.name.split('_')[3]
            time_range_start = self.data.name.split('_')[4]
            time_range_end = self.data.name.split('_')[5]            
            plot_type = self.data.name.split('_')[6]
            cut_time = self.data.name.split('_')[7]
            
            self.folder = 'printer_out' + '/' + plot_type + '/' + 'Client' + client_desc + 'Application' + client_document_type
            self.filename = self.folder + '/' + 'Client' + client_desc + 'Application' + client_document_type + 'Weekday' + client_weekday + 'GroupedBy' + client_type + 'PlotType' + plot_type + 'CutTime' + cut_time + '.png'
            
            ax = plt.gca()
            
            plt.text(0.05, 0.8, 'Client: ' + client_desc + '\n' + 'Application: ' + client_document_type + '\n' + 'Weekday: ' + client_weekday + '\n' + 'Grouped by: ' + client_type + '\n' + 'From: ' + time_range_start + '\n' + 'To: ' + time_range_end + '\n' + 'PlotType: ' + plot_type + '\n' + 'TimeCut: ' + cut_time, fontproperties=self.font, transform=ax.transAxes)
            
            plt.xticks(rotation=20, fontproperties=self.font)
            plt.yticks(fontproperties=self.font)            
            plt.ylabel('Number of EDI transmissions', fontproperties=self.font)            
            
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)
                
            plt.savefig(self.filename, dpi=100)
