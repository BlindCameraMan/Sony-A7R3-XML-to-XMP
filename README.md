# Sony A7R3 XML to XMP

Using Phil Harvey's [Exiftool](https://exiftool.org/) and [PyExiftool](https://github.com/sylikc/pyexiftool) by sylikc this script scans the current directory for Sony .xml sidecar files and extracts the shot date and time, device make, model, serial number, and GPS information and renames the files in the following format:

C0001MO1.XML -> C0001.XMP

If the filename for the XML does not match this format the XMP will be keep the same exact name.
2025-12-31T11-43-50 - C0003.XML -> 2025-12-31T11-43-50 - C0003.XMP
