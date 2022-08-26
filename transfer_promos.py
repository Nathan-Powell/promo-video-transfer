from feed import Feed
import shutil
import os


# Dictionary to initialize all house numbers to their corresponding XYZ house IDs.
id_dict = {'XYZMONAM1': 53996, 'XYZMONAM2': 53987, 'XYZMONAM3': 53348, 'XYZMONMID1': 53299, 
            'XYZMONMID2': 54000, 'XYZMONMID3': 55213, 'XYZMONEVE1': 59745, 'XYZMONEVE2': 53999, 
            'XYZMONEVE3': 53887, 'XYZMONACC1': 53221, 'XYZMONLAT1': 57552}

source = 'C:\\Test\\feed_folder\\'
destination = 'C:\\Test\\output\\'
os.chdir(source)

# Initiate Feed class instance.
feed_folder = Feed()

def get_all_feed_info(filename):
    """
    Takes feed filename as input and returns 
    row as dictionary with all feed info
    """
    for row in feed_folder.parse_csv():
        if filename in row.values():
            feed_info = row
            # Breaks loop so if there is more than one instance
            # of the filename in the CSV file it should only
            # return the first instance
            break
    return feed_info

def rename_and_copy_file(old_name, new_name, src, dest):
    """
    Renames file and copies to destination folder
    """
    os.rename(old_name, new_name)
    shutil.copyfile(src, dest)

if __name__ == "__main__":
    # Loop over the video files in the feed folder and use each video
    # filename to extract that files' row information in the CSV file.
    for file in feed_folder.get_files():
        feed_info = get_all_feed_info(os.path.basename(file)[:-4])
        house_id = feed_info['EVENT_ID']
        last_air_date = feed_info['DATE'][-14:-9]
        new_filename = f'{id_dict[house_id]} {last_air_date}.mp4'
        if house_id and id_dict[house_id]:
            print(f'New filename is {new_filename}')
            rename_and_copy_file(house_id, new_filename, f'{source}{new_filename}', f'{destination}{new_filename}')