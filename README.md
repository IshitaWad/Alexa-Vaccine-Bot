## Inspiration
The  inspiration for this bot came from the ever growing demand of individuals needing to book vaccine shots to stay protected against COVID-19. As has been seen in the past few weeks, booking appointments has become a long and tedious process as individuals are struggling to find available vaccine slots in their area. This bot was inspired with the idea of making it easier to book a vaccine by automating the process of checking for available vaccine slots.

## What it does
The bot makes use of the voice-assistant Alexa to notify you when slots are available. It works by first requiring you to give Alexa your city location, which can be voice activated by the command "Alexa, find my vaccine". Once Alexa receives your location, it sets up an automatic process by which it continuously checks for available slots every 15 minutes. When Alexa finds empty booking slots available in the individual's region, it responds back with the address, the type of vaccine dose available (first, second, third), the brand of vaccine available, and the eligible age group. The individual is then able to log onto the website of the vaccine clinic and book an appointment directly. This process is significantly easier for the individual as with the Alexa Vaccine Bot they don't have to sign up for dozens of vaccine waitlists.

## How we built it
The project utilizes data from Verto API, which is an API service that checks for vaccine slots at all registered clinics in the area. The API service updates with new information every 15 minutes, and that is then passed onto Alexa so that it is able to look for available vaccine slots.

### You can view the Devpost for the project here: https://devpost.com/software/alexa-vaccine-bot
