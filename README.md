# Where Should I Eat? - Backend
Hungry, but can't figure out a place nearby to eat? Craving something sweet? Spicy or mild? Pizza or sushi?  
Use the [WhereShouldIEat Chatbot](https://wheretoeat.vercel.app/) to help you decide!

## [Demo Video](https://youtu.be/Uac_E676KiQ)

## Collaborators
- Ryan Campbell
- Harry Lai
- Shulu Li
- Rishi Khare

## Factored Cognition Chatbot

- Ask a series of questions about proximity/location, occasion, price, etc.
- From responses, output one restaurant

## App workflow:

- App tells user an initial question: occasion/location preference/etc.
- User types in answer, hits enter
- User’s response is sent to OpenAI API, formatted with correct prompt
- Repeat: (factored cognition)
  - Chat gives user another question about their preference
  - User types response, hits enter
  - User’s response is sent to OpenAI API, formatted with correct prompt
- OpenAI generates search input to Google Maps API, then returns information to user
- possibly use OpenAI to refine input to Google Maps API, then return refined information to user

## Commands

### To install

```bash
pip install -r requirements.txt
```

### To Run Application

```bash
flask run
```
