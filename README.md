# join-form-submitter

```
$ python main.py --help
usage: join-form-submitter [-h] [--real] --file FILE (--splinter | --api)

Submits the join form at https://www.nycmesh.net/es/join

options:
  -h, --help   show this help message and exit
  --real
  --file FILE
  --splinter
  --api

Contact Willard for help
```

# Usage

Requires firefox.

```
pip install -r requirements.txt
python main.py --splinter --file requests.csv
```
