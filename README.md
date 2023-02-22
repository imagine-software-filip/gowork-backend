# Getting Started with GoWork Backend

This project is using Python, Django, Django Rest Framework, and graphene
 - git clone [the link of the project/branch]
 - Create a new python virtualenv 
    * virtualenv env
    * [linux/mac] source venv/bin/activate
    * [windows] venv\Scripts\activate
    * pip install -r requirements.txt
 - After you instal the req in the venv open the directory that has the manage.py file
 - [terminal] python manage.py makemigrations (db)
 - [terminal] python manage.py migrate (db)
 - [terminal] python manage.py runserver

## How to get involved

Always clone the main branch. As soon as you clone the main branch create a new local branch.

e.g.
git checkout -b [name-of-the-branch]
 - The name of the branch has to start with the ticket number and be followed by the title of the ticket
 - After you are done with the ticket use the git add command and commited with a good message.
 - git push origin [name-of-the-branch]
 - On the GitHub website create a pull request from the branch and wait for the tests to run.
 - After the tests are successful, ping me to review it
 - If I approve it, merge it to the main branch

## Code Guidelines
https://daisy-halibut-056.notion.site/Code-Guidelines-f62cd43f725447259281141ff5b3bbe1
