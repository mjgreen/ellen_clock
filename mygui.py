from psychopy import gui
from psychopy import core


def present_gui():
    dlg = None

    dialog = gui.Dlg(title="Intentional Binding", screen=1)
    #
    dialog.addField('Participant ID', 'test')
    dialog.addField('Participant Age', 19)
    dialog.addField('Participant Sex', choices=['female', 'male', 'other'])
    #
    dialog.addField('Condition', choices=['baseline action', 'baseline with tone', 'action-effect: action', 'action-effect: tone'])
    #
    dialog.show()
    if dialog.OK:
        dlg = {dialog.__dict__["inputFieldNames"][i]: dialog.__dict__["data"][i] for i in range(len(dialog.__dict__["data"]))}
        if not dlg['Condition'] == 'baseline action':
            print('not implemented yet')
            core.quit()
        elif dlg['Condition'] == 'baseline action':
            pass
    else:
        print('user cancelled')
        core.quit()
    return dlg
