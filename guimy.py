from psychopy import gui
from psychopy import core


def present_gui():
    dlg = None

    dialog = gui.Dlg(title="Intentional Binding", screen=0)
    #
    dialog.addField('Participant ID', 'tester')
    dialog.addField('Participant Age', 19)
    dialog.addField('Participant Sex', choices=['female', 'male', 'other'])
    #
    dialog.addField('Condition', choices=['baseline action', 'baseline tone', 'action-effect action', 'action-effect tone'])
    #
    dialog.addField('Stimulus size', choices=['window', 'fullscreen'])
    #
    dialog.show()
    if dialog.OK:
        dlg = {dialog.__dict__["inputFieldNames"][i]: dialog.__dict__["data"][i] for i in range(len(dialog.__dict__["data"]))}
    else:
        print('user cancelled')
        core.quit()
    return dlg
