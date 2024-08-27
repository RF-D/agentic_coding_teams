import os
from unified import UnifiedApis
import asyncio
import subprocess
from termcolor import colored


class CoderTeam:
    def __init__(self):
        self.all_models = [
            UnifiedApis(
                name="Claude",
                provider="anthropic",
                model="claude-3-5-sonnet-20240620",
                use_async=True,
                print_color="yellow",
            ),
            UnifiedApis(
                name="GPT-4o",
                provider="openai",
                model="gpt-4o",
                use_async=True,
                print_color="magenta",
            ),
            UnifiedApis(
                name="Gemini",
                provider="openrouter",
                model="google/gemini-pro-1.5",
                use_async=True,
                print_color="cyan",
            ),
            UnifiedApis(
                name="DeepSeek",
                provider="openrouter",
                model="deepseek/deepseek-coder",
                use_async=True,
                print_color="green",
            ),
        ]
        self.models = []
        self.coder = UnifiedApis(
            name="Sonnet-Coder",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
        )
        self.error_corrector = UnifiedApis(
            name="ErrorFixer",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
        )
        self.code_improver = UnifiedApis(
            name="CodeEnhancer",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
        )

    def select_models(self):
        print(colored("Available models:", "cyan"))
        for i, model in enumerate(self.all_models, 1):
            print(colored(f"{i}. {model.name}", model.print_color))
        print(
            colored(
                "Enter the numbers of the models you want to use for planning (comma-separated), 'all' for all models, or 'none' to skip planning:",
                "yellow",
            )
        )
        selection = input().strip().lower()
        if selection == "all":
            self.models = self.all_models
        elif selection == "none":
            self.models = []
        else:
            try:
                indices = [int(i) - 1 for i in selection.split(",")]
                self.models = [
                    self.all_models[i] for i in indices if 0 <= i < len(self.all_models)
                ]
            except ValueError:
                print(colored("Invalid input. Using all models by default.", "red"))
                self.models = self.all_models

    async def get_full_response(self, agent, prompt, max_attempts=2):
        message_history = agent.history
        if len(message_history) > 0 and message_history[0]["role"] != "user":
            message_history.insert(0, {"role": "user", "content": "..."})
        full_response = ""
        for attempt in range(max_attempts):
            response = await agent.chat_async(prompt)
            if "</code>" in response:
                return response
            else:
                print(colored("code output got cutoff", "red"))

        return response

    async def discuss_project(
        self, project_description, iterations, independent_first_round
    ):
        if not self.models:
            print(
                colored(
                    "Skipping project discussion as no models were selected.", "yellow"
                )
            )
            return ""
        discussion = []
        for i in range(iterations):
            print(colored(f"\nIteration {i+1}/{iterations}", "cyan"))
            round_responses = []
            if i == 0 and independent_first_round:
                print(colored("First iteration: Models respond independently", "blue"))
                tasks = [
                    model.chat_async(
                        f"Please brainstorm and plan the following project to implement all user requests. Do not use or refer to any external files in the code unless explicitly told to do so by the user.we do not need unit tests and error handling and information printing should be handled by print statements and not by logging. Do not write out the entire application but provide logic, design, architecture and pseudo code inspirations. we also dont need marketing and other considerations like that. Be very critical and strive to eliminate errors and missing features.: {project_description}"
                    )
                    for model in self.models
                ]
                responses = await asyncio.gather(*tasks)
                for model, response in zip(self.models, responses):
                    round_responses.append(f"{model.name}: {response}")

            else:
                for model in self.models:
                    print(colored("Models will consider full discussion", "blue"))
                    full_discussion = "\n".join(discussion)
                    round_responses_text = "\n".join(round_responses)
                    response = await model.chat_async(
                        f"Discuss the following project, taking into account the previous discussion. Be critical and strive to improve the project and remove any errors. we do not need unit tests and error handling and information printing should be handled by print statements and not by logging. Do not write out the entire application but provide logic, design, architecture and pseudo code inspirations. we also dont need marketing and other considerations like that. Be very critical and strive to eliminate errors and missing features. Do not use or refer to to any external files unless explicitly told to do so by the user. Only focus on the code and logic of the app itself:\n\nProject: {project_description}\n\nCurrent round's responses:\n{round_responses_text}\n\nPrevious discussion:\n{full_discussion}"
                    )
                    round_responses.append(f"{model.name}: {response}")
                discussion.extend(round_responses)
        return "\n".join(discussion)

    async def generate_code(self, project_description, discussion, file_path):
        print(colored("\nGenerating initial code...", "blue"))
        system_message = "You are an expert programmer. Generate code based on the project description and team discussion. Consider all aspects of the app that is discussed and use the best provided suggestions to implement all suggested features. Do not skip over features. we do not need unit tests and error handling and information printing should be handled by print statements and not by logging. Do not use or refer to to any external files unless explicitly told to do so by the user. Wrap the code in <code> full code here </code> tags. return the full code as for a single file"
        self.coder.set_system_message(system_message)
        code_response = await self.get_full_response(
            self.coder,
            f"Project: {project_description}\n\nTeam Discussion:\n{discussion}\n\nGenerate the code for this project.",
        )

        code = code_response.split("<code>")[1].split("</code>")[0].strip()
        with open(file_path, "w") as f:
            f.write(code)
        print(colored(f"Initial code written to {file_path}", "green"))
        return code

    async def error_correction_cycle(self, file_path):
        system_message = "You are an expert programmer tasked with fixing errors in code. Analyze the error message and the code, then provide the corrected full code wrapped in <code> tags."
        self.error_corrector.set_system_message(system_message)

        while True:
            print(colored("\nExecuting code...", "cyan"))
            try:
                result = subprocess.run(
                    ["python", file_path], capture_output=True, text=True, check=True
                )
                print(colored("Code execution successful!", "green"))
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr
                print(colored(f"Error detected: {error_message}", "red"))
                with open(file_path, "r") as f:
                    current_code = f.read()

                print(colored("Attempting to fix the error...", "yellow"))
                correction_prompt = f"Error message:\n{error_message}\n\nCurrent code:\n{current_code}\n\nPlease fix the error and provide the full corrected code. "
                corrected_code_response = await self.get_full_response(
                    self.error_corrector, correction_prompt
                )

                corrected_code = (
                    corrected_code_response.split("<code>")[1]
                    .split("</code>")[0]
                    .strip()
                )
                with open(file_path, "w") as f:
                    f.write(corrected_code)
                print(colored("Applied fix. Retrying execution...", "magenta"))

    async def feedback_improvement_cycle(self, file_path, user_feedback):
        system_message = "You are an expert programmer tasked with improving code based on user feedback and team suggestions. Analyze the feedback, suggestions, and current code, then provide the improved full code wrapped in <code> tags. Do not use to any external files unless explicitly told to do so by the user."
        self.code_improver.set_system_message(system_message)

        with open(file_path, "r") as f:
            current_code = f.read()

        print(colored("\nGathering improvement suggestions from the team...", "cyan"))
        tasks = [
            model.chat_async(
                f"User feedback: {user_feedback}\n\nCurrent code:\n{current_code}\n\nProvide a plan on how to best implement the changes asked by the user (do not write full code)."
            )
            for model in self.models
        ]
        suggestions = await asyncio.gather(*tasks)

        print(
            colored(
                "Generating improved code based on feedback and suggestions...",
                "yellow",
            )
        )
        improvement_prompt = f"User feedback: {user_feedback}\n\nTeam suggestions:\n{' '.join(suggestions)}\n\nCurrent code:\n{current_code}\n\nPlease improve the code based on the user feedback and the best elements from the team suggestions. Provide the full improved code."
        improved_code_response = await self.get_full_response(
            self.code_improver, improvement_prompt
        )

        improved_code = (
            improved_code_response.split("<code>")[1].split("</code>")[0].strip()
        )
        with open(file_path, "w") as f:
            f.write(improved_code)
        print(colored(f"Improved code written to {file_path}", "green"))

        # Run the code after improvement
        await self.error_correction_cycle(file_path)

    async def run_project(self):
        self.select_models()
        continue_from_file = (
            input(
                colored(
                    "Do you want to continue from an existing file? (y/n): ", "cyan"
                )
            ).lower()
            == "y"
        )

        if continue_from_file:
            file_path = input(
                colored("Enter the path to the existing Python file: ", "cyan")
            )
            while not os.path.exists(file_path) or not file_path.endswith(".py"):
                print(
                    colored(
                        "Error: The file does not exist or is not a Python file.", "red"
                    )
                )
                file_path = input(
                    colored("Please enter a valid Python file path: ", "cyan")
                )

            print(colored("Starting error correction phase...", "cyan"))
            await self.error_correction_cycle(file_path)
        else:
            project_description = input(colored("Enter project description: ", "cyan"))
            if self.models:
                iterations = int(
                    input(colored("Enter number of discussion iterations: ", "cyan"))
                )
                independent_first_round = (
                    input(
                        colored(
                            "Do you want the models to respond independently in the first round instead of a sequential discussion? Models will still discuss in future rounds (y/n): ",
                            "cyan",
                        )
                    ).lower()
                    == "y"
                )
            else:
                iterations = 0
                independent_first_round = False
            file_path = input(colored("Enter output file path: ", "cyan"))
            while not file_path.endswith(".py"):
                print(
                    colored(
                        "Error: The file must be a Python file with a .py extension.",
                        "red",
                    )
                )
                file_path = input(
                    colored("Please enter a valid Python file path: ", "cyan")
                )
            print(colored("Starting project discussion...", "cyan"))
            discussion = await self.discuss_project(
                project_description, iterations, independent_first_round
            )
            await self.generate_code(project_description, discussion, file_path)
            await self.error_correction_cycle(file_path)

        print(colored("Entering feedback improvement phase...", "cyan"))
        while True:
            user_feedback = input(
                colored(
                    "Enter feedback for improvement (or 'done' to finish): ", "yellow"
                )
            )
            if user_feedback.lower() == "done":
                break
            await self.feedback_improvement_cycle(file_path, user_feedback)

        print(
            colored(
                f"Project completed! Final code has been written to {file_path}",
                "green",
            )
        )


if __name__ == "__main__":
    team = CoderTeam()
    asyncio.run(team.run_project())
