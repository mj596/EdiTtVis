class PrEDIctionClient:

    def __init__(self):
        self.client = None
        self.application = None
        self.count = 0
        self.weekday = None
        self.plot_type = None
        self.cut_time = None
        
    def set_client(self, client):
        self.client = client

    def clean(self):
        self.client = None
        self.application = None
        self.weekday = None
        self.plot_type = None
        self.cut_time = None
        
    def get_client(self):
        if self.client is None:
            self.client = 'none'
            
        return self.client

    def get_application(self):
        if self.application is None:
            self.application= 'none'

        return self.application

    def set_application(self, application):
        self.application = application
    
    def get_id(self):
        return self.get_client() + '_' + self.get_application()

    def set_count(self, count):
        self.count = count
    
    def get_count(self):
        return self.count

    def set_weekday(self, weekday):
        self.weekday = weekday

    def get_weekday(self):
        return self.weekday

    def set_plot_type(self, plot_type):
        self.plot_type = plot_type

    def get_plot_type(self):
        return self.plot_type

    def set_cut_time(self, cut_time):
        self.cut_time = cut_time

    def get_cut_time(self):
        return self.cut_time
