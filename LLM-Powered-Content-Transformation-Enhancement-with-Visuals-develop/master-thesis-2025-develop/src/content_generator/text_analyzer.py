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
                    - Important diagrams and photoes
                    Return the points as a numbered list."""
                },
                {
                    "role": "user",
                    "content": f"Extract the key points from this text:\n\n{text}"
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
        """Generate summary using LLM with improved prompting."""
        try:
            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at creating comprehensive yet concise summaries.
                    Focus on:
                    - Main themes and arguments
                    - Key findings and conclusions
                    - Significant implications
                    Keep the summary clear and well-structured."""
                },
                {
                    "role": "user",
                    "content": f"Create a comprehensive summary of this text:\n\n{text}"
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
                    - Maintaining proper markdown syntax"""
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
            # Create a template for the expected structure
            template = {
                "title_slide": {"title": title},
                "summary_slide": {
                    "title": "Executive Summary",
                    "content": summary
                },
                "content_slides": [
                    {
                        "title": "Key Points",
                        "points": key_points
                    }
                ]
            }

            # Ask LLM to enhance the content while maintaining structure
            chat_prompt = [
                {
                    "role": "system",
                    "content": """You are an expert at creating engaging presentations. 
                    I will provide you with a base presentation structure in JSON format.
                    Your task is to return an enhanced version while maintaining the exact same JSON structure.
                    You can modify the text content but must keep the JSON keys and structure identical.In each slide you are allowed
                    ONLY have 5 lines. Add more details. At least you should have 3 pages. You can create diagrams to have a better visualization. 
                    
                    Expected structure:
                    {
                        "title_slide": {
                            "title": "string"
                        },
                        "summary_slide": {
                            "title": "string",
                            "content": "string"
                        },
                        "content_slides": [
                            {
                                "title": "string",
                                "points": ["string"]
                            }
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Enhance this presentation content while maintaining the exact JSON structure:\n{json.dumps(template, indent=2)}"
                }
            ]

            completion_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=chat_prompt,
                max_completion_tokens=2000
            )

            # Get the response and ensure it's valid JSON
            response_text = completion_response.choices[0].message.content

            # Try to find JSON content within the response
            try:
                # First try to parse the entire response
                content = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON portion
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    content = json.loads(json_str)
                else:
                    # If we can't parse the response, use the template
                    logger.warning("Could not parse LLM response, using base template")
                    content = template

            # Validate the structure
            required_keys = ["title_slide", "summary_slide", "content_slides"]
            if not all(key in content for key in required_keys):
                logger.warning("Invalid response structure, using base template")
                content = template

            return content

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return template
        except Exception as e:
            raise Exception(f"Error generating presentation content: {str(e)}")

    def _extract_json_from_text(self, text: str) -> dict:
        """Helper method to extract JSON from text that might contain additional content."""
        try:
            # First try to parse the entire text as JSON
            return json.loads(text)
        except json.JSONDecodeError:
            # If that fails, try to find JSON content within the text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            raise ValueError("No valid JSON found in response")