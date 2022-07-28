
## To install from that requirements.txt file
- pip install -r  /path/to/requirements.txt

### Requirements.txt was created by:
#### Local installed pkgs only
- pip freeze -l > requirements.txt

#### All pkgs that are installed
- pip freeze > requirements.txt



---------
# To setup and run
 - adjust your conf/settings.ini values for your env


 - in the appropriate dirs pointed to by :
> [user-export-file]
source:/home/gsimpson/gjs/realplay_user_exports
output:/home/gsimpson/gjs/realplay_user_exports/upload_files
output_prefix:postgres_upload_

> collect at least some of these files to run:
>> Auth0 export in source
>>> Generated upload in output

- pip -r  /path/to/requirements.txt
- python one_big_flyway_insert_file.py


----
> Here is a skeleton example of the settings.ini file
>>I left the parts that are not password or key related

> [Auth0Info]
>> url_get_token:/api/v2/","scope":"read:roles","grant_type":"client_credentials"}


> [Config_Data]
>> log_dir: logs
>> 
>> throttle_counter: 10
> >
>> throttle_sleep: 15


*** a section like this for every tenant
> [ttec-realplay-blueshield]
>> - RealPlay BOT - BlueShield
>> client_domain:ttec-realplay-blueshield.auth0.com
>>
>> client_id:
>>
>> client_secret:


> [ttec-ped-developers]
> - API Explorer Application
>> client_domain:ttec-ped-developers.auth0.com
>>
>> client_id:
>>
>> client_secret: 


> [ttec-realplay-parasol]
> - RealPlay BOT - Parasol
>> client_domain:ttec-realplay-parasol.auth0.com
>>
>> client_id:
>> 
>> client_secret:


> [user-export-file]
>> source:/home/gsimpson/gjs/realplay_user_exports
>>
>> output_orig:/home/gsimpson/gjs/realplay_user_exports/upload_files
>>
>> output:/home/gsimpson/gjs/git_stuff/RealPlay/database/postgres/Migrations/sql
>>
>> output_prefix:postgres_upload_
>>
>> output_single_file_orig:realplay_insert_stmts.sql
>>
>> output_single_file:V1.24.0_5__RP-997_one_big_insert_roles_file.sql

