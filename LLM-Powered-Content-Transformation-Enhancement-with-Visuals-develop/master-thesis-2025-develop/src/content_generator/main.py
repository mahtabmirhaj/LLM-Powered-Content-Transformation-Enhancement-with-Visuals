import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from config import Config
from pdf_processor import PDFProcessor
from text_analyzer import TextAnalyzer
from markdown_converter import MarkdownConverter
from presentation_creator import PresentationCreator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFAgent:
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the PDF processing agent.
        
        Args:
            output_dir: Optional custom output directory path
        """
        try:
            # Initialize configuration
            self.config = Config()
            
            # Set up output directory
            self.output_dir = self._setup_output_directory(output_dir)
            
            # Initialize components with dependencies
            self.text_analyzer = TextAnalyzer(self.config)
            self.markdown_converter = MarkdownConverter(self.text_analyzer)
            self.presentation_creator = PresentationCreator(self.text_analyzer)
            self.pdf_processor = PDFProcessor()
            
            logger.info(f"Using output directory: {self.output_dir}")
            
        except Exception as e:
            logger.error(f"Error initializing PDFAgent: {str(e)}")
            raise

    def _setup_output_directory(self, custom_dir: Optional[str] = None) -> Path:
        """
        Set up the output directory for processed files.
        
        Args:
            custom_dir: Optional custom directory path
            
        Returns:
            Path: Path object for the output directory
        """
        try:
            if custom_dir:
                output_dir = Path(custom_dir)
            else:
                # Create output directory in the project directory
                current_dir = Path(__file__).parent
                output_dir = current_dir / "output"
            
            # Create directory with full permissions for the user
            output_dir.mkdir(parents=True, exist_ok=True, mode=0o777)
            logger.info(f"Output directory set up at: {output_dir}")
            return output_dir
            
        except Exception as e:
            logger.error(f"Error setting up output directory: {str(e)}")
            raise

    def process_document(self, pdf_path: str, output_name: Optional[str] = None) -> Dict:
        """
        Process PDF document through all stages of the pipeline.
        
        Args:
            pdf_path: Path to the PDF file
            output_name: Optional custom name for output files
            
        Returns:
            Dict containing paths to generated files and extracted information
        """
        try:
            logger.info(f"Starting to process document: {pdf_path}")
            
            # Validate PDF path
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found at {pdf_path}")
            
            # Generate output prefix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_name:
                base_name = output_name
            else:
                base_name = pdf_path.stem
            
            output_prefix = self.output_dir / f"{base_name}_{timestamp}"
            
            # Extract and clean text from PDF
            logger.info("Extracting text from PDF")
            text = self.pdf_processor.extract_pdf(str(pdf_path))
            
            # Generate summary using LLM
            logger.info("Generating summary")
            summary = self.text_analyzer.generate_summary(text)
            
            # Extract key points using LLM
            logger.info("Extracting key points")
            key_points = self.text_analyzer.extract_key_points(text)
            
            # Convert to markdown and enhance with LLM
            logger.info("Converting to markdown")
            markdown_text = self.markdown_converter.convert_to_markdown(text)
            markdown_path = f"{output_prefix}_output.md"
            self.markdown_converter.save_markdown(markdown_text, markdown_path)
            
            # Create presentation with LLM-enhanced content
            logger.info("Creating presentation")
            presentation_path = f"{output_prefix}_presentation.pptx"
            self.presentation_creator.create_presentation(
                title=pdf_path.name,
                summary=summary,
                key_points=key_points,
                output_path=presentation_path
            )
            
            results = {
                "summary": summary,
                "key_points": key_points,
                "markdown_path": markdown_path,
                "presentation_path": presentation_path
            }
            
            logger.info("Document processing completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

def process_batch(pdf_dir: str, output_dir: Optional[str] = None) -> None:
    """
    Process all PDF files in a directory.
    
    Args:
        pdf_dir: Directory containing PDF files
        output_dir: Optional custom output directory
    """
    try:
        # Initialize agent
        agent = PDFAgent(output_dir)
        
        # Process all PDF files in directory
        pdf_path = Path(pdf_dir)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Directory not found: {pdf_dir}")
        
        pdf_files = list(pdf_path.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Processing {pdf_file.name}")
                results = agent.process_document(str(pdf_file))
                
                # Log results
                logger.info(f"Successfully processed {pdf_file.name}")
                logger.info(f"Generated files:")
                logger.info(f"- Markdown: {results['markdown_path']}")
                logger.info(f"- Presentation: {results['presentation_path']}")
                
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        raise

def main():
    """Main entry point for the PDF processing system."""
    try:
        # Get input from user
        while True:
            print("\nPDF Processing Options:")
            print("1. Process single PDF file")
            print("2. Process directory of PDF files")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                pdf_path = input("\nEnter the path to your PDF file: ").strip()
                output_name = input("Enter custom output name (or press Enter for default): ").strip()
                
                agent = PDFAgent()
                try:
                    results = agent.process_document(pdf_path, output_name if output_name else None)
                    
                    # Print results
                    print("\nProcessing completed successfully!")
                    print(f"\nSummary:\n{results['summary']}")
                    print(f"\nKey Points:")
                    for point in results['key_points']:
                        print(f"• {point}")
                    print(f"\nOutputs saved to:")
                    print(f"- Markdown: {results['markdown_path']}")
                    print(f"- Presentation: {results['presentation_path']}")
                    
                except Exception as e:
                    print(f"\nError: {str(e)}")
                
            elif choice == "2":
                pdf_dir = input("\nEnter the directory path containing PDF files: ").strip()
                output_dir = input("Enter custom output directory (or press Enter for default): ").strip()
                
                try:
                    process_batch(pdf_dir, output_dir if output_dir else None)
                    print("\nBatch processing completed!")
                    
                except Exception as e:
                    print(f"\nError: {str(e)}")
                
            elif choice == "3":
                print("\nExiting program.")
                break
                
            else:
                print("\nInvalid choice. Please try again.")
                
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        logger.error(f"Unexpected error in main: {str(e)}")

if __name__ == "__main__":
    main()