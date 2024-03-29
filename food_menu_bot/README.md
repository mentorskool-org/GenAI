# Food Menu Chatbot Project

## What's This Project All About?

This project introduces a simple yet interactive chatbot designed to navigate through a food menu based on user-selected cuisines. The bot streamlines the decision-making process for users by presenting a series of choices, starting from cuisine selection to showcasing specific food items from chosen restaurants. Each step in the process is dependent on the user's previous choice, creating a seamless and personalized browsing experience.

## How Does It Work?

The chatbot uses a chained logic model, where each user action triggers the next step in the sequence:
1. **Cuisine Selection**: Users are first presented with a dropdown menu to choose a cuisine (e.g., Indian, American).
2. **Restaurant Name Generation**: Based on the selected cuisine, the bot generates the name of restaurant.
3. **Food Items Display**: Once a restaurant name is generated, the bot displays a list of available food items from that restaurant.

These actions are hardcoded into a sequence and combined using an LLM (Large Language Model) chain, ensuring that each action logically follows from the previous one.

## Why Is This Important?

This project showcases the practical application of chained actions in a conversational AI interface, offering an intuitive and efficient way for users to navigate through complex choices. It's a step towards making AI more interactive and user-friendly, with potential applications in various domains such as e-commerce, online booking, and customer service.

## Tasks You'll Do

### Common tasks performed:
- Implementing a user-friendly interface for cuisine selection.
- Hardcoding the logic for generating restaurant names based on cuisine.
- Using the LLM Chain to hardcode the steps that should be performed, one after another

## Skills You'll Learn

### Concepts:
- **LLM Chain**: Understanding how to chain together a series of dependent actions within a chatbot framework to create a fluid user experience.
- **User Interface Design**: Learning the basics of creating intuitive and responsive user interfaces for chatbots.
- **Data Management**: Gaining insights into organizing and structuring data (cuisines, restaurants, food items) in a way that can be efficiently retrieved and displayed by the chatbot.
- **Modular Programming**: Developing skills in modularizing chatbot functionalities, making the codebase more manageable and scalable.

By completing this project, participants will not only learn about the technical aspects of building a conversational AI but also appreciate the importance of user experience design in developing interactive applications. This foundation will be invaluable for those looking to explore more advanced projects in the future.