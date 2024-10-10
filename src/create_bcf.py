import xml.etree.ElementTree as ET
import datetime
import uuid
import zipfile
import os
import random

def create_bcf(topic_title="topic text", author="author name", comment_text="comment text", description="some description text", project_int=123):

    proj_id = str(uuid.UUID(int=random.Random(project_int).randint(0, 9999), version=4))
    top_guid = str(uuid.uuid4())
    comm_guid = str(uuid.uuid4())
    vp_guid = str(uuid.uuid4())
    now = datetime.datetime.isoformat(datetime.datetime.now())

    markup = ET.Element("Markup", attrib={'xmlns:xs':"http://www.w3.org/2001/XMLSchema"})
    ET.SubElement(markup, "Header")
    topic = ET.SubElement(markup, "Topic", Guid=top_guid, TopicType="Issue", TopicStatus="Active")
    ET.SubElement(topic, "Title").text = topic_title
    ET.SubElement(topic, "Description").text = description
    ET.SubElement(topic, "CreationDate").text = now
    ET.SubElement(topic, "CreationAuthor").text = author

    comment = ET.SubElement(markup, "Comment", Guid=comm_guid)
    ET.SubElement(comment, "Date").text = now
    ET.SubElement(comment, "Author").text = author
    ET.SubElement(comment, "Comment").text = comment_text
    ET.SubElement(comment, "Topic", Guid=top_guid)
    ET.SubElement(comment, "Viewpoint", Guid=vp_guid)

    viewpoints = ET.SubElement(markup, "Viewpoints", Guid=vp_guid)
    ET.SubElement(viewpoints, "Viewpoint").text = "viewpoint.bcfv"
    if os.path.isfile("snapshot.jpg"):
        ET.SubElement(viewpoints, "Snapshot").text = "snapshot.jpg"

    tree = ET.ElementTree(markup)
    ET.indent(tree, '  ')
    tree.write("markup.bcf", xml_declaration=True, encoding="UTF-8")


    viz_info = ET.Element("VisualizationInfo", attrib={'xmlns:xs':"http://www.w3.org/2001/XMLSchema", "Guid":vp_guid})
    ET.SubElement(viz_info, "Components")
    tree = ET.ElementTree(viz_info)
    ET.indent(tree, '  ')
    tree.write("viewpoint.bcfv", xml_declaration=True, encoding="UTF-8")

    proj = ET.Element("ProjectInfo", attrib={'xmlns:xs':"http://www.w3.org/2001/XMLSchema"})
    ET.SubElement(proj, "Project", ProjectId=proj_id)
    tree = ET.ElementTree(proj)
    ET.indent(tree, '  ')
    tree.write("project.bcfp", xml_declaration=True, encoding="UTF-8")

    version = ET.Element("Version", attrib={'xmlns:xs':"http://www.w3.org/2001/XMLSchema", 'VersionId':"3.0"})
    tree = ET.ElementTree(version)
    ET.indent(tree, '  ')
    tree.write("bcf.version", xml_declaration=True, encoding="UTF-8")

    extensions = ET.Element("Extensions", attrib={'xmlns:xs':"http://www.w3.org/2001/XMLSchema"})
    tree = ET.ElementTree(extensions)
    ET.indent(tree, '  ')
    tree.write("extensions.xml", xml_declaration=True, encoding="UTF-8")

    with zipfile.ZipFile('new_issue.bcfzip', 'a') as zipf:
        files_in_zip = zipf.namelist()

        for file in ['bcf.version', 'project.bcfp', 'extensions.xml']:
            if file not in files_in_zip:  
                zipf.write(file)
        
        
        folder = top_guid
        
        for file in ["markup.bcf", "viewpoint.bcfv"]:
            file_path = os.path.join(folder, file)
            zipf.write(file, file_path)
            
        if os.path.isfile("snapshot.jpg"):
            file_path = os.path.join(folder, "snapshot.jpg")
            zipf.write("snapshot.jpg", file_path)

    for file in ["markup.bcf", "viewpoint.bcfv", "bcf.version", "extensions.xml", "project.bcfp"]:
        os.remove(file)

    if os.path.isfile("snapshot.jpg"):
        os.remove("snapshot.jpg")

    print("success?")
    