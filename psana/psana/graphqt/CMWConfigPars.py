
"""Class :py:class:`CMWConfigPars` is a QWidget for configuration parameters
==============================================================================

Usage ::
    # Test: python lcls2/psana/psana/graphqt/CMWConfigPars.py

    # Import
    from psana.graphqt.CMConfigParameters import

    # See test at the EOF

See:
  - :class:`CMWMain`
  - :class:`CMWConfig`
  - `on github <https://github.com/slac-lcls/lcls2>`_.

Created on 2017-04-05 by Mikhail Dubrovin
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QComboBox, QLineEdit
from psana.graphqt.CMConfigParameters import cp
from psana.graphqt.Styles import style


class CMWConfigPars(QWidget):
    """QWidget for managements of configuration parameters"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._name = 'CMWConfigPars'

        self.log_level_names = list(logging._levelToName.values())

        self.lab_host = QLabel('Host:')
        self.lab_port = QLabel('Port:')
        self.lab_level= QLabel('Log level:')
        self.lab_dir_ins= QLabel('Instrument dir:')
        self.lab_log_file = QLabel('Log dir:')
        self.edi_log_file = QLineEdit(cp.log_prefix.value())
        self.edi_dir_ins = QLineEdit(cp.instr_dir.value())

        self.cmb_host = QComboBox(self)        
        self.cmb_host.addItems(cp.list_of_hosts)
        hostname = cp.cdb_host.value()
        idx = cp.list_of_hosts.index(hostname) if hostname in cp.list_of_hosts else 1
        self.cmb_host.setCurrentIndex(idx)

        self.cmb_port = QComboBox(self)        
        self.cmb_port.addItems(cp.list_of_str_ports)
        self.cmb_port.setCurrentIndex(cp.list_of_str_ports.index(str(cp.cdb_port.value())))

        self.cmb_level = QComboBox(self)        
        self.cmb_level.addItems(self.log_level_names)
        self.cmb_level.setCurrentIndex(self.log_level_names.index(cp.log_level.value()))

        self.grid = QGridLayout()
        self.grid.addWidget(self.lab_host, 0, 0)
        self.grid.addWidget(self.cmb_host, 0, 1, 1, 1)

        self.grid.addWidget(self.lab_port, 2, 0)
        self.grid.addWidget(self.cmb_port, 2, 1, 1, 1)

        self.grid.addWidget(self.lab_dir_ins, 3, 0)
        self.grid.addWidget(self.edi_dir_ins, 3, 1, 1, 1)

        self.grid.addWidget(self.lab_level, 4, 0)
        self.grid.addWidget(self.cmb_level, 4, 1, 1, 1)

        self.grid.addWidget(self.lab_log_file, 5, 0)
        self.grid.addWidget(self.edi_log_file, 5, 1, 1, 1)

        self.setLayout(self.grid)
        
        self.cmb_host.currentIndexChanged[int].connect(self.on_cmb_host_changed)
        self.cmb_port.currentIndexChanged[int].connect(self.on_cmb_port_changed)
        self.cmb_level.currentIndexChanged[int].connect(self.on_cmb_level_changed)
        self.edi_log_file.editingFinished.connect(self.on_edi_log_file)
        self.edi_dir_ins.editingFinished.connect(self.on_edi_dir_ins)

        self.set_tool_tips()
        self.set_style()

    def set_tool_tips(self):
        self.cmb_host.setToolTip('Select DB host')
        self.cmb_port.setToolTip('Select DB port')

    def set_style(self):
        self.         setStyleSheet(style.styleBkgd)
        self.lab_host.setStyleSheet(style.styleLabel)
        self.lab_port.setStyleSheet(style.styleLabel)
        self.lab_level.setStyleSheet(style.styleLabel)
        self.lab_log_file.setStyleSheet(style.styleLabel)
        self.lab_dir_ins.setStyleSheet(style.styleLabel)

        self.setMaximumSize(400,600)

    #def resizeEvent(self, e):
    #    logger.debug('resizeEvent size: %s' % str(e.size())) 


    #def moveEvent(self, e):
        #logger.debug('moveEvent pos: %s' % str(e.pos())) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())

    def closeEvent(self, event):
        logger.debug('closeEvent')
        #try   : del cp.guiworkresdirs # CMWConfigPars
        #except: pass # silently ignore
#
#
#   def onClose(self):
#       logger.debug('onClose')
#       self.close()
#
#    def onButShowVers(self):
#        #list_of_pkgs = ['CalibManager', 'ImgAlgos'] #, 'CSPadPixCoords', 'PSCalib', 'pdscalibdata']
#        #msg = 'Package versions:\n'
#        #for pkg in list_of_pkgs:
#        #    msg += '%s  %s\n' % (gu.get_pkg_version(pkg).ljust(10), pkg.ljust(32))
#
#        #msg = cp.package_versions.text_version_for_all_packages()
#        msg = cp.package_versions.text_rev_and_tag_for_all_packages()
#        logger.info(msg)
#
#
#    def onButLsfStatus(self):
#        queue = cp.bat_queue.value()
#        farm = cp.dict_of_queue_farm[queue]
#        msg, status = gu.msg_and_status_of_lsf(farm)
#        msgi = '\nLSF status for queue %s on farm %s: \n%s\nLSF status for %s is %s' % \
#               (queue, farm, msg, queue, {False:'bad',True:'good'}[status])
#        logger.info(msgi)
#
#        cmd, msg = gu.text_status_of_queues(cp.list_of_queues)
#        msgq = '\nStatus of queues for command: %s \n%s' % (cmd, msg)       
#        logger.info(msgq)
#
#    def onButDirWork(self):
#        self.selectDirectory(cp.dir_work, self.edi_dir_work, 'work')
#
#    def onButDirResults(self):
#        self.selectDirectory(cp.dir_results, self.edi_dir_results, 'results')
#
#    def selectDirectory(self, par, edi, label=''):        
#        logger.debug('Select directory for ' + label)
#        dir0 = par.value()
#        path, name = os.path.split(dir0)
#        dir = str(QtGui.QFileDialog.getExistingDirectory(None,'Select directory for '+label,path))
#
#        if dir == dir0 or dir == '':
#            logger.info('Directiry for ' + label + ' has not been changed.')
#            return
#        edi.setText(dir)        
#        par.setValue(dir)
#        logger.info('Set directory for ' + label + str(par.value()))
#        gu.create_directory(dir)
#
#    def onBoxBatQueue(self):
#        queue_selected = self.box_bat_queue.currentText()
#        cp.bat_queue.setValue( queue_selected ) 
#        logger.info('onBoxBatQueue - queue_selected: ' + queue_selected)
#

#    def onEdiDarkStart(self):
#        str_value = str(self.edi_dark_start.displayText())
#        cp.bat_dark_start.setValue(int(str_value))      
#        logger.info('Set start event for dark run: %s' % str_value)
#
#    def onEdiDarkEnd(self):
#        str_value = str(self.edi_dark_end.displayText())
#        cp.bat_dark_end.setValue(int(str_value))      
#        logger.info('Set last event for dark run: %s' % str_value)
#
#    def onEdiDarkScan(self):
#        str_value = str(self.edi_dark_scan.displayText())
#        cp.bat_dark_scan.setValue(int(str_value))      
#        logger.info('Set the number of events to scan: %s' % str_value)
#
#    def onEdiTimeOut(self):
#        str_value = str(self.edi_timeout.displayText())
#        cp.job_timeout_sec.setValue(int(str_value))      
#        logger.info('Job execution timout, sec: %s' % str_value)
#
#    def onEdiDarkSele(self):
#        str_value = str(self.edi_dark_sele.displayText())
#        if str_value == '': str_value = 'None'
#        cp.bat_dark_sele.setValue(str_value)      
#        logger.info('Set the event code for selector: %s' % str_value)
#
#    def onEdiRmsThrMin(self):
#        str_value = str(self.edi_rms_thr_min.displayText())
#        cp.mask_rms_thr_min.setValue(float(str_value))  
#        logger.info('Set hot pixel RMS MIN threshold: %s' % str_value)
#
#    def onEdiRmsThr(self):
#        str_value = str(self.edi_rms_thr_max.displayText())
#        cp.mask_rms_thr_max.setValue(float(str_value))  
#        logger.info('Set hot pixel RMS MAX threshold: %s' % str_value)
#
#    def onEdiMinThr(self):
#        str_value = str(self.edi_min_thr.displayText())
#        cp.mask_min_thr.setValue(float(str_value))  
#        logger.info('Set hot pixel intensity MIN threshold: %s' % str_value)
#
#
#    def onEdiMaxThr(self):
#        str_value = str(self.edi_max_thr.displayText())
#        cp.mask_max_thr.setValue(float(str_value))  
#        logger.info('Set hot pixel intensity MAX threshold: %s' % str_value)
#
#    def onEdiRmsNsigLo(self):
#        str_value = str(self.edi_rmsnlo.displayText())
#        cp.mask_rmsnlo.setValue(float(str_value))  
#        logger.info('Set nsigma low limit of rms: %s' % str_value)
#
#    def onEdiRmsNsigHi(self):
#        str_value = str(self.edi_rmsnhi.displayText())
#        cp.mask_rmsnhi.setValue(float(str_value))  
#        logger.info('Set nsigma high limit of rms: %s' % str_value)
#
#    def onEdiIntNsigLo(self):
#        str_value = str(self.edi_intnlo.displayText())
#        cp.mask_intnlo.setValue(float(str_value))  
#        logger.info('Set nsigma low limit of intensity: %s' % str_value)
#
#    def onEdiIntNsigHi(self):
#        str_value = str(self.edi_intnhi.displayText())
#        cp.mask_intnhi.setValue(float(str_value))  
#        logger.info('Set nsigma high limit of intensity: %s' % str_value)


#    def on_cbx(self, par, cbx):
#        #if cbx.hasFocus():
#        par.setValue(cbx.isChecked())
#        msg = 'check box %s is set to: %s' % (cbx.text(), str(par.value()))
#        logger.info(msg)


#    def on_cbx_host_changed(self, i):
#        logger.debug('XXX: %s' % str(type(i))
#        self.on_cbx(cp.cdb_host, self.cbx_host)


#    def on_cbx_port_changed(self, i):
#        self.on_cbx(cp.cdb_port, self.cbx_port)

    def on_cmb_host_changed(self):
        selected = self.cmb_host.currentText()
        cp.cdb_host.setValue(selected) 
        logger.info('Set DB host: %s' % selected)

    def on_cmb_port_changed(self):
        selected = self.cmb_port.currentText()
        cp.cdb_port.setValue(int(selected)) 
        logger.info('Set DB port: %s' % selected)

    def on_cmb_level_changed(self):
        selected = self.cmb_level.currentText()
        cp.log_level.setValue(selected) 
        logger.info('Set logger level %s' % selected)

    def on_edi(self, par, but):
        #logger.debug('on_edi')
        par.setValue(str(but.displayText()))
        logger.info('Set field: %s' % str(par.value()))

    def on_edi_log_file(self):
        ##logger.debug('on_edi_log_file')
        self.on_edi(cp.log_prefix, self.edi_log_file)
        #cp.log_prefix.setValue(str(self.edi_log_file.displayText()))
        #logger.info('Set logger file name: ' + str(cp.log_prefix.value()))

    def on_edi_dir_ins(self):
        self.on_edi(cp.instr_dir, self.edi_dir_ins)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    app = QApplication(sys.argv)
    w = CMWConfigPars()
    w.setGeometry(200, 400, 500, 200)
    w.setWindowTitle('Config Parameters')
    w.show()
    app.exec_()
    del w
    del app

# EOF
