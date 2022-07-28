###    #!/bin/bash

export port='5432'
export host='ovpc1-pgsql03.clrygru5fh3l.us-west-2.rds.amazonaws.com'
export database='realplay_dce1'
export user='realplayuser'
export password='<not stored>'

python block_auth0_tenant.py

