# snowdog

In order to run SNOWdog, we'll need the following environment variables set:

```
LIMIT           :   Cap to the first N number of hosts. Set to 0 for unlimited or don't set.
DD_API_KEY      :   Your Datadog API Key
DD_APP_KEY      :   Your Datadog App Key
BASE_URL        :   The base of your SNOW url: ie. mysweetorg if your URL is mysweetorg.service-now.com
SNOW_USER       :   Your SNOW user with CMDB API Access
SNOW_PWD        :   Your SNOW password for above user
```

You can either set these environment variables and then run SNOWdog like this:

```
python snowdog.py
```

OR, set your variables in line like this:

```
LIMIT=5 DD_API_KEY=XYZ DD_APP_KEY=ABC BASEURL=mysweetorg SNOW_USER=admin SNOW_PWD=secret python snowdog.py
```

Great for a cron job or for that new intern that needs something to do!
