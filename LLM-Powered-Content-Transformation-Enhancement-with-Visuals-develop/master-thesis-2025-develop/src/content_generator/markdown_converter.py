from typing import Dict, List

class MarkdownConverter:
    def __init__(self, text_analyzer):
        self.text_analyzer = text_analyzer

    def convert_to_markdown(self, text: str) -> str:
        """Convert text to enhanced markdown format using LLM."""
        # First, create a basic markdown structure
        basic_markdown = self._create_basic_markdown(text)
        
        # Then use LLM to enhance it
        enhanced_markdown = self.text_analyzer.enhance_markdown(basic_markdown)
        
        return enhanced_markdown

    def _create_basic_markdown(self, text: str) -> str:
        """Create basic markdown structure from text."""
        sections = []
        current_section = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            else:
                current_section.append(line)
        
        if current_section:
            sections.append('\n'.join(current_section))
        
        return '\n\n'.join(sections)

    def save_markdown(self, markdown_text: str, output_path: str):
        """Save markdown content to file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
        except Exception as e:
            raise Exception(f"Error saving markdown file: {str(e)}")

# Make the class available for import
__all__ = ['MarkdownConverter']