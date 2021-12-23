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
    milli_date = datetime.utcnow().strftime('%A%d-%H:%M.%f')
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


def process_input_files(json_or_csv):
    # Getting the work directory (cwd)
    source_dir = parser.get('user-export-file', 'source')

    output_dir = Path('{}'.format(parser.get('user-export-file', 'output')))
    output_dir.mkdir(parents=True, exist_ok=True)

    src_extension = ".{}".format(json_or_csv)

    # r=root, d=directories, f = files
    for r, d, f in walklevel(source_dir,0):
       for file in f:
            #if file.endswith(".json"):
            if file.endswith(src_extension):
                full_path = os.path.join(r, file)
                file_root = os.path.splitext(file)[0]
                upload_filename = ("{}/{}{}".format(output_dir, file_root, '.csv'))

                logger.info('\tfull_path          : {}'.format(full_path))
                logger.info('\tsource_dir         : {}'.format(source_dir))
                logger.info('\tfile_root          : {}'.format(file_root))
                logger.info('\tupload_filename    : {}'.format(upload_filename))
                logger.info('\toutput_dir         : {}'.format(output_dir))

                if (src_extension == '.json'):
                    this_df = pd.read_json(full_path, lines=True)
                if (src_extension == '.csv'):
                    this_df = pd.read_csv(full_path)

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

    # either 'json' or 'csv'
    #process_input_files('json')
    process_input_files('csv')


