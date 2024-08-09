import json
import re
from typing import Any

SUGGESTED_QUESTIONS_AFTER_ANSWER_INSTRUCTION_PROMPT = (
    "Please help me predict the three most likely questions that human would ask, note that the recommended questions you provide should be questions the user or human might ask, not questions to ask the user or human. It is crucial to ensure their accuracy; otherwise, the recommended questions may appear ridiculous, severely affecting the experience of user or human ."
    "and keeping each question under 20 characters.\n"
    "Do not repeat questions that the user has already asked.\n"
    "MAKE SURE your output is the SAME language as the Assistant's latest response(if the main response is written in Chinese, then the language of your output must be using Chinese.)!\n"
    "The output must be an array in JSON format following the specified schema:\n"
    "[\"question1\",\"question2\",\"question3\"]\n"
)

class SuggestedQuestionsAfterAnswerOutputParser:

    def get_format_instructions(self) -> str:
        return SUGGESTED_QUESTIONS_AFTER_ANSWER_INSTRUCTION_PROMPT

    def parse(self, text: str) -> Any:
        action_match = re.search(r"\[.*?\]", text.strip(), re.DOTALL)
        if action_match is not None:
            json_obj = json.loads(action_match.group(0).strip())
        else:
            json_obj= []
            print(f"Could not parse LLM output: {text}")

        return json_obj
