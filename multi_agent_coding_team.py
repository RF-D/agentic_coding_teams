from dataclasses import dataclass, field
from typing import List, Dict
import asyncio
from termcolor import colored
from unified import UnifiedApis
import subprocess
import os


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
In discussions, provide insights that reflect your leadership role and technical expertise."""

        self.ai_agent = UnifiedApis(
            name="Claude",
            provider="anthropic",
            model="claude-3-5-sonnet-20240620",
            use_async=True,
            print_color="yellow",
        )

        # Set the system message after initializing the UnifiedApis instance
        self.ai_agent.set_system_message(system_message)

    def coordinate_team(self):
        print(
            colored(
                f"{self.name} is coordinating the team and assigning tasks.",
                self.ai_agent.print_color,
            )
        )


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

    async def error_correction_cycle(self, file_path: str):
        while True:
            print(colored("\nExecuting code...", "cyan"))
            try:
                result = subprocess.run(
                    ["python", file_path], capture_output=True, text=True, check=True
                )
                print(colored("Code execution successful!", "green"))
                if result.stdout:
                    print(colored("Output:", "blue"))
                    print(result.stdout)
                return  # Exit the method if execution is successful
            except subprocess.CalledProcessError as e:
                error_message = e.stderr
                print(colored(f"Error detected: {error_message}", "red"))
                with open(file_path, "r") as f:
                    current_code = f.read()

                print(colored("Attempting to fix the error...", "yellow"))
                correction_prompt = f"Error message:\n{error_message}\n\nCurrent code:\n{current_code}\n\nPlease fix the error and provide the full corrected code wrapped in <code></code> tags."
                corrected_code_response = await self.error_corrector.chat_async(
                    correction_prompt
                )

                corrected_code = (
                    corrected_code_response.split("<code>")[1]
                    .split("</code>")[0]
                    .strip()
                )
                with open(file_path, "w") as f:
                    f.write(corrected_code)
                print(colored("Applied fix. Retrying execution...", "magenta"))

    async def feedback_improvement_cycle(self, file_path: str, user_feedback: str):
        with open(file_path, "r") as f:
            current_code = f.read()

        print(colored("\nGathering improvement suggestions from the team...", "cyan"))
        suggestions = await asyncio.gather(
            *[
                member.discuss(
                    f"User feedback: {user_feedback}\n\nCurrent code:\n{current_code}\n\nProvide a plan on how to best implement the changes asked by the user (do not write full code)."
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
        improvement_prompt = f"User feedback: {user_feedback}\n\nTeam suggestions:\n{' '.join(suggestions)}\n\nCurrent code:\n{current_code}\n\nPlease improve the code based on the user feedback and the best elements from the team suggestions. Provide the full improved code wrapped in <code></code> tags."
        improved_code_response = await lead_developer.discuss(improvement_prompt)

        improved_code = (
            improved_code_response.split("<code>")[1].split("</code>")[0].strip()
        )
        with open(file_path, "w") as f:
            f.write(improved_code)
        print(colored(f"Improved code written to {file_path}", "green"))

        # Run the code after improvement
        await self.error_correction_cycle(file_path)

    async def run_project(self):
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
            iterations = int(
                input(colored("Enter number of discussion iterations: ", "cyan"))
            )
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
            discussion = await self.discuss_project(project_description, iterations)
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
