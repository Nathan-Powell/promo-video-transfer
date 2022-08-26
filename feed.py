from datetime import datetime, timedelta
import glob
import csv
import os

class Feed:
    """
    A class to hold feed information from the CSV file.

        Reference for feed_info method options:

        ex. feed_info['DAY'] = SATURDAY

        CATEGORY ------------------ TV
        PERIOD -------------------- Sat 9-7p
        TIMEZONE ------------------ EASTERN
        DATE ---------------------- d/m/yyyy 00:00:00
        DAY ----------------------- SATURDAY
        PRIORITY ------------------ 10
        EVENT_ID ------------------ XYZMONAM1
        AIR_CODE ------------------ 9843-0893-1458
        FILENAME ------------------ IV763HCM902
        TITLE --------------------- Test Program
        
    """

    def __init__(self):
        """
        Initiates variables for video & schedule file formats
        """
        self.vid_format = '.mp4'
        self.schedule_format = '.csv'

    def _timestamp(self):
        """
        Gets date in format to match CSV file
        """
        raw_date = datetime.now()

        # Formats date to YYYY-MM-DD to pattern match CSV filename.
        date_formatted = raw_date.strftime('%Y-%m-%d')
        return date_formatted

    def _get_csv(self):
        """
        Globs through folder to find today's CSV file
        """

        # Timestamp method ensures the script is using today's CSV file.
        files = glob.glob(f'{self._timestamp()}*{self.schedule_format}')

        # Lambda function filters by modified time in case multiple versions
        # of the CSV file have been uploaded due to error/revisions
        files_ascending = sorted(files, key=lambda t: os.stat(t).st_mtime)

        # Returns only the most recent file in the sorted list.
        return files_ascending[0]

    def _time_modified(self, file):
        """
        Returns True if file has been modified within the last 12 hours
        """
        current_time = datetime.now()
        past_time = current_time - timedelta(hours=12)
        if os.path.getmtime(file) > past_time.timestamp():
            return True

    def parse_csv(self):
        """
        A method to parse information from CSV file and store in dictionary
        """
        rows = []

        # Read CSV file as dictionary and append all rows to the rows list.
        with open(self._get_csv(), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return rows

    def get_files(self):
        """
        Iterates over feed folder and returns list of video files
        """
        vid_files = [vid_file for vid_file in glob.glob(f'*{self.vid_format}') if self._time_modified(vid_file)]
        return vid_files



