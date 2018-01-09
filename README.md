# Subseeker
Automatic Subtitle Downloading Tool for Nautilus in Ubuntu.
Use opensubtitles.org's XMLRPC api to query and download subtitles.

It's frontend is basically a Nautilus-Action Config , that gives a submenu option to download subtilies.

Backend is a small python script that genrates the video files hash and does a query to the opensubtitles api.

If any Subtitle is there related with the video hash , it downloads it automatically and places the subtitle in the same folder as the video.

As if now , it only downloads English subtitles but language support will be added in coming versions.

Dependencies are:

*Nautilus Action Config Tool


Total size including Nautilus Action Config Tool: ~ 13 MegaBytes
Total size excluding Nautilus Action Config Tool: ~ 30 KiloBytes
