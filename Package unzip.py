import os
import zipfile
# Choose a folder where the zips are stored
path = r'\\srpzyfap0003.insim.biz\ESGShare\GRP\FLECS_share\User Folders\Yiming Liang\SCR Prediction Tool\DataBase'
# Write the start of the zip folder name
# Choose file(s) you want to extract
zip_name = "report"
reports = ["BSCR_IM_MarketRisk_Position_Report_EUR.csv"]
# True = Files will be extracted to zip file named subfolders False = Files will be saved next to the zips
subfolder = True

# Set to keep track of unzipped folders
unzipped_folders = set()

os.chdir(path)
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.zip') and file.startswith(zip_name):
            # Extract the identifier from the zip file name
            identifier = file[7:12].rstrip(".zip")
            if identifier not in unzipped_folders:
                with zipfile.ZipFile(os.path.join(root, file), 'r') as zip_ref:
                    zipinfos = zip_ref.infolist()
                    for report in reports:
                        new_name = report.rstrip(".csv") + "_" + identifier + ".csv"
                        for zipinfo in zipinfos:
                            if zipinfo.filename == report and new_name not in files:
                                zipinfo.filename = new_name
                                if subfolder:
                                    print(f"Extracting {report} from {file} in {root + '/' + file.rstrip('.zip')}")
                                    zip_ref.extract(member=report, path=root + '/' + file.rstrip('.zip'))
                                else:
                                    print(f"Extracting {zipinfo.filename} from {file} in {root}")
                                    zip_ref.extract(member=zipinfo, path=root)
                # Add the identifier to the set of unzipped folders
                unzipped_folders.add(identifier)
