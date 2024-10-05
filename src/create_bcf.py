from ifcopenshell.bcf import BCF

# Create a BCF object
bcf = BCF()

# Create a topic
topic = bcf.create_topic('Sample Issue', 'Description of the issue here.')

# Optional: Add a viewpoint (with dummy values)
viewpoint = topic.add_viewpoint('viewpoint_1', 'Sample Viewpoint', [0, 0, 0])
viewpoint.set_camera_position(1, 1, 1)  # Set camera position (example)

# Save to BCF file
with open('output.bcf', 'wb') as bcf_file:
    bcf_file.write(bcf.to_bytes())