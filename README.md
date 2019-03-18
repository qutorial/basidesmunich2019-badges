# Installation

Please, install the tools first:

```
sudo apt-get install python3 imagemagick inkscape evince
```

Install PDFtk

```
sudo apt-get install pdftk
```

Or, on Ubuntu 18.04 and newer:

```
sudo snap install pdftk
```


# Usage

## Step 1

Compose the CSV file as people.csv shows with people, companies and roles.



## Step 2

Then run the `ProduceBadges.py -h`:

```
usage: ProduceBadges.py [-h] [--csv CSV] [--svg SVG] [--outdir OUTDIR]

optional arguments:
  -h, --help       show this help message and exit
  --csv CSV        The CSV file with people names
  --svg SVG        The SVG file with badge template
  --outdir OUTDIR  The output directory, will be created
```

By default it will take the people.csv, the badge-bsides2019-template.svg
file as a template and will create an OUT-timestamp folder with SVGs.


## Step 3

Run inkscape to polish the SVGs the way the ProduceBadges script 
suggests.

```
inkscape OUT-DIR/*.svg
```

The start can take some RAM and time.

Don't forget to save the SVGs after the review and correction (if needed).


## Step 4

Run `CompilePdf.sh` to compile the SVGs into one large printable PDF file.


## Step 5

Open the file and print it. All of it or the necessary badge only.

