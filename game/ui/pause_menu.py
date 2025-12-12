import pygame
import webbrowser
import os
import json
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, PRIMARY_BLUE, WARM_BEIGE
from game.managers.asset_manager import AssetManager

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 50)
        self.options = ["Resume", "Print Resume", "Main Menu"]
        self.selected_index = 0
        self.visible = False

        self.rect = pygame.Rect(0, 0, 400, 300)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.asset_manager = AssetManager()
        self.resume_data = self.asset_manager.get_json('resume.json')

    def toggle(self):
        self.visible = not self.visible
        self.selected_index = 0

    def handle_events(self, events):
        if not self.visible:
            return False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.select_option()
                elif event.key == pygame.K_ESCAPE:
                    self.toggle()

        return True # Consumed input

    def select_option(self):
        option = self.options[self.selected_index]
        if option == "Resume":
            self.toggle()
        elif option == "Print Resume":
            self.export_resume()
        elif option == "Main Menu":
            self.toggle()
            self.game.scene_manager.set_scene("menu_scene")

    def export_resume(self):
        # Generate HTML
        html_content = self.generate_html()

        # Determine output path
        # If web (pygbag), we might not be able to write file easily to user desktop.
        # But for "desktop build", we can write to user home or similar.
        # Since I am in a sandbox, I will write to a local file and simulate the action.

        filename = "Resume_Sumanth_Udupi.html"

        try:
            with open(filename, "w", encoding='utf-8') as f:
                f.write(html_content)
            print(f"Resume exported to {os.path.abspath(filename)}")

            # Open the file
            webbrowser.open('file://' + os.path.abspath(filename))
        except Exception as e:
            print(f"Failed to export resume: {e}")

    def generate_html(self):
        if not self.resume_data:
            return "<html><body><h1>Resume Data Not Found</h1></body></html>"

        info = self.resume_data.get('contact_info', {})
        summary = self.resume_data.get('professional_summary', '')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{info.get('name')} - Resume</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #2980b9; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                .contact {{ margin-bottom: 20px; }}
                .job {{ margin-bottom: 20px; }}
                .job-title {{ font-weight: bold; font-size: 1.1em; }}
                .company {{ font-style: italic; }}
                .dates {{ float: right; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <h1>{info.get('name')}</h1>
            <div class="contact">
                {info.get('title')}<br>
                {info.get('location')} | {info.get('phone')} | <a href="mailto:{info.get('email')}">{info.get('email')}</a><br>
                <a href="https://{info.get('linkedin')}">LinkedIn</a> | <a href="https://{info.get('github')}">GitHub</a>
            </div>

            <h2>Professional Summary</h2>
            <p>{summary}</p>

            <h2>Skills</h2>
            <ul>
        """

        for cat, skills in self.resume_data.get('skills', {}).items():
            cat_name = cat.replace('_', ' ').title()
            skill_list = ", ".join(skills)
            html += f"<li><strong>{cat_name}:</strong> {skill_list}</li>"

        html += """
            </ul>
            <h2>Professional Experience</h2>
        """

        for job in self.resume_data.get('professional_experience', []):
            html += f"""
            <div class="job">
                <div class="dates">{job.get('dates')}</div>
                <div class="job-title">{job.get('role')}</div>
                <div class="company">{job.get('company')} - {job.get('location', '')}</div>
                <ul>
            """
            for ach in job.get('key_achievements', []):
                html += f"<li>{ach}</li>"
            html += "</ul></div>"

        html += "<h2>Education</h2>"
        for edu in self.resume_data.get('education', []):
            html += f"""
            <div class="edu">
                <strong>{edu.get('degree')}</strong><br>
                {edu.get('institution')} ({edu.get('year')})
            </div><br>
            """

        html += "<h2>Certifications</h2><ul>"
        for cert in self.resume_data.get('certifications', []):
            html += f"<li>{cert}</li>"

        html += "</ul></body></html>"
        return html

    def draw(self, screen):
        if not self.visible:
            return

        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Draw Menu Box
        pygame.draw.rect(screen, WARM_BEIGE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Draw Title
        title_surf = self.font.render("Paused", True, PRIMARY_BLUE)
        title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.top + 40))
        screen.blit(title_surf, title_rect)

        # Draw Options
        start_y = self.rect.top + 100
        for i, option in enumerate(self.options):
            color = PRIMARY_BLUE if i == self.selected_index else BLACK
            text_surf = self.font.render(option, True, color)
            rect = text_surf.get_rect(center=(self.rect.centerx, start_y + i * 50))
            screen.blit(text_surf, rect)
