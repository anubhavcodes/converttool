# Data Pipeline Case-Study

This is a test project within trivago's technical recruiting process.

At trivago we maintain a big amount of hotel data.  
Imagine you need to write a tool that converts the data  
from one format to other formats.

This should **not** be a one-off script. Instead, imagine your team  
will need to maintain the tool and extend it to other formats.  
So, focus on code quality rather than performance.

## Requirements

Your program needs to fulfill the following requirements:

1. Read data from the given CSV file `hotels.csv`. The first line is a header
   which describes all field names.

2. Validate the data

   To keep it simple, let's go with the following rules:
   
   - A hotel name may only contain UTF-8 characters.
   - The hotel URL must be valid (please come up with a good definition of "valid").
   - Hotel ratings are given as a number from 0 to 5 stars. There may be no negative numbers.

3. Write the valid data in *two* of the following formats of your choice:  
   XML, JSON, YAML, HTML, SQLite Database, or your own custom format.  
   The output must be in the same directory as the input.

Feel free to choose any programming language, framework, libraries or existing tools you like.
The only constraint is that your tool needs to run on our local machine.  
A graphical user interface is not necessary.

## How we test your code

We will test your code on an x86-64 machine with the most recent unmodified
Debian stable release or the current Mac OSX - depending on your choice.

Please provide some information on how to execute your program. If it requires
any special parameters, please mention them as well. All optional libraries
should be either packaged with your code or easy to install with a package
manager. Of course you can also provide a Dockerfile if you like.

## Bonus tasks

If you find the time, here are some nice bonus ideas. All of them are **optional**.

* Make the tool extensible to new output formats
* We care more about code quality (readability, software architecture)
  than about performance - although fast execution is a plus.
* Unit tests would be nice
* Add options to sort/group the data before writing it

## Additional help

We understand that the task specification is pretty vague. This is intended.  
In case of doubt, try to come up with a sensible default and document your decisions.

## Legal notice

Please keep in mind that this case study is proprietary.  
That means that you are not allowed to share your code with anybody other than trivago.  
Especially you may not upload it to websites like Github or BitBucket. Please be fair.
