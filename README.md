# Make Nullarbor reports machine readable

Nullarbor reports come out in beautiful HTML. But, sometimes we want them in
a format that we can easily load into a database, an `R` session, or pass
on to some other script.

In this program, we parse the information contained in a Nullarbor report
folder into a few keywords, which can then be formatted into anything by using
a `Jinja2` template.

In our own pipeline, we use it to translate the report into a `JSON` format
using a schema appropriate for our own LIMs system. But, the keywords could
be combined in any template to generate any time of file.

## Installation

`pip install ...`

## Dependencies

Click
Jinja2

## Inputs

The program takes three mandatory inputs:

1. A path to a Nullarbor `report` folder
2. A path to a Jinja2 template file
3. A path to a YAML configuration file

### The Jinja2 template file keywords

The program will create the following `keywords` that can be used in a Jinja2
template file:

* job_id --- a `string` with a job ID number (at MDU we use it to track jobs)
* mlst_sop_id --- a `string` the SOP number for MLST
* mlst_header --- a `list` with the headers of the MLST table:
    - ['Scheme','SequenceType','Allele', 'Allele', 'Quality']
* mlst_isolates --- a `list` of `dictionaries`, each `dictionary` represents
    the results for a single isolate:
    - Each dictionary has the following keys:
        * id --- the isolate ID
        * scheme --- the identified MLST scheme
        * alleles --- a `list` of alleles
        * quality --- a `string` (PASSED|FAILED|?|UNKNOWN)

Additional `keywords` will be added soon.

A template that outputs a `CSV` file with only the isolate id and quality would
look like this:

```
Isolate, Quality
{% for isolate in mlst_isolates %} {{ isolate.id }}, {{ isolate.quality}} {% endfor %}
```
### A YAML configuration file

The goal of the configuration file is to set some parameters that would be used
in every run. Currently, there are two sets of parameters that must be included
in the configuration file:

* sopid
* nullarbor_files

The `sopid` parameters refer to the IDs of individual SOPs. If not relevant to
you, just enter them with a blank.

The `nullarbor_files` parameters refer to the name of the output files within
the Nullarbor `report` folder that have the data of interest. This will allow
for future proofing, in case these files change names.

The current default config file looks like this:

```
sopid:
    mlst: MMS109

nullarbor_files:
    mlst: mlst.csv
```
Feel free to use it if you are **NOT** interested in SOP IDs.
