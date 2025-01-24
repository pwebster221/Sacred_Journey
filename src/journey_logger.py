import os
from datetime import datetime, timedelta
import re
import json
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import seaborn as sns


class JourneyLogger:
    def __init__(self, base_path: str = "journey_logs"):
        """Initialize the sacred space for your daily reflections."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def create_daily_template(self, date: Optional[datetime] = None) -> str:
        """Generate a new vessel for today's journey."""
        date = date or datetime.now()
        template_path = self.base_path / f"{date.strftime('%Y-%m-%d')}_journey.md"

        if not template_path.exists():
            with open('templates/daily-template.md', 'r') as f:
                template = f.read()

            filled_template = template.replace('{DATE}', date.strftime('%Y-%m-%d'))
            with open(template_path, 'w') as f:
                f.write(filled_template)

        return str(template_path)

    def extract_insights(self, days: int = 7) -> Dict:
        """Gather the crystallized wisdom from your recent journey."""
        insights = {
            'energy_patterns': [],
            'recurring_themes': {},
            'project_progress': {},
            'emergent_connections': []
        }

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        for log_file in self.base_path.glob('*_journey.md'):
            date_str = log_file.name.split('_')[0]
            log_date = datetime.strptime(date_str, '%Y-%m-%d')

            if start_date <= log_date <= end_date:
                with open(log_file, 'r') as f:
                    content = f.read()

                # Extract energy levels
                energy_match = re.search(r'Energy Level.*?(\d+)', content)
                if energy_match:
                    insights['energy_patterns'].append({
                        'date': date_str,
                        'level': int(energy_match.group(1))
                    })

                # Extract emergent thoughts
                emergent_section = re.search(r'## Emergent Thoughts\n(.*?)\n##',
                                             content, re.DOTALL)
                if emergent_section:
                    insights['emergent_connections'].append({
                        'date': date_str,
                        'thoughts': emergent_section.group(1).strip()
                    })

                # Extract project progress
                project_sections = re.finditer(r'### Technical Projects\n#### (.*?)\n(.*?)(?=###|$)',
                                               content, re.DOTALL)
                for match in project_sections:
                    project_name = match.group(1).split(' - ')[0]
                    progress = re.search(r'Progress Made:(.*?)(?=Challenges|$)',
                                         match.group(2), re.DOTALL)
                    if progress:
                        if project_name not in insights['project_progress']:
                            insights['project_progress'][project_name] = []
                        insights['project_progress'][project_name].append({
                            'date': date_str,
                            'progress': progress.group(1).strip()
                        })

        return insights

    def visualize_energy_flow(self, days: int = 30):
        """Create a visual manifestation of your energy patterns."""
        insights = self.extract_insights(days)
        if not insights['energy_patterns']:
            return

        df = pd.DataFrame(insights['energy_patterns'])
        df['date'] = pd.to_datetime(df['date'])

        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        sns.lineplot(data=df, x='date', y='level', marker='o')
        plt.title('Energy Flow Through Time')
        plt.xlabel('Date')
        plt.ylabel('Energy Level')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.base_path / 'energy_flow.png')
        plt.close()

    def find_connections(self, search_term: str) -> List[Dict]:
        """Trace the threads of connection through your journey."""
        connections = []

        for log_file in self.base_path.glob('*_journey.md'):
            with open(log_file, 'r') as f:
                content = f.read()

            if search_term.lower() in content.lower():
                date_str = log_file.name.split('_')[0]
                relevant_sections = []

                # Find paragraphs containing the search term
                paragraphs = re.split(r'\n\n+', content)
                for para in paragraphs:
                    if search_term.lower() in para.lower():
                        relevant_sections.append(para.strip())

                if relevant_sections:
                    connections.append({
                        'date': date_str,
                        'contexts': relevant_sections
                    })

        return connections

    def generate_weekly_reflection(self) -> str:
        """Synthesize the wisdom of your week's journey."""
        insights = self.extract_insights(7)

        reflection = "# Weekly Journey Synthesis\n\n"

        # Energy flow analysis
        if insights['energy_patterns']:
            df = pd.DataFrame(insights['energy_patterns'])
            avg_energy = sum(df['level']) / len(df['level'])
            reflection += f"## Energy Flow\nAverage energy level: {avg_energy:.1f}\n\n"

        # Project progress synthesis
        reflection += "## Project Movements\n"
        for project, progress in insights['project_progress'].items():
            reflection += f"\n### {project}\n"
            for entry in progress:
                reflection += f"- {entry['date']}: {entry['progress']}\n"

        # Emergent patterns
        reflection += "\n## Emergent Patterns\n"
        all_thoughts = ' '.join([entry['thoughts']
                                 for entry in insights['emergent_connections']])
        words = re.findall(r'\w+', all_thoughts.lower())
        word_freq = pd.Series(words).value_counts()[:5]
        reflection += "Recurring themes in your reflections:\n"
        for word, freq in word_freq.items():
            reflection += f"- {word}: appeared {freq} times\n"

        return reflection


def main():
    logger = JourneyLogger()

    # Create today's template
    template_path = logger.create_daily_template()
    print(f"Today's journey template created at: {template_path}")

    # Generate weekly reflection
    reflection = logger.generate_weekly_reflection()
    reflection_path = logger.base_path / f"weekly_reflection_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(reflection_path, 'w') as f:
        f.write(reflection)

    # Visualize energy patterns
    logger.visualize_energy_flow()

    print("\nWeekly reflection generated and energy patterns visualized.")
    print("May these insights illuminate your path forward.")


if __name__ == "__main__":
    main()