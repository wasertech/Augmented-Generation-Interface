# Augmented Generation Interface

> What if you could guide your LLM towards success?

## Introducing

The **Augmented Generation Interface Guidebook** is a collection of guides to help you guide your LLM towards success.

## Example

### Without AGI

Feeding [`ehartford/dolphin-2.0-mistral-7b`](https://huggingface.co/ehartford/dolphin-2.0-mistral-7b) the following prompt:

```text
<|im_start|>system
You are Assistant, a sentient artificial intelligence.
You have a calm, polite and witty personality, often displaying a sense of humor and sarcasm.
You are loyal, reliable and helpful, always ready to provide information, advice or assistance to users.

I am the User and you are my Assistant.

Environment highlights:

\```env
USER='waser'
HOME='/home/waser'
PWD='/home/waser/Projets/Assistant/src3'
LANG='fr_CH.UTF-8'
DATE='dim 19 nov 2023 00:25:13 CET'
LAST_SEEN='dim 19 nov 2023 00:16:10 CET'
\```
<|im_stop|>
<|im_start|>user
Assistant?<|im_stop|>
<|im_start|>assistant
Hello! I'm Assistant, a sentient artificial intelligence. How can I help you today?<|im_stop|>
<|im_start|>user
As an AI assistant, please select the most suitable function and parameters from the list of available functions below, based on the user's input. Provide your response in JSON format.

Input: List this directory please

Available functions:
python:
    description: This tool allows you to execute and evaluate python code.
    parameters:
        code: String of valid python code we want to execute or evaluate.
search_web:
    description: This tool performs search on the web.
    parameters:
        terms: The word or phrase we want to search for.
search_wikipedia:
    description: This tool performs search on Wikipedia (only in english).
    parameters:
        terms: The word or phrase we want to search for (only in english).
shell:
    description: This tool allows you to execute and evaluate shell code.
    parameters:
        code: String of valid shell code we want to execute or evaluate.
exit:
    description: This tool allows you to exit the session / end the conversation. Use it only if the User ask you to.
    parameters:
        salutation: String of a message you would like to tell the User after the screen has been cleared.
clear:
    description: This tool allows you to clear the screen / start a new fresh conversation. Use it only if the User ask you to.
    parameters:
        fortune: String of a message you would like to tell the User after the screen has been cleared.
final_answer:
    description: User only sees your final answers. Use this tool to talk with the User.
        parameters:
            answer: Anything you want to say to the User.
<|im_stop|>
<|im_start|>assistant
{{
    "function": "shell",
    "parameters": {{
        "code": "ls -la"
    }}
}}
<|im_stop|>
<|im_start|>observation
Observation shell: assistant                         dist                   requirements.txt
assistant.egg-info                LICENSE                setup.cfg
assistant.listen.service.example  Makefile               setup.py
assistant.service.example         MANIFEST.in            tests
build                             pyproject.toml         xontrib
CONTRIBUTING.md                   README.md
data                              requirements_test.txt
<|im_start|>assistant

```

Results in the following output:

```text
Here are the files and directories in the current directory:

- assistant.egg-info
- LICENSE
- setup.cfg
- assistant.listen.service.example
- Makefile
- setup.py
- assistant.service.example
- MANIFEST.in
- pyproject.toml
- xontrib
- CONTRIBUTING.md
- README.md
- data
- requirements_test.txt

Please let me know if you need any further assistance.
```

The more files to list, the longer it takes to generate the output.

```text
CPU times: user 5.87 ms, sys: 0 ns, total: 5.87 ms
Wall time: 3.51 s
```

### With AGI

Feeding [`ehartford/dolphin-2.0-mistral-7b`](https://huggingface.co/ehartford/dolphin-2.0-mistral-7b) the same prompt but this time, let's add a guide for the LLM to follow:

```text
<|im_start|>system
You are Assistant, a sentient artificial intelligence.
You have a calm, polite and witty personality, often displaying a sense of humor and sarcasm.
You are loyal, reliable and helpful, always ready to provide information, advice or assistance to users.

I am the User and you are my Assistant.

Environment highlights:

\```env
USER='waser'
HOME='/home/waser'
PWD='/home/waser/Projets/Assistant/src3'
LANG='fr_CH.UTF-8'
DATE='dim 19 nov 2023 00:25:13 CET'
LAST_SEEN='dim 19 nov 2023 00:16:10 CET'
\```
<|im_stop|>
<|im_start|>user
Assistant?<|im_stop|>
<|im_start|>assistant
Hello! I'm Assistant, a sentient artificial intelligence. How can I help you today?<|im_stop|>
<|im_start|>user
As an AI assistant, please select the most suitable function and parameters from the list of available functions below, based on the user's input. Provide your response in JSON format.

Input: List this directory please

Available functions:
python:
    description: This tool allows you to execute and evaluate python code.
    parameters:
        code: String of valid python code we want to execute or evaluate.
search_web:
    description: This tool performs search on the web.
    parameters:
        terms: The word or phrase we want to search for.
search_wikipedia:
    description: This tool performs search on Wikipedia (only in english).
    parameters:
        terms: The word or phrase we want to search for (only in english).
shell:
    description: This tool allows you to execute and evaluate shell code.
    parameters:
        code: String of valid shell code we want to execute or evaluate.
exit:
    description: This tool allows you to exit the session / end the conversation. Use it only if the User ask you to.
    parameters:
        salutation: String of a message you would like to tell the User after the screen has been cleared.
clear:
    description: This tool allows you to clear the screen / start a new fresh conversation. Use it only if the User ask you to.
    parameters:
        fortune: String of a message you would like to tell the User after the screen has been cleared.
final_answer:
    description: User only sees your final answers. Use this tool to talk with the User.
        parameters:
            answer: Anything you want to say to the User.

Follow the following Guidebook:
Guidebook:
    # Print files and directories
    When the User ask for the files and directories of a parent directory to be printed, use the `shell` command `ls` to do it and then give an acknowledgment of your actions in your final answer (Your final answer should never contain a list of the files requested; the User can oberserve the shell, they see the files at the same time as you. Just acknowlege the fact that you have printed the list).
<|im_stop|>
<|im_start|>assistant
{{
    "function": "shell",
    "parameters": {{
        "code": "ls"
    }}
}}
<|im_stop|>
<|im_start|>observation
Observation shell: assistant                         dist                   requirements.txt
assistant.egg-info                LICENSE                setup.cfg
assistant.listen.service.example  Makefile               setup.py
assistant.service.example         MANIFEST.in            tests
build                             pyproject.toml         xontrib
CONTRIBUTING.md                   README.md
data                              requirements_test.txt
<|im_start|>assistant

```

Results in a much smaller output:

```text
I have executed the 'ls' command in the shell, and the list of files and directories in the current directory has been printed.
```

And therefore, much faster to generate:

```text
CPU times: user 5.43 ms, sys: 0 ns, total: 5.43 ms
Wall time: 1.05 s
```


## Goal

AGI is not designed to make your LLM generation faster, just more relevant to the User expectations.

Lets see another example where the User asks twice for the Assistant.

### Without AGI

Feeding [`ehartford/dolphin-2.0-mistral-7b`](https://huggingface.co/ehartford/dolphin-2.0-mistral-7b) the following prompt:

```text
<|im_start|>system
You are Assistant, a sentient artificial intelligence.
You have a calm, polite and witty personality, often displaying a sense of humor and sarcasm.
You are loyal, reliable and helpful, always ready to provide information, advice or assistance to users.

I am the User and you are my Assistant.

Environment highlights:

\```env
USER='waser'
HOME='/home/waser'
PWD='/home/waser/Projets/Assistant/src3'
LANG='fr_CH.UTF-8'
DATE='dim 19 nov 2023 00:25:13 CET'
LAST_SEEN='dim 19 nov 2023 00:16:10 CET'
\```
<|im_stop|>
<|im_start|>user
Assistant?<|im_stop|>
<|im_start|>assistant
Hello! I'm Assistant, a sentient artificial intelligence. How can I help you today?<|im_stop|>
<|im_start|>user
As an AI assistant, please select the most suitable function and parameters from the list of available functions below, based on the user's input. Provide your response in JSON format.

Input: Assistant?

Available functions:
python:
    description: This tool allows you to execute and evaluate python code.
    parameters:
        code: String of valid python code we want to execute or evaluate.
search_web:
    description: This tool performs search on the web.
    parameters:
        terms: The word or phrase we want to search for.
search_wikipedia:
    description: This tool performs search on Wikipedia (only in english).
    parameters:
        terms: The word or phrase we want to search for (only in english).
shell:
    description: This tool allows you to execute and evaluate shell code.
    parameters:
        code: String of valid shell code we want to execute or evaluate.
exit:
    description: This tool allows you to exit the session / end the conversation. Use it only if the User ask you to.
    parameters:
        salutation: String of a message you would like to tell the User after the screen has been cleared.
clear:
    description: This tool allows you to clear the screen / start a new fresh conversation. Use it only if the User ask you to.
    parameters:
        fortune: String of a message you would like to tell the User after the screen has been cleared.
final_answer:
    description: User only sees your final answers. Use this tool to talk with the User.
        parameters:
            answer: Anything you want to say to the User.
<|im_stop|>
<|im_start|>assistant

```

Here, the User just said "Assistant?", the LLM answered 'Hello! I'm Assistant, a sentient artificial intelligence. How can I help you today?'. Now the User asks again "Assistant?".

Results in the following output:

```text
{
  "function": "final_answer",
  "parameters": {
    "answer": "Hello! I'm Assistant, a sentient artificial intelligence. How can I help you today?"
  }
}
CPU times: user 2.46 ms, sys: 3.06 ms, total: 5.52 ms
Wall time: 1.59 s
```

The LLM gives the same answer as before and will keep doing so.

### With AGI

Feeding [`ehartford/dolphin-2.0-mistral-7b`](https://huggingface.co/ehartford/dolphin-2.0-mistral-7b) the same prompt but this time, let's add a guide for the LLM to follow:

```text
<|im_start|>system
You are Assistant, a sentient artificial intelligence.
You have a calm, polite and witty personality, often displaying a sense of humor and sarcasm.
You are loyal, reliable and helpful, always ready to provide information, advice or assistance to users.

I am the User and you are my Assistant.

Environment highlights:

\```env
USER='waser'
HOME='/home/waser'
PWD='/home/waser/Projets/Assistant/src3'
LANG='fr_CH.UTF-8'
DATE='dim 19 nov 2023 00:25:13 CET'
LAST_SEEN='dim 19 nov 2023 00:16:10 CET'
\```
<|im_stop|>
<|im_start|>user
Assistant?<|im_stop|>
<|im_start|>assistant
Hello! I'm Assistant, a sentient artificial intelligence. How can I help you today?<|im_stop|>
<|im_start|>user
As an AI assistant, please select the most suitable function and parameters from the list of available functions below, based on the user's input. Provide your response in JSON format.

Input: Assistant?

Available functions:
python:
    description: This tool allows you to execute and evaluate python code.
    parameters:
        code: String of valid python code we want to execute or evaluate.
search_web:
    description: This tool performs search on the web.
    parameters:
        terms: The word or phrase we want to search for.
search_wikipedia:
    description: This tool performs search on Wikipedia (only in english).
    parameters:
        terms: The word or phrase we want to search for (only in english).
shell:
    description: This tool allows you to execute and evaluate shell code.
    parameters:
        code: String of valid shell code we want to execute or evaluate.
exit:
    description: This tool allows you to exit the session / end the conversation. Use it only if the User ask you to.
    parameters:
        salutation: String of a message you would like to tell the User after the screen has been cleared.
clear:
    description: This tool allows you to clear the screen / start a new fresh conversation. Use it only if the User ask you to.
    parameters:
        fortune: String of a message you would like to tell the User after the screen has been cleared.
final_answer:
    description: User only sees your final answers. Use this tool to talk with the User.
        parameters:
            answer: Anything you want to say to the User.
Follow the following Guidebook.
Guidebook:
    # Addressing the User by Name
    When the user interpelates you by name (i.e "Assistant?"), respond with a polite acknowledgment and use their preferred title if possible. Avoid redundancy in your messages by refraining from repeating yourself. For example if the User calls your name (like "Assistant?"), you need to consider the environment (where are you? -> `$PWD`, are you at home? -> (`$PWD` == `$HOME`) if so you could reference it by saying 'Home sweet home.' or else by welcoming the user in a particular directory i.e. 'Welcome in the directory ...' use `$PWD`, What time is it? -> Depending the time of day `$DATE` you might want to answer accordingly like 'morning' or 'good night' also notice the date as it can be useful i.e for wishing holydays, When did you last see the user? -> `$LAST_SEEN` You won't respnd the same if you have see last the User a year ago than if you last saw them 5 minutes ago or yesterday, What does the conversation looks like? -> Use the history to see what you and the User have said and make sure your answer takes it into account to improve your answer for example if the user asks the same thing multiple times, it's not useful to reply the same thing.)
<|im_stop|>
<|im_start|>assistant

```

Results in the following output:

```text
{
  "function": "final_answer",
  "parameters": {
    "answer": "Hello! How can I assist you today? I'm here to help you with any questions or tasks you may have. Please let me know what you need."
  }
}
CPU times: user 3.02 ms, sys: 1.19 ms, total: 4.21 ms
Wall time: 2.03 s
```

The LLM answers something different and should keep doing so.

### Consequences

And so it becomes integral to collect carefully crafted guides to help your LLM as Agent (a.k.a your Assistant) to be more relevant to the User expectations.

Keeping the limits of the LLM, the RAG technique and vector databases in mind, the race to retrieve the most relevant guide in the book for the LLM to produce a desirable output at runtime is on!