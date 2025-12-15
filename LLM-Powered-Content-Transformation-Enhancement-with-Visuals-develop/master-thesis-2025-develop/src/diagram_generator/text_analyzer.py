from typing import List, Dict
import json

class TextAnalyzer:
    def __init__(self, config):
        self.client = config.get_client()
        self.deployment = config.get_deployment()

    def extract_key_points(self, text: str) -> List[str]:
        """Extract key points using LLM."""
        try:
            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at analyzing documents and extracting key points. 
                    Extract the most important points from the text, focusing on:
                    - Main arguments and findings
                    - Critical data points and statistics
                    - Key conclusions and recommendations
                    - Important diagrams and visuals - describe their content in detail
                    - Extract any charts or graphs and explain their meaning
                    Return the points as a numbered list."""
                },
                {
                    "role": "user",
                    "content": f"Extract the key points, including all visuals and their meaning from this text:\n\n{text}"
                }
            ]

            completion_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=chat_prompt,
                max_completion_tokens=1000
            )

            # Process the response to extract points
            response_text = completion_response.choices[0].message.content
            # Split by newlines and remove numbering
            key_points = [
                point.strip().split('. ', 1)[-1] 
                for point in response_text.split('\n') 
                if point.strip() and any(char.isdigit() for char in point)
            ]
            
            return key_points

        except Exception as e:
            raise Exception(f"Error extracting key points: {str(e)}")

    def generate_summary(self, text: str) -> str:
        """Generate summary using LLM with improved visual understanding."""
        try:
            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at creating comprehensive summaries.
                    Focus on:
                    - Main themes and arguments
                    - Key findings and conclusions
                    - Significant implications
                    - Any visual elements (diagrams, charts, graphs) and their meaning
                    - Relationships between concepts shown in diagrams
                    Keep the summary clear and well-structured."""
                },
                {
                    "role": "user",
                    "content": f"Create a comprehensive summary of this text, including analysis of any visual elements:\n\n{text}"
                }
            ]

            completion_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=chat_prompt,
                max_completion_tokens=800
            )

            return completion_response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def enhance_markdown(self, markdown_text: str) -> str:
        """Enhance markdown content using LLM."""
        try:
            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at improving document structure and readability.
                    Enhance the markdown by:
                    - Improving section organization
                    - Adding clear headers and subheaders
                    - Including relevant emphasis and formatting
                    - Maintaining proper markdown syntax
                    - Adding descriptions of any diagrams or visual elements
                    - Creating markdown-based representations of diagrams where possible"""
                },
                {
                    "role": "user",
                    "content": f"Enhance this markdown content while maintaining its core information:\n\n{markdown_text}"
                }
            ]

            completion_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=chat_prompt,
                max_completion_tokens=2000
            )

            return completion_response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error enhancing markdown: {str(e)}")

    def generate_presentation_content(self, title: str, summary: str, key_points: List[str]) -> dict:
        """Generate enhanced presentation content using LLM."""
        try:
            # Create visual-focused template
            visual_points = [point for point in key_points 
                           if any(word in point.lower() 
                           for word in ['diagram', 'chart', 'graph', 'figure', 'image'])]
            
            template = {
                "title_slide": {"title": title},
                "summary_slide": {
                    "title": "Executive Summary",
                    "content": summary
                },
                "content_slides": [
                    {
                        "title": "Key Concepts",
                        "points": key_points[:5],
                        "visualization": """
                        <svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                            <!-- SVG content will be generated here -->
                        </svg>
                        """
                    },
                    {
                        "title": "Visual Elements",
                        "points": visual_points,
                        "visualization": """
                        <svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                            <!-- SVG content will be generated here -->
                        </svg>
                        """
                    }
                ]
            }

            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at creating engaging presentations and visual representations.
                    For any diagrams or visual elements, create an SVG representation using clean, modern design principles.
                    The SVG should:
                    - Use clear visual hierarchy
                    - Include appropriate shapes, connectors, and text
                    - Use a professional color scheme
                    - Be well-organized and visually appealing
                    - Use <text> elements for labels
                    - Use <path> elements for connectors
                    - Use basic shapes like <circle>, <rect> for nodes
                    
                    Maintain the exact JSON structure but enhance the visualizations."""
                },
                {
                    "role": "user",
                    "content": f"Create a presentation with SVG visualizations for this content:\n{json.dumps(template, indent=2)}"
                }
            ]

            # Ask LLM to enhance the content while maintaining structure
            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at creating engaging presentations. 
                    Enhance this presentation content while maintaining exact JSON structure.
                    For any diagrams, provide specific instructions in this format:
                    {
                        "diagram_type": "radial|flow|hierarchy",
                        "diagram_instructions": {
                            "center_text": "Main concept",
                            "elements": ["Element 1", "Element 2", ...],
                            "steps": ["Step 1", "Step 2", ...],
                            "relationships": [{"from": "Element 1", "to": "Element 2", "type": "arrow"}]
                        }
                    }
                    Maximum 5 elements per diagram.
                    Use clear, specific terms for shapes and connections."""
                },
                {
                    "role": "user",
                    "content": f"Enhance this presentation content:\n{json.dumps(template, indent=2)}"
                }
            ]

            completion_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=chat_prompt,
                max_completion_tokens=2000
            )

            # Get the response and ensure it's valid JSON
            try:
                return json.loads(completion_response.choices[0].message.content)
            except:
                return template

        except Exception as e:
            raise Exception(f"Error generating presentation content: {str(e)}")

    def _extract_json_from_text(self, text: str) -> dict:
        """Helper method to extract JSON from text that might contain additional content."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            raise ValueError("No valid JSON found in response")