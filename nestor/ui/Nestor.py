from nestor.ui.taggingUI_app import MyTaggingToolWindow, openYAMLConfig_File


from PyQt5.QtWidgets import QApplication, QMessageBox, qApp
from PyQt5 import QtCore
import sys
import traceback
from pathlib import Path


def exception_handler(type_, value, traceback_):
    if qApp.thread() is QtCore.QThread.currentThread():
        p = traceback.format_exc()
        msg = QMessageBox()
        msg.setWindowTitle("Nestor has encountered an error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An unhandled error occurred! Check the log for more detailed information...")
        msg.setDetailedText(p)
        msg.setEscapeButton(QMessageBox.Ok)
        msg.exec_()



def main():

    app = QApplication(sys.argv)

    stylesheet = """
        QGroupBox { 
            border: 1px solid gray;
            border-radius: 9px;
            font-weight: bold;
            margin-top: 0.5em;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        """
    projectsPath = Path.home() / '.nestor-tmp'
    projectsPath.mkdir(parents=True, exist_ok=True)


    nestorPath = Path(__file__).parent.parent
    databaseToCsv_mapping = openYAMLConfig_File(
        yaml_path= nestorPath / 'store_data' / 'csvHeader.yaml'
    )
    icon_path = nestorPath / 'ui' / 'kea-icon.png'
    print(str(icon_path))
    app.setStyleSheet(stylesheet)
    window = MyTaggingToolWindow(projectsPath=projectsPath,
                                 iconPath=str(icon_path),
                                 databaseToCsv_mapping = databaseToCsv_mapping)
    # sys.excepthook = exception_handler
    sys.exit(app.exec_())



if __name__ == "__main__":
    print(
        "====================================================================\n",
        " Welcome to NESTOR, a tagging tool created by the KEA team at NIST\n",
        " It allows you to nicely tag your human-written Maintenance Data in \n",
        " order to make it computable by a machine and easily readable by you\n",
        "====================================================================\n"
    )


    main()

