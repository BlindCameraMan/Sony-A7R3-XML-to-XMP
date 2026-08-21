import os
import exiftool
from exiftool import ExifToolHelper
import xml.etree.ElementTree as ET

x = 0
os.chdir(r"D:\Documents\Python\Sony A7R3 XML to XMP\test videos")
xml_files_list = []
with os.scandir() as xmlListEntries:
 for entry in xmlListEntries:
  if entry.is_file() and entry.name.lower().endswith('.xml'):
   xml_files_list.append(entry.name)
# tree = ET.parse(xml_files_list)
# root = tree.getroot()
# raw_namespaces = {node[0]: node[1] for _, node in ET.iterparse(xml_files_list, events=['start-ns'])}
# namespaces = {}
# for prefix, uri in raw_namespaces.items():
#     if prefix == '':
#         namespaces['ns'] = uri  # Assign 'ns' to the default namespace URI
#     else:
#         namespaces[prefix] = uri

for xml_file in xml_files_list:
#     print(xml_file)
    tags = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    raw_namespaces = {node[0]: node[1] for _, node in ET.iterparse(xml_file, events=['start-ns'])}
    namespaces = {}
    for prefix, uri in raw_namespaces.items():
        if prefix == '':
            namespaces['ns'] = uri  # Assign 'ns' to the default namespace URI
        else:
            namespaces[prefix] = uri
    device_elem = root.find(".//ns:Device", namespaces)
    print(xml_file)
    if device_elem is not None:
        tags["Model"] = device_elem.get("modelName")
#         print("Model Name:", ModelName)
        tags["Make"] = device_elem.get("manufacturer")
#         print("Manufacturer:", Manufacturer)
        tags["SerialNumber"] = device_elem.get("serialNo")
#         print("Serial Number:", SerialNo)
    else:
        print("Make and Model not found.")
        
#     duration_elem = root.find(".//ns:Duration", namespaces)
#     if duration_elem is not None:
#         xml_video_duration = duration_elem.get("value")
#         print("XML Video Duration is:", xml_video_duration)
#     else:
#         print("Duration not found.")

    CreationDate_elem = root.find(".//ns:CreationDate", namespaces)
    if CreationDate_elem is not None:
        tags["xmp:CreateDate"] = CreationDate_elem.get("value")
#         print("Creation Date is:", CreationDate)
    else:
        print("Creation Date not found.")

#     VideoFormat_elem = root.find(".//ns:VideoFormat", namespaces)
#     if VideoFormat_elem is not None:
#         video_frame = VideoFormat_elem.find("ns:VideoFrame", namespaces)
#         video_layout = VideoFormat_elem.find("ns:VideoLayout", namespaces)
#         if video_frame is not None:
#             codec = video_frame.get("videoCodec")
#             fps = video_frame.get("captureFps")
#             print(f"Codec: {codec}")
#             print(f"FPS: {fps}")
#         if video_layout is not None:
#             pixels = video_layout.get("pixel")
#             lines = video_layout.get("numOfVerticalLine")
#             aspect = video_layout.get("aspectRatio")
#             print(f"Resolution: {pixels}x{lines}")
#             print(f"Aspect Ratio: {aspect}")
#     else:
#         print("VideoFormat element not found.")
    gps_group = latitude = longitude = latitudeRef = longitudeRef = None
    latitudeSplit = latitudeDD = longitudeSplit = longitudeDD = None
    gps_group = root.find(".//ns:Group[@name='ExifGPS']", namespaces)
    if gps_group is not None:
        for item in gps_group.findall("ns:Item", namespaces):
            if item.get("name") == "Latitude":
#                 print("Latitude:", item.get("value"))
                latitude = item.get("value")
            if item.get("name") == "Longitude":
#                 print("Longitude:", item.get("value"))
                longitude = item.get("value")
            if item.get("name") == "LatitudeRef":
#                 print("LatitudeRef:", item.get("value"))
                latitudeRef = item.get("value")
            if item.get("name") == "LongitudeRef":
                longitudeRef = item.get("value")
#                 print("LongitudeRef:", item.get("value"))
            if item.get("name") == "VersionID":
                tags["XMP:GPSVersionID"] = item.get("value")
            if item.get("name") == "Status":
                tags["XMP:GPSStatus"] = item.get("value")
            if item.get("name") == "MeasureMode":
                tags["XMP:GPSMeasureMode"] = item.get("value")
            if item.get("name") == "MapDatum":
                tags["XMP:GPSMapDatum"] = item.get("value")
            if item.get("name") == "Differential":
                tags["XMP:GPSDifferential"] = item.get("value")
            if item.get("name") == "TimeStamp":
                xml_TimeStamp = item.get("value")
            if item.get("name") == "DateStamp":
                xml_DateStamp = item.get("value")
#                 tags["xmp-exif:GPSDateTime"] = (f'{xml_DateStamp} {xml_TimeStamp}')
    if latitude and longitude != None:
        latitudeSplit = latitude.split(":")
        print(latitudeSplit)
        latitudeDD = (float(latitudeSplit[0]) + (float(latitudeSplit[1]) / 60) + (float(latitudeSplit[2]) / 3600))
        if latitudeRef == "S":
            latitudeDD = latitudeDD * -1
        if latitudeRef == "N":
            latitudeDD = latitudeDD
        print(latitudeDD)

        longitudeSplit = longitude.split(":")
        print(longitudeSplit)
        longitudeDD = (float(longitudeSplit[0]) + (float(longitudeSplit[1]) / 60) + (float(longitudeSplit[2]) / 3600))
        if longitudeRef == "W":
            longitudeDD = longitudeDD * -1
        if longitudeRef == "E":
            longitudeDD = longitudeDD
        print(longitudeDD)
        tags.update({"XMP:GPSLatitude": latitudeDD, "XMP:GPSLongitude": longitudeDD})
        tags["xmp-exif:GPSDateTime"] = (f'{xml_DateStamp} {xml_TimeStamp}')
    x = x + 1
    filename = f"test{x}.xmp"
    print(filename)
    with ExifToolHelper() as et:
        et.set_tags(
            filename,
            tags,    
            params=["-P", "-overwrite_original"]
        )
