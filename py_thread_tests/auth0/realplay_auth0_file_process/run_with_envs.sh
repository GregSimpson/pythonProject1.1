###    #!/bin/bash

export port='5432'
export host='ovpc1-pgsql03.clrygru5fh3l.us-west-2.rds.amazonaws.com'
export user='realplayuser'
export password='F35D6492-CC53-4F38-BA0C-DA8500D793C9'

# for the original db and schema
export database='realplay_dce1'
export db_schema_version='v1'

# for the V2 db and schema
#export database='realplay2_dce1'
#export db_schema_version='v2'

python database_bulk_update.py
#python filebased_userid_process.py

