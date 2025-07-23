# comparer_.sys_with_.fboot
Project made by student while practising in company RTSoft. It helps to compare files generated when working with
assemblies of 4diac-IDE and 4diac-forte from [IT_Severstal](https://gitverse.ru/IT_Severstal).  
By using this you can see if something go wrong with .fboot while converting/sending.
The project is implemented as a console application that accepts several required input parameters.
## Installation
This project made with [Python 3.12.0](https://www.python.org/downloads/release/python-3120/) using only standard
libraries. That means that you only need to install python to get it work.

So firstly you must install Python 3.12.0 (wasn't tested with another versions) and add it into PATH.

After that open terminal go to path where you want this application to be installed and enter the command:  
```commandline
git clone https://github.com/DAKudryashev/rtsoft
```

Now, go to rtsoft/src to start work with application.
## Usage

When you get to rtsoft/src you can start using application by typing in terminal:
```commandline
python main.py
```
You must specify two parameters in any order: -f/--fboot path/to/.fboot/file and -s/--sys path/to/.sys/file.  
Example:
```commandline
python main.py -s D:\projects\rtsoft\project_examples\IncorrectParserTest2\IncorrectParserTest2.sys -f D:\projects\rtsoft\project_examples\IncorrectParserTest2\IncorrectParserTest2_FORTE_PC.fboot
```
If you forget how to use this application you can always type:
```commandline
python main.py -h
```
You can type -v/--verbose to start application in detailed description mode.  
Example:
```commandline
python main.py -s D:\projects\rtsoft\project_examples\IncorrectParserTest2\IncorrectParserTest2.sys -f D:\projects\rtsoft\project_examples\IncorrectParserTest2\IncorrectParserTest2_FORTE_PC.fboot -v
```
Try projects in project_example directory to see how does it work.