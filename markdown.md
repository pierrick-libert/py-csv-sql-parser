# Markdown

The purpose of this file is to briefly explain how I decided to work on the project and the potential improvements I could implement.

## Technical Choice

I decided to go with Python since its scripting style and the possibility to type the code is a good match for this kind of project.
I chose to do not install pre-made framework to keep it as simple as possible.

I just added libraries to control the code quality and to facilitate the communication with the DB.

My implementation is very strict when it comes to typings with Python. Though it's definitely not mandatory with the language, I think that's a good practice to keep in order to ease the readability of the code.

## Solution

My solution is pretty straightforward as explained below.

### Specification files

I simply loop on the `specs` folder and handle cases as follow:

 * I check the number of columns in the file
 * I check the `width` column is a positive integer
 * I check the `datatype` column and choose the best SQL type

If all the checks above are alrght, I create the table and proceed to the next step described in `Data files`.
Otherwise I throw an error, print it in the terminal with accurate information and move to the next file without looking at the `data` files.

### Data files

Using the name of the file retrieved in `Specification files`, I filter the files in the `data` folder and parse them as follow:

 * I check value validity based on the specification file

Everytime one of the value is incorrect, I will store it inside an array and print it in the terminal with accurate information. No data from the file would be inserted to avoid duplicated values when you re-launch the program for this file.
If all data are correct, I insert them in DB

### Migration table

I created a migration table to keep a history of the file already inserted in DB.
The check is made during the `Data files` step.
If the file has already been inserted, I print an information message and move to the next file.
Otherwise the `Data files` step is triggered and, if everything went well, I insert a new line in the migration table with the filename.

## Improvements

Numerous improvements could be set up in this project.

 * Targeting a special file or file pattern when launching the program
 * Adding `Date` and `Datetime` columns to the imported table to store the insertion time but also the date in the filename
 * A better configuration to be able to change folders the program is looking into
 * Improve the unit test
