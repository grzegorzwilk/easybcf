# TODO UTF-8

# first run "source venv/bin/activate"

import base64
import os
import uuid

import bcf.v3.bcfxml as BCF # type: ignore
import bcf.v3.model as MDL
import bcf.v3.visinfo as VIS

def prepare_snapshot(snapshot_filename: str) -> str:
    """Reads a PNG file and returns its Base64 encoded string."""
    full_snapshot_path = os.path.join(os.path.dirname(__file__), snapshot_filename)
    
    with open(full_snapshot_path, "rb") as image_file:
        # Encode the image file to Base64 and return the string
        return base64.b64encode(image_file.read()).decode('utf-8')

bcf = BCF.BcfXml()
new_bcf = bcf.create_new("LKJDLFJ")

new_topic = new_bcf.add_topic(
        title="New Topic Title",
        description="This is a description of the new topic.",
        author="John Doe", # This might be redundant
        topic_type="Issue", # This might be redundant
        topic_status="Open" # This might be redundant
    )

snapshot = prepare_snapshot("snapshot.png")

# Create a new VisualizationInfo object
visualization_info = MDL.VisualizationInfo(
    guid=str(uuid.uuid4()),  # Generate a new GUID
    components=MDL.Components(),  # Initialize components as needed
)

new_viewpoint = VIS.VisualizationInfoHandler(visualization_info)
new_viewpoint = new_topic.add_visinfo_handler(new_viewpoint, snapshot_filename=snapshot)

new_bcf.save("test.bcf") # TODO activate
print(new_bcf )