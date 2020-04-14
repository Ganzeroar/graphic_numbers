import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LesgaftGraph')
        self.desktop_size = QApplication.desktop().availableGeometry()
        self.desktop_width = self.desktop_size.width()
        self.desktop_height = self.desktop_size.height()
        self.setFixedSize(self.desktop_width, self.desktop_height)

        self.all_buttons = []
        self.all_buttons_info = []
        self.pressed_buttons = []

        self.main_vbox = QtWidgets.QVBoxLayout()
        self.upper_hbox = QtWidgets.QHBoxLayout()
        self.middle_hbox = QtWidgets.QHBoxLayout()

        font_obj_for_label = QtGui.QFont('Segoe UI', pointSize=26)
        
        self.coordinates_label = QtWidgets.QLabel("Координаты")
        self.coordinates_label.setFont(font_obj_for_label)
        self.upper_hbox.addWidget(self.coordinates_label)

        self.upper_hbox.addStretch(1)

        self.x_label = QtWidgets.QLabel("X")
        self.x_label.setFont(font_obj_for_label)
        self.upper_hbox.addWidget(self.x_label, alignment=QtCore.Qt.AlignRight)
        self.x_line_edit = QtWidgets.QLineEdit()
        self.x_line_edit.setFixedSize(50, 50)
        self.upper_hbox.addWidget(self.x_line_edit)


        self.y_label = QtWidgets.QLabel("Y")
        self.y_label.setFont(font_obj_for_label)
        self.upper_hbox.addWidget(self.y_label, alignment=QtCore.Qt.AlignRight)
        self.y_line_edit = QtWidgets.QLineEdit()
        self.y_line_edit.setFixedSize(50, 50)
        self.upper_hbox.addWidget(self.y_line_edit)

        self.create_lines_on_graph_btn = QtWidgets.QPushButton('Построить')
        self.create_lines_on_graph_btn.clicked.connect(self.create_lines_on_graph)
        self.create_lines_on_graph_btn.setStyleSheet("font-size:30px;")
        self.create_lines_on_graph_btn.setFixedSize(170, 60)
        self.upper_hbox.addWidget(self.create_lines_on_graph_btn)

        self.x_line_edit.setText('10')
        self.y_line_edit.setText('10')

        self.upper_hbox.addStretch(1)

        self.line_spacing_label = QtWidgets.QLabel("Расстояние между \nлиниями в пикселях")
        self.line_spacing_label.setFont(font_obj_for_label)
        self.upper_hbox.addWidget(self.line_spacing_label)

        self.x_label_line_spacing = QtWidgets.QLabel("X")
        self.x_label_line_spacing.setFont(font_obj_for_label)
        self.upper_hbox.addWidget(self.x_label_line_spacing, alignment=QtCore.Qt.AlignRight)
        self.x_line_spacing_edit = QtWidgets.QLineEdit()
        self.x_line_spacing_edit.setFixedSize(50, 50)
        self.upper_hbox.addWidget(self.x_line_spacing_edit)

        self.y_label_line_spacing = QtWidgets.QLabel("Y")
        self.y_label_line_spacing.setFont(font_obj_for_label)
        self.upper_hbox.addWidget(self.y_label_line_spacing, alignment=QtCore.Qt.AlignRight)
        self.y_line_spacing_edit = QtWidgets.QLineEdit()
        self.y_line_spacing_edit.setFixedSize(50, 50)
        self.upper_hbox.addWidget(self.y_line_spacing_edit)

        self.x_line_spacing_edit.setText('20')
        self.y_line_spacing_edit.setText('20')

        self.upper_hbox.addStretch(1)


        self.settings_checkbox = QtWidgets.QCheckBox()
        #self.settings_checkbox.setChecked(True)
        self.settings_checkbox.setStyleSheet("QCheckBox::indicator { width: 27px; height: 27px;}")
        self.upper_hbox.addWidget(self.settings_checkbox)

        self.settings_label = QtWidgets.QLabel("Выбрать несколько точек \nв одном вертикальном ряду")
        self.settings_label.setFont(QtGui.QFont('Segoe UI', pointSize=17))
        self.upper_hbox.addWidget(self.settings_label, alignment=QtCore.Qt.AlignRight)

        self.upper_hbox.addStretch(1)

        self.clear_graph = QtWidgets.QPushButton('Очистить')
        self.clear_graph.setStyleSheet("font-size:30px;")
        self.clear_graph.setFixedSize(170, 60)
        self.upper_hbox.addWidget(self.clear_graph) 

        self.main_vbox.addLayout(self.upper_hbox)

        self.coordinates_labels = QtWidgets.QLabel("    №           X           Y           (X,Y)")
        self.main_vbox.addWidget(self.coordinates_labels, alignment=QtCore.Qt.AlignTop)


        self.number_info = QtWidgets.QTextEdit()
        self.number_info.setFixedSize(45, 900)
        self.middle_hbox.addWidget(self.number_info, alignment=QtCore.Qt.AlignTop)

        self.x_info = QtWidgets.QTextEdit()
        self.x_info.setFixedSize(45, 900)
        self.middle_hbox.addWidget(self.x_info, alignment=QtCore.Qt.AlignTop)

        self.y_info = QtWidgets.QTextEdit()
        self.y_info.setFixedSize(45, 900)
        self.middle_hbox.addWidget(self.y_info, alignment=QtCore.Qt.AlignTop)

        self.xy_info = QtWidgets.QTextEdit()
        self.xy_info.setFixedSize(55, 900)
        self.middle_hbox.addWidget(self.xy_info, alignment=QtCore.Qt.AlignTop)


        self.graph_window = QtWidgets.QWidget(parent=self)
        self.graph_window.setFixedSize(1700, 900)

        self.graphics_scence = QtWidgets.QGraphicsScene(0, 0, 1700, 900)
        self.line_x = self.graphics_scence.addLine(50, 850, 1650, 850)
        self.line_y = self.graphics_scence.addLine(50, 850, 50, 50)

        self.view = QtWidgets.QGraphicsView(self.graphics_scence)

        self.graph_box = QtWidgets.QVBoxLayout()
        self.graph_box.addWidget(self.view)

        self.graph_window.setLayout(self.graph_box)

        self.middle_hbox.addWidget(self.graph_window, alignment=QtCore.Qt.AlignJustify)

        self.main_vbox.addLayout(self.middle_hbox, stretch=1)
        self.main_vbox.addStretch(1)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_vbox)
        self.setCentralWidget(self.main_widget)

    def create_lines_on_graph(self):

        if self.x_line_edit.text() == '':
            print('выбросиь диалоговое окно')
            return
        elif self.y_line_edit.text() == '':
            print('выбросиь диалоговое окно')
            return
        self.number_of_x_lines = int(self.x_line_edit.text())
        self.number_of_y_lines = int(self.y_line_edit.text())

        self.x_line_spacing = int(self.x_line_spacing_edit.text())
        self.y_line_spacing = int(self.y_line_spacing_edit.text())

        self.x_lines_arr = []
        self.y_lines_arr = []

        for number in range(1, self.number_of_x_lines + 1):
            x_coor = 50 + self.x_line_spacing * number
            first_y = 850
            second_y = 50
            self.x_arr_line = self.graphics_scence.addLine(x_coor, first_y, x_coor, second_y)
            self.x_lines_arr.append(self.x_arr_line)

        for number in range(1, self.number_of_y_lines + 1):
            y_coor = 850 - self.y_line_spacing * number
            first_x = 50
            second_x = 1650
            self.y_arr_line = self.graphics_scence.addLine(first_x, y_coor, second_x, y_coor)
            self.y_lines_arr.append(self.y_arr_line)
        
        serial_number = 0
        for x_graph_coor in range(self.number_of_x_lines + 1):
            x_pixel_coor = (50 + self.x_line_spacing * x_graph_coor) - 8
            for y_graph_coor in range(self.number_of_y_lines + 1):
                serial_number += 1
                y_pixel_coor = (850 - self.y_line_spacing * y_graph_coor) - 8
                self.btn = QtWidgets.QPushButton('')
                self.btn.setFixedSize(16, 16)
                self.btn.move(x_pixel_coor, y_pixel_coor)
                self.btn_info = {
                    'btn_obj' : self.btn,
                    'serial_number' : serial_number,
                    'x_pixel_coor' : x_pixel_coor,
                    'y_pixel_coor' : y_pixel_coor,
                    'x_graph_coor' : x_graph_coor,
                    'y_graph_coor' : y_graph_coor,
                }
                self.btn.clicked.connect(
                    lambda checked, btn_info_1=self.btn_info: self.create_line_between_btns_on_graph(btn_info_1))
                self.all_buttons.append(self.btn)
                self.all_buttons_info.append(self.btn_info)
                self.graphics_scence.addWidget(self.btn)

    def create_line_between_btns_on_graph(self, pressed_btn_info):
        append_inf_to_table = False
        if len(self.pressed_buttons) == 0:
            if pressed_btn_info['x_graph_coor'] == 0 or pressed_btn_info['y_graph_coor'] == 0:
                pressed_btn_info['btn_obj'].setStyleSheet("background-color: red")
                btn_info = {'serial_number':0, 'btn_info':pressed_btn_info}
                self.pressed_buttons.append([btn_info, None])
                append_inf_to_table = True
            else:
                pressed_btn_info['btn_obj'].setStyleSheet("background-color: red")
                x_coor = pressed_btn_info['x_pixel_coor'] + 8
                y_coor = pressed_btn_info['y_pixel_coor'] + 8
                line_obj = self.graphics_scence.addLine(50, 850, x_coor, y_coor)
                btn_info = {'serial_number':0, 'btn_info':pressed_btn_info, 'line_obj':line_obj}
                self.pressed_buttons.append([btn_info, None])
                append_inf_to_table = True
        else:
            if self.settings_checkbox.isChecked() == True:
                pressed_btn_info['btn_obj'].setStyleSheet("background-color: red")
                pressed_before_btn_x_coor = self.pressed_buttons[-1][0]['btn_info']['x_pixel_coor'] + 8
                pressed_before_btn_y_coor = self.pressed_buttons[-1][0]['btn_info']['y_pixel_coor'] + 8
                line_obj = self.graphics_scence.addLine(pressed_before_btn_x_coor, pressed_before_btn_y_coor, pressed_btn_info['x_pixel_coor']+8, pressed_btn_info['y_pixel_coor']+8)
                
                serial_num_of_pressed_btn = self.pressed_buttons[-1][0]['serial_number'] + 1
                btn_info = {'serial_number':serial_num_of_pressed_btn, 'btn_info':pressed_btn_info, 'line_obj':line_obj}
                self.pressed_buttons.append([btn_info, None])
                append_inf_to_table = True

            elif self.settings_checkbox.isChecked() == False:
                repeated_buttons = False
                for obj in self.pressed_buttons:
                    if obj[0]['btn_info']['x_graph_coor'] == pressed_btn_info['x_graph_coor']:
                        repeated_buttons = True
                if repeated_buttons:
                    if pressed_btn_info['x_graph_coor'] == 0 or pressed_btn_info['y_graph_coor'] == 0:
                        last_pressed_btn_x = self.pressed_buttons[-1][0]['btn_info']['x_graph_coor']
                        last_pressed_btn_y = self.pressed_buttons[-1][0]['btn_info']['y_graph_coor']
                        if last_pressed_btn_x == 0 or last_pressed_btn_y == 0:
                            self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: white")
                            self.pressed_buttons[-1][0]['btn_info'] = pressed_btn_info
                            self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: red")
                            number_info_text = self.number_info.toPlainText().split('\n')
                            number_info_text.pop()
                            x_info_text = self.x_info.toPlainText().split('\n')
                            x_info_text.pop()
                            y_info_text = self.y_info.toPlainText().split('\n')
                            y_info_text.pop()
                            xy_info_text = self.xy_info.toPlainText().split('\n')
                            xy_info_text.pop()
                            self.number_info.clear()
                            for x in number_info_text:
                                self.number_info.append(x)
                            self.x_info.clear()
                            for x in x_info_text:
                                self.x_info.append(x)
                            self.y_info.clear()
                            for x in y_info_text:
                                self.y_info.append(x)
                            self.xy_info.clear()
                            for x in xy_info_text:
                                self.xy_info.append(x)
                            append_inf_to_table = True
                        elif self.pressed_buttons[-1][0]['btn_info']['x_graph_coor'] == pressed_btn_info['x_graph_coor']:
                            self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: white")
                            self.graphics_scence.removeItem(self.pressed_buttons[-1][0]['line_obj'])
                            last_btn_x = self.pressed_buttons[-2][0]['btn_info']['x_pixel_coor'] + 8
                            last_btn_y = self.pressed_buttons[-2][0]['btn_info']['y_pixel_coor'] + 8
                            line_obj = self.graphics_scence.addLine(last_btn_x, last_btn_y, pressed_btn_info['x_pixel_coor']+8, pressed_btn_info['y_pixel_coor']+8)
                            self.pressed_buttons[-1][0]['btn_info'] = pressed_btn_info
                            self.pressed_buttons[-1][0]['line_obj'] = line_obj
                            self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: red")
                            number_info_text = self.number_info.toPlainText().split('\n')
                            number_info_text.pop()
                            x_info_text = self.x_info.toPlainText().split('\n')
                            x_info_text.pop()
                            y_info_text = self.y_info.toPlainText().split('\n')
                            y_info_text.pop()
                            xy_info_text = self.xy_info.toPlainText().split('\n')
                            xy_info_text.pop()
                            self.number_info.clear()
                            for x in number_info_text:
                                self.number_info.append(x)
                            self.x_info.clear()
                            for x in x_info_text:
                                self.x_info.append(x)
                            self.y_info.clear()
                            for x in y_info_text:
                                self.y_info.append(x)
                            self.xy_info.clear()
                            for x in xy_info_text:
                                self.xy_info.append(x)
                            append_inf_to_table = True
                        
                    elif len(self.pressed_buttons) >= 2 and self.pressed_buttons[-1][0]['btn_info']['x_graph_coor'] == pressed_btn_info['x_graph_coor']:
                        self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: white")
                        self.graphics_scence.removeItem(self.pressed_buttons[-1][0]['line_obj'])
                        last_btn_x = self.pressed_buttons[-2][0]['btn_info']['x_pixel_coor'] + 8
                        last_btn_y = self.pressed_buttons[-2][0]['btn_info']['y_pixel_coor'] + 8
                        line_obj = self.graphics_scence.addLine(last_btn_x, last_btn_y, pressed_btn_info['x_pixel_coor']+8, pressed_btn_info['y_pixel_coor']+8)
                        self.pressed_buttons[-1][0]['btn_info'] = pressed_btn_info
                        self.pressed_buttons[-1][0]['line_obj'] = line_obj
                        self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: red")
                        number_info_text = self.number_info.toPlainText().split('\n')
                        number_info_text.pop()
                        x_info_text = self.x_info.toPlainText().split('\n')
                        x_info_text.pop()
                        y_info_text = self.y_info.toPlainText().split('\n')
                        y_info_text.pop()
                        xy_info_text = self.xy_info.toPlainText().split('\n')
                        xy_info_text.pop()
                        self.number_info.clear()
                        for x in number_info_text:
                            self.number_info.append(x)
                        self.x_info.clear()
                        for x in x_info_text:
                            self.x_info.append(x)
                        self.y_info.clear()
                        for x in y_info_text:
                            self.y_info.append(x)
                        self.xy_info.clear()
                        for x in xy_info_text:
                            self.xy_info.append(x)
                        append_inf_to_table = True
                        
                    elif len(self.pressed_buttons) == 1:
                        self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: white")
                        self.graphics_scence.removeItem(self.pressed_buttons[-1][0]['line_obj'])
                        line_obj = self.graphics_scence.addLine(50, 850, pressed_btn_info['x_pixel_coor']+8, pressed_btn_info['y_pixel_coor']+8)
                        self.pressed_buttons[-1][0]['btn_info'] = pressed_btn_info
                        self.pressed_buttons[-1][0]['line_obj'] = line_obj
                        self.pressed_buttons[-1][0]['btn_info']['btn_obj'].setStyleSheet("background-color: red")
                        number_info_text = self.number_info.toPlainText().split('\n').remove(self.number_info.toPlainText().split('\n')[-1])
                        x_info_text = self.x_info.toPlainText().split('\n').remove(self.x_info.toPlainText().split('\n')[-1])
                        y_info_text = self.y_info.toPlainText().split('\n').remove(self.y_info.toPlainText().split('\n')[-1])
                        xy_info_text = self.xy_info.toPlainText().split('\n').remove(self.xy_info.toPlainText().split('\n')[-1])
                        self.number_info.clear()
                        self.number_info.setText(number_info_text)
                        self.x_info.clear()
                        self.x_info.setText(x_info_text)
                        self.y_info.clear()
                        self.y_info.setText(y_info_text)
                        self.xy_info.clear()
                        self.xy_info.setText(xy_info_text)
                        append_inf_to_table = True
                else:
                    pressed_btn_info['btn_obj'].setStyleSheet("background-color: red")
                    pressed_before_btn_x_coor = self.pressed_buttons[-1][0]['btn_info']['x_pixel_coor'] + 8
                    pressed_before_btn_y_coor = self.pressed_buttons[-1][0]['btn_info']['y_pixel_coor'] + 8
                    line_obj = self.graphics_scence.addLine(pressed_before_btn_x_coor, pressed_before_btn_y_coor, pressed_btn_info['x_pixel_coor']+8, pressed_btn_info['y_pixel_coor']+8)
                    serial_num_of_pressed_btn = self.pressed_buttons[-1][0]['serial_number'] + 1
                    btn_info = {'serial_number':serial_num_of_pressed_btn, 'btn_info':pressed_btn_info, 'line_obj':line_obj}
                    self.pressed_buttons.append([btn_info])
                    append_inf_to_table = True
        if append_inf_to_table == True:
            serial_num_of_pressed_btn = self.pressed_buttons[-1][0]['serial_number'] + 1
            self.number_info.append(str(serial_num_of_pressed_btn))
            self.x_info.append(str(pressed_btn_info['x_graph_coor']))
            self.y_info.append(str(pressed_btn_info['y_graph_coor']))
            xy_info_text = str(pressed_btn_info['x_graph_coor'])+', '+str(pressed_btn_info['y_graph_coor'])
            self.xy_info.append(xy_info_text)

                            

        #переменная, отвечающая за присваивание кнопке номера 
        #self.var += 1
        # какой-то массив с другими кнопками, их номерами, координатами и пиксельными
        # координатами, что бы от него рисовать
        #self.btns_and_coors.append()


        


if __name__ == '__main__':

    # Добавить кнопку "скрыть кнопки"
    # Рисовать кноки на графике для возможности начать НЕ из точки 0:0
    # Добавить кнопку "Отменить последнюю точку"

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_()) 