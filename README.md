# Subseeker
Automatic Subtitle Downloading Tool for Nautilus in Ubuntu.
Uses opensubtitles.org's XMLRPC based API to query and download subtitles.

Its frontend is basically a Nautilus-Action Config, that gives a submenu option to download subtitles.

The backend is a small python script that generates the video files hash and does a query to the opensubtitles API.

<b>The Default Environment used is Python2.x as the hashing function isn't very compatible with Python3.x.</b>

If any Subtitle is there related to the video hash, it downloads it automatically and places the subtitle in the same folder as the video.

Language Support has been added , and the default language is to be selected during the process of installation.

</hr></br>
<b>Dependencies are:</b>

<li>Nautilus Action Config Tool </li>
<b>Note:</b><i> You'll be automatically asked to install it while installing Subseeker. </i>
</br>

</br></hr>
<b>Size Information:</b>
<li>Total size including Nautilus Action Config Tool: ~ 13 MegaBytes</li>
<li>Total size excluding Nautilus Action Config Tool: ~ 140 KiloBytes </li>
</br>
</br>
<b>Installation Procedure: </b>
<ol>
<li> You must have an Opensubtitles Account to use this app.</li>

<li> Follow : <i>"https://www.opensubtitles.org/en/newuser"</i>   , to register.</li>

<li> Download or clone the Archived Package to your home folder.</li>

<li> Extract the tar ball (Compressed Archive) to **Home folder** .</li>

<li> Navigate to subseeker folder.</li>

<li> In explorer (File manager window of subseeker folder) , right click and select 'Open in Terminal'.</li>

<li> In the terminal Window type: <code>$ sudo python3 Install.py</code></li>

<li> Enter 'y' if asked to install Dependencies.(external utility packages.)</li>

<li> A Setup window pops up, Enter your opensubtitle user-name and password there and select your default language.</li>

<li> Once the Partial installation complete , a new read-me will open with futher instructions.</li>

</ol>

</hr></br>
<b>Usage Instructions: </b> </hr></br></hr></br>
Just Navigate to any Video and Right Click , You'll See a "Get Subtitle" (Shown In Image Below) Option in the Sub-menu. 
</br></hr></br></hr>

![Image Showing Submenu Option "Get Subtitles" in Nautilus.](/Screenshots/Nautilus_Submenu_Option.png "Image Showing Submenu Option 'Get Subtitles' in Nautilus.")

</br></hr></br></hr>
After Clicking the sub-menu Option a new confirmational window will appear and You'll see the subtitles Appear in the Folder.(Shown in Image Below)
</br></hr><b>Note:</b><i></br></hr> <ul><li>It takes some time to search and download the Subtitles (2-5 Secs) Depending Upon you computer and Internet Speed.</li><li> The Subtitles will only be downloaded if they exist on Opensubtitles Website. </i></li></ul>

![Image Showing Downloaded Subtitle and confirmation window in Nautilus.](/Screenshots/Downloaded_File_With_confirmation.png "Image Showing Downloaded Subtitle and confirmation window in Nautilus.")


</br></hr></br></hr>
<b>Feedback:</b>
For feedback or error reporting please E-mail me at: <mailto:ubdussamad@gmail.com>.
