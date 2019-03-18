#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys


# log something
def msg(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def checkFileType(path, type):
  return type in "%s" % subprocess.check_output(["file", "%s" % path])

def main():

  # PREPARE AND CHECK FILE ARGUMENTS

  parser = argparse.ArgumentParser()
  parser.add_argument("--csv", help="The CSV file with people names")
  parser.add_argument("--svg", help="The SVG file with badge template")
  parser.add_argument("--outdir", help="The output directory, will be created")
  args = parser.parse_args()
  scriptDir = os.path.dirname(os.path.realpath(__file__))
  if args.csv is None:
    args.csv = os.path.join(scriptDir, "people.csv")

  if args.svg is None:
    args.svg = os.path.join(scriptDir, "badge-bsides2019-template.svg")

  if not checkFileType(args.csv, "Unicode text"):
    msg("The provided file %s is not in unicode CSV format, please, check it." % args.csv)
    exit(1)

  if not checkFileType(args.svg, "SVG Scalable Vector Graphics"):
    msg("The provided file %s is not in SVG format." % args.svg)
    exit(2)

  if args.outdir is None:
    import datetime
    now = datetime.datetime.now()
    args.outdir="OUT-%02d.%02d.%04d-%02d:%02d:%02d" % (now.month, now.day, now.year, now.hour, now.minute, now.second)
    args.outdir = os.path.join(scriptDir, args.outdir)

  if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

  if not os.path.isdir(args.outdir):
    msg("Had trouble creating output directory: %s" % args.outdir)
    exit(3)
  else:
    msg("Saving results into %s" % args.outdir)


  # READ THE TEMPLATE SVG AND CHECK IT

  template = ""
  with open(args.svg, 'r') as svgfile:
    template = svgfile.read()

  if len(template) == 0:
    msg("Could not read the template SVG")
    exit(4)

  if not "MAX MUSTERMANN" in template or not "firma gmbh" in template or not "ROLE" in template:
    msg("The template SVG has to contain 'MAX MUSTERMANN', 'firma gmbh' and 'ROLE' placeholders")
    exit(5)

  # READ THE CSV, CREATE FILES

  with open(args.csv) as csvfile:
    import csv
    csvreader = csv.reader(csvfile)
    for person in csvreader:
      # skip the table header if present
      if "Company, Person’s name, Person’s role" == ", ".join(person):
        continue
      (company, name, role) = ('', '', '')

      try:
        company = person[0]
      except:
        msg("Got an empty line in the CSV")
        continue

      try:
        name = person[1]
      except:
        msg("Could not parse the CSV line, %s" % " | ".join(person))
        continue

      try:
        role = person[2]
      except:
        msg("No specified role for %s" % name)

      msg("Making badge for %s" % name)

      import tempfile
      # filename of a name of the person
      filename = "BadgeFor"+"".join(char for char in name if char.isalpha())
      outfile = tempfile.NamedTemporaryFile(mode='w', suffix='.svg',
                              prefix=filename+"-", dir=args.outdir, delete=False)
      with outfile as outf:
        content = template.replace("MAX MUSTERMANN", name.upper())
        content = content.replace("firma gmbh", company.lower())
        content = content.replace("ROLE", role.upper())
        outf.write(content)

  msg("""Done. Please, review and polish the badges with
           \n inkscape %s/*.svg \n
         and run ProducePdf.sh then.""" % args.outdir)


if __name__ == '__main__':
  main()

