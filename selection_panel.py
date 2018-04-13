import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# List of tuples (this is the model, aka the data that will be displayed by the TreeView)

index = None
class TreeViewFilterWindow(Gtk.Window):
    
    def __init__(self,people):
        Gtk.Window.__init__(self, title="Subseeker v4")

        #Main list box
        main_list_box = Gtk.ListBox()
        self.add(main_list_box)

        #Box container for labels
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)

        self.heading_text = Gtk.Label()
        self.heading_text.set_markup('''<big><b>Choose Subtitles below</b></big>\n\n<i>Select a subtitle and press Download.</i>\n''')
        label_box.pack_start(self.heading_text,1,1,0)
        label_box.set_center_widget(self.heading_text)
        main_list_box.add(label_box)
        
        
        # Box container for treeview
        tree_view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)

        # Convert data to ListStore (lists that TreeViews can display) and specify data types
        self.people_list_store = Gtk.ListStore(str,str,str, str)
        for item in people:
            self.people_list_store.append(list(item[:4]))


        # TreeView is the item that is displayed
        self.people_tree_view = Gtk.TreeView(self.people_list_store)

        # Enumerate to add counter (i) to loop
        for i, col_title in enumerate(["#","Name", "Language", "Score",]):

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

        self.submit_button = Gtk.Button(label="Download")
        self.submit_button.connect("clicked", self.select_handle)
        buttons_box.pack_start(self.submit_button, True , True  , 0)

        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", lambda:self.destroy())
        buttons_box.pack_start(self.cancel_button, True , True  , 0)
        
        main_list_box.add(buttons_box)

        
    def select_handle(self,widget):
        global index
        tree_sel = self.people_tree_view.get_selection()
        (tm, ti) = tree_sel.get_selected()
        #print(tm.get_value(ti, 1))
        index = tm.get_value(ti, 0)
        self.destroy()

def qt(subs):
    window = TreeViewFilterWindow(subs)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    
def run(subs):
    qt(subs)
    return(index)
        

