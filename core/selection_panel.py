import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

index = None #Global variable holding the index of the final chosen subtitle
class window(Gtk.Window):
        def __init__(self,data):
                Gtk.Window.__init__(self, title="SubseekerV7 R&D")
                self.set_border_width(5)
                self.set_default_size(200, 400)
                self.grid = Gtk.Grid()
                self.grid.set_column_homogeneous(True)
                self.grid.set_rowndex = None

                heading_text = Gtk.Label()
                heading_text.set_markup('<big><b>Choose Subtitle below</b></big>\n\n<i>Select a subtitle and press Download</i>\n')

                scrolled_window = Gtk.ScrolledWindow()
                scrolled_window.set_border_width(5)
                scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
                self.data_list_store = Gtk.ListStore(str,str,str, str)
                for item in data:self.data_list_store.append(list(item[:4]))
                self.data_tree_view = Gtk.TreeView(self.data_list_store)
                for i, col_title in enumerate(["Serial","Name", "Language", "Score",]):
                        renderer = Gtk.CellRendererText()
                        column = Gtk.TreeViewColumn(col_title, renderer, text=i)
                        self.data_tree_view.append_column(column)
                scrolled_window.add_with_viewport(self.data_tree_view);
                # Setting a fixed height
                scrolled_window.set_size_request(-1, 200)
                # Configure the scrolled window to expand
                scrolled_window.set_property('expand', True)

                buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)

                #Button Declarations
                self.submit_button = Gtk.Button(label="Download")
                self.submit_button.connect("clicked", self.select_handle)
                self.cancel_button = Gtk.Button(label="Cancel")
                self.cancel_button.connect("clicked", lambda x:self.destroy())

                #Adding buttons to button box
                buttons_box.pack_start(self.submit_button, True , True  , 0)
                buttons_box.pack_start(self.cancel_button, True , True  , 0)


                self.grid.attach(heading_text, 0, 0, 4, 1)
                self.grid.attach(scrolled_window,0,1,4,4)
                self.grid.attach(buttons_box,0,5,4,1)

                self.add(self.grid)
        def select_handle(self,widget):
                global index
                tree_sel = self.data_tree_view.get_selection()
                (tm, ti) = tree_sel.get_selected()
                index = tm.get_value(ti, 0) #Modifying the index value to the currently selected index in treeview
                self.destroy()
def selection_panel_func(subs):
        w = window(subs) #Bogus test dxata
        w.connect("destroy", Gtk.main_quit)
        w.show_all()
        Gtk.main()
        return(index)

if __name__ == '__main__':
        selection_panel_func([('a'*30,'b','c','d','e'),('p'*30,'q','r','s','t')])