import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class popup(Gtk.MessageDialog):

    def __init__(self,parent):
        
        Gtk.MessageDialog.__init__(self,parent,0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, "No Subtitles found in your Language.")
        self.format_secondary_text("Would you like to check other languages?")

def ext():
    dialog = popup(None)
    response = dialog.run()
    will = (response == Gtk.ResponseType.YES)
    '''if response == Gtk.ResponseType.YES:
        print("QUESTION dialog closed by clicking YES button")
    elif response == Gtk.ResponseType.NO:
        print("QUESTION dialog closed by clicking NO button")'''
    dialog.destroy()
    return will
    

if __name__ == '__main__':
    ext()
