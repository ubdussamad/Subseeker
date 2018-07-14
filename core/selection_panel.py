import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

'''
Subtitle Selection UI for Subseeker 4v0.
'''


index = None #Global variable holding the index of the final chosen subtitle

class TreeViewFilterWindow(Gtk.Window):
    
    def __init__(self,people):
        Gtk.Window.__init__(self, title="Subseeker V4")
        self.set_border_width(2)
        
        #Main list box
        main_list_box = Gtk.ListBox()
        self.add(main_list_box)

        #Box container for labels
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)

        #Heading Labels
        self.heading_text = Gtk.Label()
        self.heading_text.set_markup('''<big><b>Choose Subtitle below</b></big>\n\n<i>Select a subtitle and press Download</i>\n''')
        label_box.pack_start(self.heading_text,1,1,0)
        label_box.set_center_widget(self.heading_text)
        main_list_box.add(label_box)
        
        
        # Box container for treeview
        tree_view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        

        # Convert raw data to ListStore
        self.people_list_store = Gtk.ListStore(str,str,str, str)
        for item in people:self.people_list_store.append(list(item[:4]))


        # Initializing Tree View using the ListStore
        self.people_tree_view = Gtk.TreeView(self.people_list_store)

        # Enumerate to add counter (i) to loop
        for i, col_title in enumerate(["Serial","Name", "Language", "Score",]):

            # Render means draw or display the data (just display as normal text)
            renderer = Gtk.CellRendererText()

            # Create columns (text is column number)
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)

            # Add columns to TreeView
            self.people_tree_view.append_column(column)

        # Add to tree_view_box
        tree_view_box.pack_start(self.people_tree_view, True, True, 0)

        #Add tree_view_box to listbox
        main_list_box.add(tree_view_box)

        #Button Box
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)

        #Button Declarations
        self.submit_button = Gtk.Button(label="Download")
        self.submit_button.connect("clicked", self.select_handle)
        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", lambda x:self.destroy())

        #Adding buttons to button box
        buttons_box.pack_start(self.submit_button, True , True  , 0)
        buttons_box.pack_start(self.cancel_button, True , True  , 0)

        #Adding button box to the list box
        main_list_box.add(buttons_box)

        
    def select_handle(self,widget):
        global index
        tree_sel = self.people_tree_view.get_selection()
        (tm, ti) = tree_sel.get_selected()
        index = tm.get_value(ti, 0) #Modifying the index value to the currently selected index in treeview
        self.destroy()

def main_window(raw_sub_data):
    window = TreeViewFilterWindow(raw_sub_data)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    
def selection_panel_func(raw_sub_data):
    main_window(raw_sub_data)
    return(index)


if __name__ == "__main__":
    lists = [('a'*30,'b','c','d','e'),('p'*30,'q','r','s','t')] #Bogus data for testing and stuff
    selection_panel_func(lists)

