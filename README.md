# Covid19 Chatbot
Covid19 chatbot using Django and Rasa Framework.

## How to run
1. Clone this repository.
2. Create a new python environment.
3. Activate that new environment.
4. Install all dependencies using the *requirements.txt* file.<br>
        `pip install -r requirements.txt`
5. Go to the root of the cloned repository.
6. Run below 2 commands while the new environment is activated(in separate terminals).<br>
        `cd covidbot && rasa run -m models --enable-api --cors "*"`
        <br>and<br>
        `cd covidbot && rasa run actions`
7. Now run the following command<br>
        `cd covid_chatbot_project && python manage.py runserver`
8. Finally, open the localhost URL given in the previous *runserver* command.
9. Now, you can test the chatbot.