# Make Nullarbor reports machine readable

[Nullarbor](https://github.com/tseemann/nullarbor) reports come out in beautiful HTML.
But, sometimes we want them in a format that we can easily load into a database,
an `R` session, or pass on to some other script.

In this program, we parse the information contained in a Nullarbor report
folder into a few keywords, which can then be formatted into anything by using
a `Jinja2` template.

In our own pipeline, we use it to translate the report into a `JSON` format
using a schema appropriate for our own LIMs system. But, the keywords could
be combined in any template to generate any type of file.

## Installation

The easiest way of installing `nullarbor_translate` is using `pip`:

`pip install git+https://github.com/andersgs/nullarbor_translate.git`

Use the `--user` option to install locally:

`pip install --user git+https://github.com/andersgs/nullarbor_translate.git`

Use the `--install-option` to install the script in a particular location:

`pip install --install-option="--install-scripts=$HOME/bin" --user git+https://github.com/andersgs/nullarbor_translate.git`

Once installed type the following:

`nullarbor_translate --help`

## Dependencies

* [Click](http://click.pocoo.org/5/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/)
* [Pandas](http://pandas.pydata.org/)
* [PyYAML](http://pyyaml.org/)

## Inputs

The program takes three mandatory inputs:

1. A path to a Nullarbor `report` folder
2. A path to a Jinja2 template file
3. A path to a YAML configuration file

### The Jinja2 template file keywords

`Jinja2` provides for a very simple and powerful templating language. Read the
[Template Designer Documentation](http://jinja.pocoo.org/docs/dev/templates/) to
see what you can do.

What `nullarbor_translate` does is read the `Nullarbor` `reports` folder creating
`keywords` that you can use in your template. For now, the following `keywords`
can be used in a `Jinja2` template file:

* `job_id` --- a `string` with a job ID number (at MDU we use it to track jobs)
* `sop_id` --- a `dictionary` with SOP numbers defined in the `config file`.
    Here, the `key:value` pairs will be defined in the `config file`, and be
    available to the user as entered in the `config file`
* `mlst_header` --- a `list` with the headers of the MLST table:
    - ['Scheme','SequenceType','Allele', 'Allele', 'Quality']
* `mlst_isolates` --- a `list` of `dictionaries`, each `dictionary` represents
    the results for a single isolate:
    - Each dictionary has the following keys:
        * `id` --- the isolate ID
        * `scheme` --- the identified MLST scheme
        * `alleles` --- a `list` of alleles
        * `quality` --- a `string` (PASSED|FAILED|?|UNKNOWN)
* `resistome_isolates` --- a `list` of `dictionaries`, each `dictionary` represents
    the results for a single isolate:
    - Each dictionary has the following keys:
        * `id` --- the isolate ID
        * `n_genes` --- the number of AMR genes found
        * `results` --- a `list` of genes found (empty if no matches were found)
        * `partials` --- a `list` of genes with partial matches (empty if no partials were found)
* `newick` --- a `string` with the Newick tree
* `core_aln` --- a `list` of `dictionaries`, each `dictionary` represents the
    results for a single isolate:
    - Each dictionary has the following keys:
        * `id` --- the isolate ID
        * `seq` --- the sequence
* `reference` --- a `list` of `dictionaries`, each `dictionary` represents a
    single entry in the references `Genbank` or `FASTA` file (i.e., chromosomes,
        and plasmids).
        - Each dictionary has the following keys:
            * `id` --- the accession ID for the sequence
            * `length` --- the length of the sequence in base-pairs
            * `description` --- A description of the sequence, as obtained from
                the file
* `jobinfo` --- a `dictionary` with basic job information. It has the following
    keys:
        - `author` --- the login of the person that executed the job
        - `date` --- the date the job was executed
        - `isolates` --- the number of included isolates
        - `host` --- the host signature where in which the job was run
        - `folder` --- the location on the server where the job was run

Additional `keywords` will be added soon.

The template is given an object that contains all the `keywords`. To access a
`keyword` from the template, just type `nullarbor.<keyword>`. For instance,
to access `mlst_isolates`, just type `nullarbor.mlst_isolates`. This will
return an array that can be looped over.

A template that outputs a `CSV` file with only the `isolate id` and `quality`
columns of the `MLST` table would look like this:

```
Isolate, Quality
{% for isolate in nullarbor.mlst_isolates %} {{ isolate.id }}, {{ isolate.quality }} {% endfor %}
```
### A YAML configuration file

The goal of the configuration file is to set some parameters that would be used
in every run. The only requirement at this stage is `nullarbor_files` section,
which specifies the names of the `files` produces by `Nullarbor` for each
of the results of interest:

* nullarbor_files

An optional entry can specify the SOP IDs:

* sopid

The `sopid` parameters refer to the IDs of individual SOPs. The `keys` used here
will be available to you in your template as `sop_id.<key>`.

The current default config file looks like this:

```
nnullarbor_files:
    mlst: mlst.csv
    resistome: resistome.csv
    newick: tree.newick
    core_aln: core.aln

sopid:
    mlst: MMS109
    resistome: MMS118
    phylogenetics: MMS108
```

In this `config file` the SOP ID for `mlst` can be used in the template by using
the `keyword` `sop_id.mlst`.

## Example

```
cd /path/to/nullarbor/report
nullarbor_translate --template /path/to/my/template.json > nullarbor.json
```

## Getting help

```
nullarbor_translate --help
```

## References

Seemann, Torsten (2016). Nullarbor: Reads to report for public health and clinical microbiology. url: [https://github.com/tseemann/nullarbor](https://github.com/tseemann/nullarbor)
