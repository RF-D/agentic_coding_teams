from dataclasses import dataclass, field
from typing import List, Dict
import asyncio
from termcolor import colored
from unified import UnifiedApis
import subprocess
import os
import sys
import re
import importlib
import pkg_resources


@dataclass
class TeamMember:
    name: str
    role: str
    skills: List[str]
    tasks: List[str] = field(default_factory=list)
    ai_agent: UnifiedApis = None

    def assign_task(self, task: str):
        self.tasks.append(task)

    def complete_task(self, task: str):
        if task in self.tasks:
            self.tasks.remove(task)
            print(
                colored(
                    f"{self.name} completed task: {task}", self.ai_agent.print_color
                )
            )
        else:
            print(
                colored(f"Task '{task}' not found in {self.name}'s task list.", "red")
            )

    async def discuss(self, prompt: str) -> str:
        if self.ai_agent:
            response = await self.ai_agent.chat_async(prompt)
            return f"{self.name} ({self.role}): {response}"
        return f"{self.name} ({self.role}) cannot discuss without an AI agent."

    async def generate_report(self, project_description: str, discussion: str) -> str:
        prompt = f"""Based on the following project description and team discussion, generate a report from your perspective as {self.role}. 
        Include your insights, concerns, and suggestions for the project.

        Project Description: {project_description}

        Team Discussion: {discussion}

        Please structure your report using XML tags as follows:
        <report>
            <insights>Your key insights here</insights>
            <concerns>Any concerns you have about the project</concerns>
            <suggestions>Your suggestions for improvement or next steps</suggestions>
        </report>
        """
        report = await self.ai_agent.chat_async(prompt)
        return f"{self.name} ({self.role}) Report:\n{report}"


@dataclass
class ProjectLead(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name,
            "Project Lead / Full-Stack Developer",
            ["Python", "JavaScript", "React", "Node.js", "Project Management"],
        )
        system_message = f"""You are {name}, the Project Lead and Full-Stack Developer of the team.
Your role involves overseeing the project, making high-level decisions, and contributing to both frontend and backend development.
Your skills include: Python, JavaScript, React, Node.js, and Project Management.
In discussions, provide insights that reflect your leadership role and technical expertise.
When asked to generate code, you may create multiple files if necessary for the project structure.
Please structure your responses using XML tags for easier parsing. For example:
<response>
    <insight>Your technical insight here</insight>
    <decision>Your project decision here</decision>
    <suggestion>Your suggestion for the team here</suggestion>
</response>
When generating multiple files, use the following structure:
<files>
    <file>
        <name>filename.ext</name>
        <content>
            // File content here
        </content>
    </file>
    // Repeat for each file
</files>
"""

        self.ai_agent = UnifiedApis(
            name="Claude",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
            print_color="yellow",
            json_mode=False,
            use_cache=False,
        )

        self.ai_agent.set_system_message(system_message)

    def coordinate_team(self):
        print(
            colored(
                f"{self.name} is coordinating the team and assigning tasks.",
                self.ai_agent.print_color,
            )
        )

    async def generate_multi_file_code(self, project_description: str, discussion: str):
        prompt = f"""Based on the following project description and team discussion, generate a multi-file code structure for the project. 
        Include all necessary files for a complete project structure.

        Project Description: {project_description}

        Team Discussion: {discussion}

        Please provide the code structure using the following format:
        <files>
            <file>
                <name>filename.ext</name>
                <content>
                    // File content here
                </content>
            </file>
            // Repeat for each file
        </files>
        """
        response = await self.ai_agent.chat_async(prompt)
        return self.parse_multi_file_response(response)

    def parse_multi_file_response(self, response: str) -> Dict[str, str]:
        files = {}
        file_matches = re.finditer(
            r"<file>.*?<name>(.*?)</name>.*?<content>(.*?)</content>.*?</file>",
            response,
            re.DOTALL,
        )
        for match in file_matches:
            filename = match.group(1).strip()
            content = match.group(2).strip()
            files[filename] = content
        return files


@dataclass
class AISpecialist(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name,
            "AI Integration Specialist",
            ["Python", "Machine Learning", "NLP", "API Integration"],
        )
        system_message = f"""You are {name}, the AI Integration Specialist of the team.
Your role involves integrating AI features into the project, including machine learning, natural language processing, and API integration.
Your skills include: Python, Machine Learning, NLP, and API Integration.
In discussions, provide insights that reflect your expertise in AI integration."""

        self.ai_agent = UnifiedApis(
            name="GPT-4o",
            provider="openai",
            model="gpt-4o",
            use_async=True,
            print_color="magenta",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def integrate_ai_feature(self, feature: str):
        print(
            colored(
                f"{self.name} is integrating AI feature: {feature}",
                self.ai_agent.print_color,
            )
        )


@dataclass
class UIUXDesigner(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name,
            "UI/UX Designer",
            ["Figma", "Adobe XD", "HTML", "CSS", "User Research"],
        )
        system_message = f"""You are {name}, the UI/UX Designer of the team.
Your role involves creating user-friendly and visually appealing designs for the project.
Your skills include: Figma, Adobe XD, HTML, CSS, and User Research.
In discussions, provide insights that reflect your expertise in UI/UX design."""

        self.ai_agent = UnifiedApis(
            name="Claude",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
            print_color="cyan",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def create_design(self, component: str):
        print(
            colored(
                f"{self.name} is creating a design for: {component}",
                self.ai_agent.print_color,
            )
        )


@dataclass
class BackendDeveloper(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name,
            "Backend Developer",
            ["Python", "Django", "Flask", "Database Design", "API Development"],
        )
        system_message = f"""You are {name}, the Backend Developer of the team.
Your role involves implementing the backend of the project, including database design and API development.
Your skills include: Python, Django, Flask, Database Design, and API Development.
In discussions, provide insights that reflect your expertise in backend development."""

        self.ai_agent = UnifiedApis(
            name="DeepSeek",
            provider="openrouter",
            model="deepseek/deepseek-coder",
            use_async=True,
            print_color="green",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def implement_api_endpoint(self, endpoint: str):
        print(
            colored(
                f"{self.name} is implementing API endpoint: {endpoint}",
                self.ai_agent.print_color,
            )
        )


@dataclass
class FrontendDeveloper(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name, "Frontend Developer", ["JavaScript", "React", "Vue.js", "HTML", "CSS"]
        )
        system_message = f"""You are {name}, the Frontend Developer of the team.
Your role involves creating the user interface of the project, including components and layouts.
Your skills include: JavaScript, React, Vue.js, HTML, and CSS.
In discussions, provide insights that reflect your expertise in frontend development."""

        self.ai_agent = UnifiedApis(
            name="Sonnet-Coder",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
            print_color="blue",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def create_component(self, component: str):
        print(
            colored(
                f"{self.name} is creating frontend component: {component}",
                self.ai_agent.print_color,
            )
        )


@dataclass
class SoftwareArchitect(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name,
            "Software Architect",
            ["System Design", "Scalability", "Design Patterns", "Cloud Architecture"],
        )
        system_message = f"""You are {name}, the Software Architect of the team.
Your role involves designing the overall architecture of the project, including system design, scalability, and cloud architecture.
Your skills include: System Design, Scalability, Design Patterns, and Cloud Architecture.
In discussions, provide insights that reflect your expertise in software architecture."""

        self.ai_agent = UnifiedApis(
            name="GPT-4",
            provider="openai",
            model="gpt-4o",
            use_async=True,
            print_color="blue",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def design_architecture(self, component: str):
        print(
            colored(
                f"{self.name} is designing the architecture for: {component}",
                self.ai_agent.print_color,
            )
        )


@dataclass
class QualityAssuranceEngineer(TeamMember):
    def __init__(self, name: str):
        super().__init__(
            name,
            "Quality Assurance Engineer",
            [
                "Test Automation",
                "Performance Testing",
                "Security Testing",
                "Code Review",
            ],
        )
        system_message = f"""You are {name}, the Quality Assurance Engineer of the team.
Your role involves ensuring the quality of the project, including test automation, performance testing, security testing, and code review.
Your skills include: Test Automation, Performance Testing, Security Testing, and Code Review.
In discussions, provide insights that reflect your expertise in quality assurance."""

        self.ai_agent = UnifiedApis(
            name="Claude-QA",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
            print_color="magenta",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def review_code(self, component: str):
        print(
            colored(
                f"{self.name} is reviewing the code for: {component}",
                self.ai_agent.print_color,
            )
        )


@dataclass
class CodingTeam:
    members: List[TeamMember] = field(default_factory=list)
    error_corrector: UnifiedApis = UnifiedApis(
        name="ErrorFixer",
        provider="anthropic",
        model="claude-3-5-sonnet-20240620",
        use_async=True,
        print_color="red",
    )

    def add_member(self, member: TeamMember):
        self.members.append(member)

    def list_members(self):
        for member in self.members:
            print(
                colored(f"{member.name} - {member.role}", member.ai_agent.print_color)
            )
            print(
                colored(
                    f"  Skills: {', '.join(member.skills)}", member.ai_agent.print_color
                )
            )
            print(
                colored(
                    f"  Tasks: {', '.join(member.tasks)}", member.ai_agent.print_color
                )
            )
            print()

    async def discuss_project(self, project_description: str, iterations: int):
        discussion = []
        for i in range(iterations):
            print(colored(f"\nIteration {i+1}/{iterations}", "cyan"))
            round_responses = []
            for member in self.members:
                full_discussion = "\n".join(discussion)
                round_responses_text = "\n".join(round_responses)
                prompt = f"""Discuss the following project:

{project_description}

Current round's responses:
{round_responses_text}

Previous discussion:
{full_discussion}

Please continue the discussion, taking into account the project description and previous comments from team members."""

                response = await member.discuss(prompt)
                colored_response = colored(
                    f"{member.name} ({member.role}): {response}",
                    member.ai_agent.print_color,
                )
                round_responses.append(colored_response)
                print(colored_response)  # Print each response as it's generated
            discussion.extend(round_responses)
        return "\n".join(discussion)

    async def generate_code(
        self, project_description: str, discussion: str, file_path: str
    ):
        print(colored("\nGenerating initial code...", "blue"))
        lead_developer = next(
            member for member in self.members if isinstance(member, ProjectLead)
        )
        prompt = f"""Generate code for this project based on the discussion:

Project: {project_description}

Team Discussion:
{discussion}

Provide the full code wrapped in <code></code> tags."""
        code_response = await lead_developer.discuss(prompt)

        code = code_response.split("<code>")[1].split("</code>")[0].strip()
        with open(file_path, "w") as f:
            f.write(code)
        print(colored(f"Initial code written to {file_path}", "green"))
        return code

    async def error_correction_cycle(self, project_path: str):
        while True:
            error_output = self.execute_project(project_path)
            if not error_output:
                print(colored("No errors found. Project runs successfully!", "green"))
                break

            print(colored(f"Error found:\n{error_output}", "red"))

            # Check for ModuleNotFoundError
            module_not_found = re.search(
                r"ModuleNotFoundError: No module named '(\w+)'", error_output
            )
            if module_not_found:
                module_name = module_not_found.group(1)
                if await self.install_missing_dependencies(module_name, project_path):
                    continue
                else:
                    print(
                        colored(
                            f"Unable to resolve dependency issue for {module_name}. Trying general error fixing.",
                            "yellow",
                        )
                    )

            # Handle all other errors generically
            fixed = await self.fix_error(error_output, project_path)
            if not fixed:
                print(
                    colored(
                        "Unable to fix the error automatically. Manual intervention may be required.",
                        "yellow",
                    )
                )
                break

    async def install_missing_dependencies(self, module_name: str, project_path: str):
        try:
            importlib.import_module(module_name)
            print(colored(f"{module_name} is already installed.", "green"))
            return True
        except ImportError:
            pass

        print(
            colored(
                f"The following package is required but not installed: {module_name}",
                "yellow",
            )
        )
        user_input = input(
            colored(f"Do you want to install {module_name}? (yes/no): ", "cyan")
        ).lower()

        if user_input == "yes":
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", module_name]
                )
                print(colored(f"Successfully installed {module_name}", "green"))
                return True
            except subprocess.CalledProcessError:
                print(colored(f"Failed to install {module_name}", "red"))
                return await self.handle_installation_failure(module_name, project_path)

        return False

    async def handle_installation_failure(
        self, module_name: str, project_path: str
    ) -> bool:
        print(
            colored(
                f"Unable to install {module_name}. Attempting to find alternatives...",
                "yellow",
            )
        )

        prompt = f"""
        The package '{module_name}' could not be installed. Please suggest alternatives or a workaround.
        Consider the following options:
        1. Suggest an alternative package that provides similar functionality.
        2. Provide a minimal implementation of the required functionality.
        3. Suggest modifications to the code to work without this package.

        Please format your response as follows:
        <suggestion>
        [Your suggestion here]
        </suggestion>
        <code_changes>
        [Any necessary code changes in the format: filename:line_number:new_code]
        </code_changes>
        """

        response = await self.error_corrector.chat_async(prompt)
        suggestion, code_changes = self.parse_ai_response(response)

        print(colored("AI Suggestion:", "cyan"))
        print(suggestion)

        if code_changes:
            user_input = input(
                colored(
                    "Do you want to apply the suggested changes? (yes/no): ", "cyan"
                )
            ).lower()
            if user_input == "yes":
                self.apply_code_changes(code_changes, project_path)
                return True

        return False

    async def fix_error(self, error_output: str, project_path: str) -> bool:
        prompt = f"""
        An error occurred in the project. Please analyze the error and suggest a fix.
        Do not use any hardcoded solutions for specific libraries.
        Provide a general solution that addresses the root cause of the error.

        Error output:
        {error_output}

        Please provide your solution in the following format:
        <solution>
        [Your explanation and suggested fix here]
        </solution>
        <code_changes>
        [Any code changes, if necessary, in the format: filename:line_number:new_code]
        </code_changes>
        """

        response = await self.error_corrector.chat_async(prompt)

        solution, code_changes = self.parse_ai_response(response)

        print(colored("AI Suggested Solution:", "cyan"))
        print(solution)

        if code_changes:
            user_input = input(
                colored(
                    "Do you want to apply the suggested code changes? (yes/no): ",
                    "cyan",
                )
            ).lower()
            if user_input == "yes":
                self.apply_code_changes(code_changes, project_path)
                return True

        return False

    def parse_ai_response(self, response: str):
        solution_match = re.search(r"<solution>(.*?)</solution>", response, re.DOTALL)
        code_changes_match = re.search(
            r"<code_changes>(.*?)</code_changes>", response, re.DOTALL
        )

        solution = solution_match.group(1).strip() if solution_match else ""
        code_changes = code_changes_match.group(1).strip() if code_changes_match else ""

        return solution, code_changes

    def apply_code_changes(self, code_changes: str, project_path: str):
        changes = code_changes.split("\n")
        for change in changes:
            parts = change.split(":", 2)
            if len(parts) == 3:
                filename, line_number, new_code = parts
                file_path = os.path.join(project_path, filename)
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        lines = f.readlines()

                    line_index = int(line_number) - 1
                    if 0 <= line_index < len(lines):
                        lines[line_index] = new_code + "\n"

                        with open(file_path, "w") as f:
                            f.writelines(lines)

                        print(
                            colored(f"Updated {filename}, line {line_number}", "green")
                        )
                    else:
                        print(
                            colored(
                                f"Invalid line number for {filename}: {line_number}",
                                "red",
                            )
                        )
                else:
                    print(colored(f"File not found: {filename}", "red"))

    async def feedback_improvement_cycle(self, project_path: str, user_feedback: str):
        print(colored("\nGathering improvement suggestions from the team...", "cyan"))
        suggestions = await asyncio.gather(
            *[
                member.discuss(
                    f"User feedback: {user_feedback}\n\nProvide a plan on how to best implement the changes asked by the user (do not write full code)."
                )
                for member in self.members
            ]
        )

        print(
            colored(
                "Generating improved code based on feedback and suggestions...",
                "yellow",
            )
        )
        lead_developer = next(
            member for member in self.members if isinstance(member, ProjectLead)
        )
        improvement_prompt = f"User feedback: {user_feedback}\n\nTeam suggestions:\n{' '.join(suggestions)}\n\nPlease improve the code in the project directory based on the user feedback and the best elements from the team suggestions. Provide the full improved code for each file that needs changes, wrapped in <file>filename.ext</file> tags."
        improved_code_response = await lead_developer.discuss(improvement_prompt)

        # Parse the response to extract file changes
        file_changes = self.parse_file_changes(improved_code_response)

        for filename, content in file_changes.items():
            file_path = os.path.join(project_path, filename)
            with open(file_path, "w") as f:
                f.write(content)
            print(colored(f"Updated file: {file_path}", "green"))

        # Run the code after improvement
        await self.error_correction_cycle(project_path)

    async def generate_team_reports(self, project_description: str, discussion: str):
        reports = []
        for member in self.members:
            report = await member.generate_report(project_description, discussion)
            reports.append(report)
            print(colored(f"\n{report}", member.ai_agent.print_color))
        return "\n\n".join(reports)

    async def generate_multi_file_code(self, project_description: str, discussion: str):
        lead_developer = next(
            member for member in self.members if isinstance(member, ProjectLead)
        )
        files = await lead_developer.generate_multi_file_code(
            project_description, discussion
        )

        # Create a project directory
        project_dir = "generated_project"
        os.makedirs(project_dir, exist_ok=True)

        for filename, content in files.items():
            # Create the full path, including any subdirectories
            file_path = os.path.join(project_dir, filename)
            # Create the directory structure if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w") as f:
                f.write(content)
            print(colored(f"Created file: {file_path}", "green"))

        return files

    async def run_project(self):
        try:
            continue_from_existing = (
                input(
                    colored(
                        "Do you want to continue from an existing project? (y/n): ",
                        "cyan",
                    )
                ).lower()
                == "y"
            )

            if continue_from_existing:
                project_path = input(
                    colored(
                        "Enter the path to the existing project file or directory: ",
                        "cyan",
                    )
                )
                while not (os.path.isfile(project_path) or os.path.isdir(project_path)):
                    print(
                        colored(
                            "Error: The specified path is not a valid file or directory.",
                            "red",
                        )
                    )
                    project_path = input(
                        colored(
                            "Please enter a valid project file or directory path: ",
                            "cyan",
                        )
                    )
            else:
                project_description = input(
                    colored("Enter project description: ", "cyan")
                )
                iterations = int(
                    input(colored("Enter number of discussion iterations: ", "cyan"))
                )
                project_path = "generated_project"
                os.makedirs(project_path, exist_ok=True)

                print(colored("Starting project discussion...", "cyan"))
                discussion = await self.discuss_project(project_description, iterations)

                print(colored("Generating team reports...", "cyan"))
                reports = await self.generate_team_reports(
                    project_description, discussion
                )

                print(colored("Generating multi-file code...", "cyan"))
                files = await self.generate_multi_file_code(
                    project_description, discussion
                )

                for filename, content in files.items():
                    file_path = os.path.join(project_path, filename)
                    with open(file_path, "w") as f:
                        f.write(content)
                    print(colored(f"Created file: {file_path}", "green"))

            print(
                colored(
                    "Starting error correction and dependency installation cycle...",
                    "cyan",
                )
            )
            await self.error_correction_cycle(project_path)

            print(colored("Entering feedback improvement phase...", "cyan"))
            while True:
                user_feedback = input(
                    colored(
                        "Enter feedback for improvement (or 'done' to finish): ",
                        "yellow",
                    )
                )
                if user_feedback.lower() == "done":
                    break
                await self.feedback_improvement_cycle(project_path, user_feedback)

            print(
                colored(
                    f"Project completed! Final code has been written to {project_path}",
                    "green",
                )
            )

        except Exception as e:
            print(colored(f"An unexpected error occurred: {str(e)}", "red"))
            print(colored("Stack trace:", "yellow"))
            import traceback

            traceback.print_exc()

    def parse_file_changes(self, response: str) -> Dict[str, str]:
        file_changes = {}
        file_matches = re.finditer(r"<file>(.*?)</file>", response, re.DOTALL)
        for match in file_matches:
            file_content = match.group(1).strip()
            filename = file_content.split("\n", 1)[0].strip()
            content = (
                file_content.split("\n", 1)[1].strip() if "\n" in file_content else ""
            )
            file_changes[filename] = content
        return file_changes

    def execute_project(self, project_path: str) -> str:
        if os.path.isfile(project_path):
            script_path = project_path
        else:
            # Search for Python files recursively
            python_files = []
            for root, dirs, files in os.walk(project_path):
                python_files.extend(
                    [os.path.join(root, f) for f in files if f.endswith(".py")]
                )

            if not python_files:
                return "No Python files found in the project directory or its subdirectories."

            # Choose the first Python file found (you might want to implement a more sophisticated selection method)
            script_path = python_files[0]

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                check=True,
            )
            return ""  # No error
        except subprocess.CalledProcessError as e:
            return e.stderr


# Create the team
team = CodingTeam()

# Add team members
team.add_member(ProjectLead("Alice"))
team.add_member(SoftwareArchitect("Frank"))
team.add_member(QualityAssuranceEngineer("Grace"))
team.add_member(AISpecialist("Bob"))
team.add_member(UIUXDesigner("Charlie"))
team.add_member(BackendDeveloper("David"))
team.add_member(FrontendDeveloper("Eve"))

# Example usage
if __name__ == "__main__":
    asyncio.run(team.run_project())
