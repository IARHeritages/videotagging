# videotagging
Crowdsourcing application to ag video content relevant to IARH 

First you will need to install all the dependencies with the following commands (be sure that you are in the project folder videotagging):

```bash

virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

This process will create a virtual environment for hosting all the PYBOSSA required libraries. This will be in a folder named **env** and each time you need to use them, you will have to activate it with the second command (source env/bin/activate).

# Creating the project

In order to create the project in a PYBOSSA server, you have to run the following command:

```
pbs --credentials micropasts create_project
```

**WARNING**: Be sure to have your virtualenv active. Use the source command, when you need it.


**NOTE**: In order to use your credentials, create a file in your home folder named .pybossa.cfg and add there a section like this:

```
[micropasts]
server: http://crowdsourced.micropasts.org
apikey: yourkey

```

## Updating the project

The previous section created the project, but none of the sections like the template, tutorial, long description or result pages have been populated. To do it, just run the following command:

```
pbs --credentials micropasts update_project
```

While this will work every time you run it, you can save a lot of time by telling pbs to watch for changes in any of those files, so it automatically updates the project for you when you save new changes to any of these files:

*  template.html
*  tutorial.html
*  results.html
*  long_description.md

```
pbs --credentials micropasts update_project --watch
```

## Adding tasks to the project from a JSON file

First of all, we would to run the command **create_json_video.py** as it will allow us to search in Youtube for anything, and create a JSON file that we will use later on for creating the tasks.

For using the script, you will need an API key from Google. Go to your Google API Console and create a key. Then, copy it, and paste it in the file settings.py, in the section GOOGLE_APIKEY. 

**NOTE**: There's a template of the settings file named settings.py.tmpl. Just make a copy of this file, rename it to *settings.py* and update its content with your API key.

**WARNING**: Be sure that you have enabled the API KEY to use the Youtube API. Go to your Library within the Google API Console, and enable it.

The previous command can be run like this:

```
python create_json_video.py --query="your query keywords" --output=videos.json

```

The **--output=filename.json** flag allows you to save your query into different files. If you don't use the flag, it will be saved to **videos.json**.

You can see all the available options by using the flag **--help**.

This will create a file with several videos. Be careful, as some searches could be very big.


Then, you can use the command line tool to import a the JSON file with tasks for your project:

```
pbs --credentials micropasts add_tasks --tasks-file=videos.json --tasks-type=json

```

**NOTE**: You can configure the priority and redundancy also, using the command line, check the help.
