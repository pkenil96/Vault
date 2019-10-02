import os
import sys
import boto3
import hashlib
from botocore.exceptions import NoCredentialsError


def upload_single_file_to_s3(filepath, targetName):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket('securebox.backup').upload_file(filepath, targetName)
        return 0
    except FileNotFoundError:
        print('Something went wrong:: {}'.format(filepath))
        return -1
    except NoCredentialsError as e:
        print('Something went wrong:: {}'.format(str(e)))
        return -1
    except Exception as e:
        print('Something went wrong:: {}'.format(str(e)))


def get_existing_file_hash():
    s3_cli = boto3.client('s3')
    try:
        response = s3_cli.list_objects_v2(Bucket='securebox.backup')
        objects_metadata = response['Contents']
        etags_list = list()
        for obj in objects_metadata:
            etags_list.append(obj['ETag'].strip('"'))
        return etags_list
    except Exception as e:
        print('Something went wrong:: {}'.format(str(e)))


def check_for_duplicate_files(filepath):
    try:
        existing_hashes = get_existing_file_hash()
        if filepath in existing_hashes:
            return True
        return False
    except FileNotFoundError as e:
        print('Something went wrong:: {}'.format(str(e)))


def sync_folder_bucket():
    UPLOADED, FAILED, ALREADY_EXISTS = 0, 0, 0
    try:
        os.chdir(BACKUP_FOLDER_PATH)
        print('\nBacking up files from: [{}]\n'.format(os.getcwd()))
        all_files = os.listdir('.')
        for _file_ in all_files:
            if os.path.isfile(_file_):
                if calculate_hash(_file_) in get_existing_file_hash():
                    print('ALREADY EXISTS: [{}]'.format(_file_))
                    ALREADY_EXISTS += 1
                elif upload_single_file_to_s3(_file_, str(_file_)) == 0:
                    print('UPLOADED: [{}]'.format(str(_file_)))
                    UPLOADED += 1
                else:
                    print('FAILED [{}].'.format(str(_file_)))
                    FAILED += 1
        return UPLOADED, FAILED, ALREADY_EXISTS
    except FileNotFoundError as e:
        print('Something went wrong:: {}'.format(str(e)))
        sys.exit(-1)


def calculate_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            hasher.update(f.read())
            return hasher.hexdigest()
    except FileNotFoundError as e:
        print('Something went wrong:: {}'.format(str(e)))


if __name__ == '__main__':

    os.system('cls||clear')
    print('\nUsage:')
    print('\nFor backup --> python3 backup.py <Folder location>')
    print('For update --> python3 update.py')

    if len(sys.argv) < 2:
        print('To run backup, specify the folder location')
        sys.exit()
    if len(sys.argv) > 2:
        print('Supplied more than 2 arguments: Ignoring the extra arguments')

    # path of the backup folder
    BACKUP_FOLDER_PATH = sys.argv[1]

    up, fail, dup = sync_folder_bucket()
    print('\n*******SUMMARY*******')
    print('UPLOADS: {}'.format(up))
    print('FAILED: {}'.format(fail))
    print('DUPLICATES: {}'.format(dup))
    print('***********************\n')
