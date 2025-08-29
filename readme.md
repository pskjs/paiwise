# Pairwise Test Generator

This project provides a small utility for generating pairwise combinations of
parameter values.

## Usage

Run the script and enter parameters when prompted.  Type `done` when you have
finished entering parameters and their values:

```
python pairwise.py
Parameter name (or 'done' to finish): size
Values for size (comma-separated): small,large
Parameter name (or 'done' to finish): color
Values for color (comma-separated): red,blue
Parameter name (or 'done' to finish): done
{"size": "small", "color": "red"}
{"size": "small", "color": "blue"}
{"size": "large", "color": "red"}
{"size": "large", "color": "blue"}
```

Each line of output is a JSON object representing one test case.

## Testing

Execute the test suite with:

```
python -m pytest -q
```

