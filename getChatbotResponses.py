from pyquery import PyQuery as pq
import json
import os
from os import listdir
from os.path import isfile, join

def GetClaudeQuestionsAndAnswers(data, path, model):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    result = {
        "model": model,
        "params": 0,
        "Qs&As": []
    }

    question_texts = []
    answer_texts = []

    for file in onlyfiles:
        print(file)
        with open(path + file, 'r', encoding='utf-8') as f:
            html_content = pq(f.read())
        
        questions = html_content('div.font-user-message')
        answers = html_content('div.font-claude-message')

        for q in questions.items(): question_texts.append(q.text())
        for a in answers.items(): answer_texts.append(a.text())

    if len(question_texts) == len(answer_texts):
        for x in range(len(question_texts)):
            temp = {
                'id':len(result['Qs&As']),
                'question' : data[x]['question'],
                'answer' : answer_texts[x][9:] if answer_texts[x].lower().startswith('atbilde:') else answer_texts[x],
                'gold' : data[x]['gold'],
                'RAG' : data[x]['RAG']
            }
            result['Qs&As'].append(temp)
    
    with open(f'ModelResponses/results_{model}.json', 'wt', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def GetGeminiQuestionsAndAnswers(data, path, model):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    result = {
        "model": model,
        "params": 0,
        "Qs&As": []
    }

    question_texts = []
    answer_texts = []

    for file in onlyfiles:
        print(file)
        with open(path + file, 'r', encoding='utf-8') as f:
            html_content = pq(f.read())
        
        questions = html_content('user-query')
        answers = html_content('model-response')

        for q in questions.items(): question_texts.append(q.text())
        for a in answers.items(): answer_texts.append(a.text())

    if len(question_texts) == len(answer_texts):
        for x in range(len(question_texts)):
            temp = {
                'id':len(result['Qs&As']),
                'question' : data[x]['question'],
                'answer' : answer_texts[x][9:] if answer_texts[x].lower().startswith('atbilde:') else answer_texts[x],
                'gold' : data[x]['gold'],
                'RAG' : data[x]['RAG']
            }
            result['Qs&As'].append(temp)
    
    with open(f'ModelResponses/results_{model}.json', 'wt', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def GetChatGptQuestionsAndAnswers(data, path, model):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    result = {
        "model": model,
        "params": 0,
        "Qs&As": []
    }

    question_texts = []
    answer_texts = []

    for file in onlyfiles:
        with open(path + file, 'r', encoding='utf-8') as f:
            html_content = pq(f.read())

        paragraphs = html_content('div.flex.max-w-full.flex-col.grow')

        question = True
        for p in paragraphs.items():
            if question: question_texts.append(p.text())
            else: 
                answer_elem = p('div.markdown')
                answer_text = ''
                for elem in answer_elem.children(':not(div)').items():
                    answer_text = answer_text + ' ' + elem.text() if answer_text != '' else elem.text()
                answer_texts.append(answer_text)
                    
            question = not(question)

    if len(question_texts) == len(answer_texts):
        for x in range(len(question_texts)):
            temp = {
                'id':len(result['Qs&As']),
                'question' : data[x]['question'],
                'answer' : answer_texts[x],
                'gold' : data[x]['gold'],
                'RAG' : data[x]['RAG']
            }
            result['Qs&As'].append(temp)
    
    with open(f'ModelResponses/results_{model}.json', 'wt', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)     

if __name__ == '__main__':
    # Need a file that has the JSON format and data.
    with open('template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)['Qs&As']

    GetClaudeQuestionsAndAnswers(data, 'ChatBotAnswers/Claude 3.7 Sonnet Answers/', 'Claude 3.7 Sonnet')
    GetChatGptQuestionsAndAnswers(data, 'ChatBotAnswers/ChatGPT-4o Answers/', 'GPT-4o')
    GetGeminiQuestionsAndAnswers(data, 'ChatBotAnswers/Gemini 2.0 Flash Answers/', 'Gemini 2.0 Flash')
