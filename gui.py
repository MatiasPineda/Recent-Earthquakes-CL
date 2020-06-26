import os
import requests
import sys
import urllib.request
import shutil
import atexit

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

API_key = os.environ['GOOGLE_API_KEY']

# TODO: get a better map style, google offers options
# TODO: style the app like: red dot in the middle, bigger map area, road names, etc
# TODO: Clean!


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Recent Earthquakes Chile')
        self.dir_name = 'temporal'
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.eq_data = self.earthquake_api_call()

        self.title_layout = QHBoxLayout()
        self.title_widget = QWidget()

        self.georef_label = QLabel("")
        self.refresh_button = QPushButton("Refresh")

        self.refresh_button.clicked.connect(self.start_refresh())

        self.title_layout.addWidget(self.georef_label)
        self.title_layout.addWidget(self.refresh_button)

        self.title_widget.setLayout(self.title_layout)

        self.photo = QLabel()

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.v_scroll_layout = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes

        self.button_group = QButtonGroup()
        self.button_group.buttonClicked[int].connect(self.on_button_clicked)

        self.generate_buttons()

        self.generate_scroll_area()

        self.first_image_start()

        self.main_layout.addWidget(self.title_widget)
        self.main_layout.addWidget(self.photo)
        self.main_layout.addWidget(self.scroll)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setGeometry(600, 100, 600, 700)

    def earthquake_api_call(self):
        """get info from the most recent earthquakes from api and work with it as json"""
        return requests.get('https://api.gael.cl/general/public/sismos').json()

    def first_image_start(self):
        self.download_map_image(0)
        self.photo.setPixmap(QPixmap('temporal/map-0.png'))
        self.reference_title(0)

    def start_refresh(self):
        self.delete_temporal_dir()
        self.eq_data = self.earthquake_api_call()
        self.button_group = QButtonGroup()
        self.button_group.buttonClicked[int].connect(self.on_button_clicked)
        self.generate_buttons()
        self.first_image_start()
        self.main_layout.addWidget(self.title_widget)
        self.main_layout.addWidget(self.photo)
        self.main_layout.addWidget(self.scroll)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        print("refreshed")

    def generate_buttons(self):
        """Generates 15 QPushButton objects, puts them in a QVBoxLayout for display and in QButtonGroup for indexing"""
        for index in range(15):
            data_dict = self.eq_data[index]
            btn_label = f'Referencia Geográfica: {data_dict["RefGeografica"]} \n' \
                        f'Fecha: {data_dict["Fecha"]} \tMagnitud: {data_dict["Magnitud"]}'
            button_object = QPushButton(btn_label)
            self.button_group.addButton(button_object, index)
            self.v_scroll_layout.addWidget(button_object)

    def generate_scroll_area(self):
        self.v_scroll_layout.setAlignment(Qt.AlignHCenter)
        self.widget.setLayout(self.v_scroll_layout)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

    def on_button_clicked(self, index):
        for button in self.button_group.buttons():
            if button is self.button_group.button(index):
                print(f"Showing image {index}")
                self.download_map_image(index)
                self.photo.setPixmap(QPixmap(f'temporal/map-{index}.png'))
                self.reference_title(index)

    def download_map_image(self, index):
        """Generate image from google maps static api using geo data from earthquake api"""
        earthquake_data = self.eq_data[index]
        lat = earthquake_data['Latitud']
        long = earthquake_data['Longitud']

        # Generate directory
        try:
            os.mkdir(self.dir_name)
            print("Directory ", self.dir_name, " Created ")
        except FileExistsError:
            print("Directory ", self.dir_name, " already exists")

        # Download image
        if not os.path.isfile(f'temporal/map-{index}.png'):
            gmaps_api_url = 'https://maps.googleapis.com/maps/api/staticmap?'
            url = f'{gmaps_api_url}center={lat},{long}&zoom=8&size=600x400&key={API_key}'
            urllib.request.urlretrieve(url, f'temporal/map-{index}.png')
            print("file created")
        else:
            print('file already exists')

    def reference_title(self, id):
        reference = self.eq_data[id]["RefGeografica"]
        self.georef_label.setText(reference)

    def delete_temporal_dir(self):
        shutil.rmtree(self.dir_name)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

atexit.register(window.delete_temporal_dir)

app.exec_()
