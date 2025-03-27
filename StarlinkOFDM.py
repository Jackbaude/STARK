#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Starlink OFDM
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class StarlinkOFDM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Starlink OFDM", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Starlink OFDM")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "StarlinkOFDM")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 240000000
        self.center = center = 1145000

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0_4_0_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.1575e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_4_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_4_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_4_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_4_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_4_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_4_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_4_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_4_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_4_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_4_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_4_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_4_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_4_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_4_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_4_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_4_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_4_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_4_0_0_win)
        self.qtgui_freq_sink_x_0_4_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.1450e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_4_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_4_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_4_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_4_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_4_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_4_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_4_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_4_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_4_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_4_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_4_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_4_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_4_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_4_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_4_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_4_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_4_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_4_0_win)
        self.qtgui_freq_sink_x_0_4 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.1325e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_4.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_4.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_4.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_4.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_4.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_4.enable_grid(False)
        self.qtgui_freq_sink_x_0_4.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_4.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_4.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_4.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_4.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_4.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_4.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_4.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_4.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_4_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_4.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_4_win)
        self.qtgui_freq_sink_x_0_3 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.1200e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_3.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_3.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_3.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_3.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_3.enable_grid(False)
        self.qtgui_freq_sink_x_0_3.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_3.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_3.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_3.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_3.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_3.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_3.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_3.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_3_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_3.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_3_win)
        self.qtgui_freq_sink_x_0_2 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.1075e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_2.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_2.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_2.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_2.enable_grid(False)
        self.qtgui_freq_sink_x_0_2.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_2.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_2.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_2_win)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.0950e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.0825e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (1.0700e+10), #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/jakku/git/STARK/data/mutli-band-measurements.bin', True, 100, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_2, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_3, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_4, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_4_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_freq_sink_x_0_4_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "StarlinkOFDM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range((1.0700e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range((1.0825e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_1.set_frequency_range((1.0950e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_2.set_frequency_range((1.1075e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_3.set_frequency_range((1.1200e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_4.set_frequency_range((1.1325e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_4_0.set_frequency_range((1.1450e+10), self.samp_rate)
        self.qtgui_freq_sink_x_0_4_0_0.set_frequency_range((1.1575e+10), self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center, self.samp_rate)

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center, self.samp_rate)




def main(top_block_cls=StarlinkOFDM, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
