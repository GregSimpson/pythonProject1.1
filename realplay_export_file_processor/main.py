from pathlib import Path
from datetime import datetime
import logging.config
import os

import yaml
from flask import Flask
import configparser
import pandas as pd

def test_log_messages():
    logger.debug('test msg')
    logger.info('test msg')
    logger.warning('test msg')
    logger.error('test msg')
    logger.critical('test msg')

    logger.debug('setting test : {}'.format(parser.get('ttec-realplay-parasol', 'client_domain')))


def setup_logging():
    with open('./conf/logging.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def load_settings():
    # https://www.tutorialspoint.com/configuration-file-parser-in-python-configparser
    #parser = configparser.ConfigParser()
    parser.read('conf/settings.ini')
    for sect in parser.sections():
       logger.info('Section: {}'.format(sect))
       for k,v in parser.items(sect):
          logger.info(' {} = {}'.format(k,v))
       logger.info(' ')


def create_app():
    app = Flask(__name__)
    setup_logging()
    load_settings()

    return app


def call_auth0_for_role_data(user_name):
    # for now just make dummy data from milli-seconds
    logger.debug("\t\tI would call auth0 and pass : {}".format(user_name))
    milli_date = datetime.utcnow().strftime('%f')
    logger.debug("\treturning milli date : {} ".format(milli_date))

    return str(milli_date)


def process_this_df(this_df, upload_filename):
    with open(upload_filename,'w') as file_out:
        for index, row in this_df.iterrows():
            new_role = call_auth0_for_role_data(row['user_id'])
            logging.debug("writing {} :{},{},{}".format(upload_filename,row['user_id'], row['email'], new_role))
            file_out.write('\n{},{},{}'.format(row['user_id'], row['email'], new_role) )


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def process_csv_files(output_dir):
    # Getting the work directory (cwd)
    this_dir = parser.get('user-export-file', 'dir')

    new_directory = Path('{}/{}'.format(this_dir,output_dir))
    new_directory.mkdir(parents=True, exist_ok=True)

    # r=root, d=directories, f = files
    for r, d, f in walklevel(this_dir,0):
       for file in f:
            if file.endswith(".csv"):
                full_path = os.path.join(r, file)
                dir_name = os.path.dirname(r)
                file_name_with_ext = file
                file_root = os.path.splitext(file)[0]
                file_ext = os.path.splitext(file)[1]
                upload_filename = ("{}/{}{}{}".format(new_directory, "upload_", file_root, '.csv'))

                logger.info('\tfull_path          : {}'.format(full_path))
                logger.info('\tdir_name           : {}'.format(dir_name))
                logger.info('\tthis_dir           : {}'.format(this_dir))
                logger.info('\tfile_name_with_ext : {}'.format(file_name_with_ext))
                logger.info('\tfile_root          : {}'.format(file_root))
                logger.info('\tfile_ext           : {}'.format(file_ext))
                logger.info('\tupload_filename    : {}'.format(upload_filename))
                logger.info('\tnew_directory      : {}'.format(new_directory))

                this_df = pd.read_csv(full_path)
                logger.debug(this_df.info)
                logger.debug(this_df.style)

                # we now have a dataframe for this file
                #  loop over the rows - make a call to auth0/users to get the roles
                #  write the user_id,email, roles to a new file : $file_root + 'processed' + .json
                process_this_df(this_df, upload_filename)


def process_json_files(output_dir):
    # Getting the work directory (cwd)
    this_dir = parser.get('user-export-file', 'dir')

    new_directory = Path('{}/{}'.format(this_dir,output_dir))
    new_directory.mkdir(parents=True, exist_ok=True)

    # r=root, d=directories, f = files
    for r, d, f in walklevel(this_dir,0):
       for file in f:
            if file.endswith(".json"):
                full_path = os.path.join(r, file)
                dir_name = os.path.dirname(r)
                file_name_with_ext = file
                file_root = os.path.splitext(file)[0]
                file_ext = os.path.splitext(file)[1]
                upload_filename = ("{}/{}{}{}".format(new_directory, "upload_", file_root, '.csv'))

                logger.info('\tfull_path          : {}'.format(full_path))
                logger.info('\tdir_name           : {}'.format(dir_name))
                logger.info('\tthis_dir           : {}'.format(this_dir))
                logger.info('\tfile_name_with_ext : {}'.format(file_name_with_ext))
                logger.info('\tfile_root          : {}'.format(file_root))
                logger.info('\tfile_ext           : {}'.format(file_ext))
                logger.info('\tupload_filename    : {}'.format(upload_filename))

                this_df = pd.read_json(full_path, lines=True)
                logger.debug(this_df.info)
                logger.debug(this_df.style)

                # we now have a dataframe for this file
                #  loop over the rows - make a call to auth0/users to get the roles
                #  write the user_id,email, roles to a new file : $file_root + 'processed' + .json
                process_this_df(this_df, upload_filename)


if __name__ == '__main__':
    parser = configparser.ConfigParser()
    logger = logging.getLogger("RealplayExportProcess")
    create_app()

    test_log_messages()


    ## process csv files
    process_csv_files('upload_files_csv')

    # process json files
    process_json_files('upload_files_json')


