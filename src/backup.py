import os
import sys
import boto3
import argparse
import hashlib
from botocore.exceptions import NoCredentialsError


def upload_single_file_to_s3(filepath, targetName):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket('securebox.backup').upload_file(filepath, targetName)
        return 0 
    except FileNotFoundError:
        print('ERROR: File {} was not found'.format(filepath))
        return -1
    except NoCredentialsError:
        print('ERROR: AWS not configured properly')
        return -1

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
        print('ERROR: {}'.format(str(e)))

def check_for_duplicate_files(filepath):
    try:
        existing_hashes = get_existing_file_hash()
        if filepath in existing_hashes:
            return True
        return False
    except FileNotFoundError:
        print('ERROR: Folder not found')


def sync_folder_bucket():
    UPLOADED, FAILED, ALREADY_EXISTS = 0, 0, 0
    try:
        os.chdir(BACKUP_FOLDER_PATH)
        all_files = os.listdir('.')
        existing_file_hash = get_existing_file_hash()
        for _file_ in all_files:
            if os.path.isfile(_file_):
                if calculate_hash(_file_ ) in get_existing_file_hash():
                    print('[{}] already exists in bucket with a different name.'.format(_file_))
                    ALREADY_EXISTS+=1
                elif upload_single_file_to_s3(_file_, str(_file_)) == 0:
                    print('[{}] uploaded to the bucket.'.format(str(_file_)))
                    UPLOADED+=1
                else:
                    print('Failed to upload [{}].'.format(str(_file_)))
                    FAILED+=1
        return UPLOADED, FAILED, ALREADY_EXISTS
    except FileNotFoundError:
        print('ERROR: Folder not found')
        sys.exit(-1)

def calculate_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath,"rb") as f:
            hasher.update(f.read()) 
            return hasher.hexdigest()
    except FileNotFoundError:
        print('ERROR: Folder not found')


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('To run backup, specify the folder location')
        sys.exit()
    if len(sys.argv) > 2:
        print('Supplied more than 2 arguments: Ignoring the extra arguments')

    #path of the backup folder
    BACKUP_FOLDER_PATH = sys.argv[1]

    print('\nBacking up files from: [{}]\n'.format(BACKUP_FOLDER_PATH))
    up, fail, dup = sync_folder_bucket()
    print('\n*******SUMMARY*******')
    print('UPLOADS: {}'.format(up))
    print('FAILED: {}'.format(fail))
    print('DUPLICATES: {}'.format(dup))
    print('***********************\n')





