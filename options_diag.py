import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#This is a test text for git integration
class pop_up(Gtk.MessageDialog):

    def __init__(self,parent):

        Gtk.MessageDialog.__init__(self,parent,0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, "No Subtitles found in your Language.")
        self.format_secondary_text("Would you like to check other languages?")

def question():

    dialog = pop_up(None) #Dialog window mapped without a parent window triggers warnings.
    response = dialog.run()
    user_will = (response == Gtk.ResponseType.YES) #User clicks Yes
    dialog.destroy()
    return user_will


if __name__ == '__main__':
    question() #While running this directly, the dialog freezes after user input
               #but when used externally, it behaves normally
