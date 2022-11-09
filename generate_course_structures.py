import openai
import pandas as pd
import requests
import json


import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--openai_api_key', required=True, type= str)
parser.add_argument('--deepL_api_key', required=True, type= str)

parser.add_argument('--model_name', required=True, type= str, default="text-davinci-002")
parser.add_argument('--temperature', required=True, type= float, default=0.8)

parser.add_argument('--num_generations', required=True, type=int, default=1)

parser.add_argument('--file_output_name', required=True, type=str, default="course_structure_suggestion")


parser.add_argument('--course_name', required=True, type= str)
parser.add_argument('--description', required=True, type= str)
parser.add_argument('--target_group', required=True, type= str)
parser.add_argument('--learning_goals', required=True, type= str)
parser.add_argument('--num_modules', required=True, type=str, default="7")

args = parser.parse_args()


openai.api_key = args.openai_api_key


prompt="""Course name: Dog training online course
Description: Online course for dog owners, so that their dogs follow commands.
Target group: Dog owners
Learning goals: Dog owners should learn in this course how to train their dogs so that the dogs follow commands, don’t make any problems and also learn a few tricks.
Number of lesson modules: 10

Course structure:

1. motivation - why is training important?

2. understanding dog behaviour
- How does a dog think?
- Body language and vocabulary
- The importance of socialisation

3. classical conditioning
- S-R-S principle
- Training with positive reinforcement
- Training with negative reinforcement
- Everyday training

4. operant conditioning
- Reward and Punishment
- Training with reinforcers
- Training with punishment

5. learning through play
- Play as motivation
- Play as training
- Application in everyday life

6. tricks
- What are the tricks?
- Training the tricks
- Application in everyday situations

7. problem behaviour
- Causes of problem behaviour
- Behaviour as a problem
- Dealing with problem behaviour

8. training units
- Structuring the training sessions
- Planning the training programme
- Implementation of the training units

9. knowledge assessment
- Test questions
- Case studies
- Self-test

10. summary
- Repetition of the most important contents
- Questions and answers
- Suggestions for further training

Course name: How to Make 20.000 USD a Month on A Social Media Marketing Agency.
Description: Online course for marketers who want's to scale their business.
Target group: Marketers.
Learning goals: The fundamentals of how different social media platforms work, how to tell engaging stories in social media, and how to use psychometrics to create compelling marketing for different groups of people.
Number of lesson modules: 6

Course structure:

1. Introduction
- What is a social media marketing agency?
- The business model
- The benefits

2. The Fundamentals of Social Media
- How social media platforms work
- The different types of social media
- The benefits of social media

3. Telling Engaging Stories in Social Media
- What makes a good story?
- How to structure a story
- The different types of stories
- The benefits of telling stories in social media

4. Using Psychometrics in Social Media Marketing
- What are psychometrics?
- How to use psychometrics in social media marketing
- The benefits of using psychometrics

5. Creating Compelling Marketing for Different Groups of People
- How to segment your audience
- How to create marketing that resonates with different groups of people
- The benefits of creating compelling marketing

6. Conclusion
- Summary of the most important points
- Questions and answers
- Suggestions for further reading

Course name: ThinkIT Data Science Professional Certificate
Description: Online course to kickstart your career in data science & ML. Build data science skills, learn Python & SQL, analyze & visualize data, build machine learning models. No degree or prior experience required.
Target group: Programmers, IT students.
Learning goals: What data science is and what methodologies to use. The course teaches multiple languages and frameworks, and teaches how to create and analyze datasets, as well as apply different data science techniques and tools.
Number of lesson modules: 5

Course structure:

1. Introduction to Data Science
- What is data science?
- Data science methodology
- The different types of data

2. Python for Data Science
- Introduction to Python
- Your first python program
- Python for data analysis

3. Data Visualization
- The different types of data visualizations
- Tools for visualization
- How to create data visualizations

4. Machine Learning
- Overview of machine learning
- How machine learning models works
- How to build machine learning models

5. Summary
- Key takeaways
- Suggested next steps for landing a data science job
- Suggested additional learning resources
"""


def generate_course_structure(name, description, target_group, learning_goals, num_modules, language="EN"):

    if language != "EN":
      name, description, target_group, learning_goals = [translate("EN", language, item) for item in [name, description, target_group, learning_goals]]

    model_prompt = prompt + "\n" + "Course name: " + name.strip()
    model_prompt = model_prompt + "\n" + "Description: " + description.strip()
    model_prompt = model_prompt + "\n" + "Target group: " + target_group.strip()
    model_prompt = model_prompt + "\n" + "Learning goals: " + learning_goals.strip()
    model_prompt = model_prompt + "\n" + "Number of lesson modules: " + num_modules.strip()
    model_prompt = model_prompt + "\n" + "\nCourse structure:\n\n1."

    #print(model_prompt)
    #print()
    course_structure = openai.Completion.create(
    model=args.model_name,
    prompt=model_prompt,
    temperature=args.temperature,
    top_p=1,
    frequency_penalty=0,
    stop=["&&&","Course name:"],
    max_tokens=1000)


    course_structure = "1. " + course_structure["choices"][0]["text"].strip()

    if language != "EN":
        translate(language, "EN", course_structure)

    return course_structure


def translate(source_lang, target_lang, text):
    availableLanguagesDeepL=["EN","ES","ZH","FR","RU","PT-PT","DE","IT","NL","PL","JA","PT-BR","SV"]

    assert target_lang in availableLanguagesDeepL

    data = {
      'auth_key': "25627dda-19f9-9440-75f7-beb6eac01235",
      'text': text,
      'target_lang': target_lang,
    }

    if source_lang != None:
        if source_lang=="PT-PT" or source_lang == "PT-BR":
            sourceLang="PT"
        data["source_lang"]=source_lang

        assert source_lang in availableLanguagesDeepL

    if target_lang=="FR":
        data["formality"]="less"

    response = requests.post('https://api.deepl.com/v2/translate', data=data)

    json_data = json.loads(response.text)
    text=json_data["translations"][0]["text"]

    return text

for i in range(args.num_generations):
    course_structure = generate_course_structure(args.course_name, args.description, args.target_group, args.learning_goals, args.num_modules, language=args.language)
    
    with open(args.file_output_name + "_" + str(i) + ".xtx", "w") as text_file:
        text_file.write(course_structure)
