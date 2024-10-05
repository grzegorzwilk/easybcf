# TODO UTF-8

# first run "source venv/bin/activate"

import bcf.v3.bcfxml as BCF

bcf = BCF.BcfXml()
new_bcf = bcf.create_new("LKJDLFJ")

new_topic = new_bcf.add_topic(
        title="New Topic Title",
        description="This is a description of the new topic.",
        author="John Doe", # This might be redundant
        topic_type="Issue", # This might be redundant
        topic_status="Open" # This might be redundant
    )

new_bcf.save("test.bcf")
print(new_bcf )