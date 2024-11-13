class Utils:
    def __init__(self, app):
        self.app = app

    def update_year_selection(self, selected_year):
        """Update selected year and refresh the plot."""
        self.selected_year = int(selected_year)
        self.update_plot()

    def update_data_type(self, data_type):
        """Update selected data type and refresh the plot."""
        self.selected_data_type = data_type
        self.overlay_mode = False
        self.update_plot()

    def toggle_overlay_mode(self):
        """Toggle overlay mode to plot all data types."""
        self.overlay_mode = not self.overlay_mode
        self.update_plot()
