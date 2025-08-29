# Pairwise Test Generator

This repository contains a simple command line application that generates
pairwise test cases for a set of parameters.  The algorithm is implemented in
pure Python and works on Windows, macOS and Linux.

## Usage

1. Run the script with Python 3:
   ```bash
   python pairwise.py
   ```
2. Enter each parameter name followed by a comma separated list of its values.
   Type `done` when no more parameters should be added.
3. The resulting pairwise test cases are printed as comma separated values so
they can easily be copied into spreadsheet programs like Excel.  Use the
`-o`/`--output` option to save the table directly to a CSV file.

Example session:

```
$ python pairwise.py
Enter parameters for pairwise testing. Type 'done' when finished.

Parameter name (or 'done'): Browser
Values for 'Browser' separated by commas: Chrome,Firefox,Safari
Parameter name (or 'done'): OS
Values for 'OS' separated by commas: Windows,macOS,Linux
Parameter name (or 'done'): User Role
Values for 'User Role' separated by commas: Admin,Member,Guest
Parameter name (or 'done'): done
Browser,OS,User Role
Chrome,Windows,Admin
Firefox,macOS,Member
Safari,Linux,Guest
...
```

The produced output can be copied directly into Excel or stored as a CSV file
with `--output results.csv`.
