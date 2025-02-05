import sqlite3
import os
import json

def delete_symlinks(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.islink(item_path):
            os.unlink(item_path)
            print(f"Deleted symlink: {item_path}")
        else:
            print(f"Not a symlink: {item_path}")

# Open the JSON file
with open('env.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    env = json.load(file)

print(env)

# Path to your digiKam SQLite database
db_path = env['db_path']

# images directory
base_dir = env['base_dir']

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


query = '''
SELECT Images.id, Images.name, Images.album, Albums.relativePath
FROM Images
JOIN ImageTags ON Images.id = ImageTags.imageid
JOIN Tags ON ImageTags.tagid = Tags.id
JOIN Albums ON Images.album = Albums.id
WHERE Tags.name = ?
'''


# Specify the tag you want to retrieve
tag_name = env['tag_name']
cursor.execute(query, (tag_name,))


images = []

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    # print(row)
    image_id, image_name, album_id, relative_path = row
    # full_path = os.path.normpath(os.path.join(base_dir, relative_path, image_name))
    full_path = os.path.normpath(f'{base_dir}{relative_path}/{image_name}')
    root, extension = os.path.splitext(full_path)
    if extension == '.jpg':
        # print(full_path)
        images.append(full_path)
    # print(f'Image ID: {image_id}, Full Path: {full_path}')


# Close the connection
conn.close()





# ---------------------------------------------------

symlink_dir = env['symlink_dir']



# Ensure the target directory for the symlink exists
target_directory = os.path.dirname(symlink_dir)
os.makedirs(target_directory, exist_ok=True)

delete_symlinks(symlink_dir)

for image in images:
    # Path where you want to create the symbolic link
    base_name = os.path.basename(image)
    symlink_path = f'{symlink_dir}{base_name}'


    # Create the symbolic link
    try:
        os.symlink(image, symlink_path)
        print(f'Symbolic link created: {symlink_path} -> {image}')
    except OSError as e:
        # print(f'Error: {e}')
        pass
