import os
import sys
import base64
import json
import io
from PIL import Image
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: The 'fitz' module is not installed.")
    print("Please install it using: pip install pymupdf")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: The 'openai' module is not installed.")
    print("Please install it using: pip install openai")
    sys.exit(1)

# Get API settings - first try environment variables, then user input
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
# Get API settings from user if not set as environment variables
if OPENROUTER_MODEL is None or OPENROUTER_MODEL == '':
    print("OPENROUTER_MODEL environment variable is not set.")
    OPENROUTER_MODEL = input("Please enter your OpenRouter model (e.g., meta-llama/llama-4-maverick): ").strip()
    if not OPENROUTER_MODEL:
        print("No model provided. Exiting!")
        sys.exit(1)

if OPENROUTER_API_KEY is None or OPENROUTER_API_KEY == '':
    print("OPENROUTER_API_KEY environment variable is not set.")
    OPENROUTER_API_KEY = input("Please enter your OpenRouter API key: ").strip()
    if not OPENROUTER_API_KEY:
        print("No API key provided. Exiting!")
        sys.exit(1)

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def extract_images_from_pdf(pdf_path):
    """Extract images from a PDF file."""
    print(f"Extracting images from {pdf_path}")
    
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    images = []
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        
        # Process each image on the page
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Create a PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to base64
            buffered = io.BytesIO()
            image.save(buffered, format=image.format if image.format else "JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            images.append({
                "page": page_num + 1,
                "index": img_index + 1,
                "base64": img_base64,
                "format": base_image["ext"]
            })
            
            print(f"Extracted image {img_index + 1} from page {page_num + 1}")
    
    pdf_document.close()
    return images

def get_image_description(image_base64, image_format="jpeg"):
    """Get a description of the image using the LLM."""
    try:
        # Prepare the prompt with the image included
        prompt_with_image = [
            {
                "type": "text",
                "text": "Describe this image in detail. What does it show? Include any text visible in the image."
            },
            {
                "type": "image_url",
                "image_url": f"data:image/{image_format};base64,{image_base64}"
            }
        ]

        # Prepare the messages payload
        messages = [
            {
                "role": "user",
                "content": prompt_with_image
            }
        ]

        # Get response from the model
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
            max_tokens=1000,
        )

        return response.choices[0].message.content
    
    except Exception as e:
        error_message = str(e)
        if "Insufficient credits" in error_message:
            print("\nERROR: Insufficient credits in your OpenRouter account.")
            print("Please add more credits at: https://openrouter.ai/settings/credits\n")
        elif "API key" in error_message.lower():
            print("\nERROR: Invalid API key or authentication issue.")
            print("Please check your OpenRouter API key is correct.\n")
        else:
            print(f"\nERROR when calling the LLM API: {error_message}\n")
        
        return f"[Error getting description: {error_message}]"

def save_to_markdown(pdf_name, image_descriptions):
    """Save the image descriptions to a markdown file."""
    output_file = f"{pdf_name}_image_analysis.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Image Analysis for {pdf_name}\n\n")
        
        for img in image_descriptions:
            # Skip images that don't have descriptions (those that weren't processed)
            if 'description' not in img:
                continue
                
            f.write(f"## Page {img['page']}, Image {img['index']}\n\n")
            f.write(f"### Description\n\n{img['description']}\n\n")
            
            # Save image to separate file instead of embedding it directly
            img_filename = f"{pdf_name}_page{img['page']}_img{img['index']}.{img['format'].lower()}"
            try:
                # Decode base64 and save as file
                with open(img_filename, 'wb') as img_file:
                    img_file.write(base64.b64decode(img['base64']))
                # Reference the file in markdown instead of embedding base64
                f.write(f"![Image {img['index']} from page {img['page']}]({img_filename})\n\n")
                print(f"Saved image to {img_filename}")
            except Exception as e:
                print(f"Error saving image file: {e}")
                # Fallback - don't include image if there's an error
                f.write(f"*Image could not be saved to file*\n\n")
            
            f.write("---\n\n")
    
    print(f"Results saved to {output_file}")
    return output_file

# Main execution
def main():
    try:
        # Ask user for PDF file path
        pdf_path = input("Please enter the path to your PDF file: ").strip()
        
        # Validate the PDF file exists
        if not os.path.exists(pdf_path):
            print(f"Error: The file '{pdf_path}' does not exist. Exiting!")
            sys.exit(1)
            
        pdf_name = os.path.basename(pdf_path).split('.')[0]
        
        # Extract images from PDF
        images = extract_images_from_pdf(pdf_path)
        print(f"Found {len(images)} images in the PDF")
        
        if not images:
            print("No images found in the PDF. Exiting.")
            sys.exit(0)
        
        # Create a list to track which images to process
        images_to_process = []
            
        # Ask user if they want to limit processing (to save credits)
        process_all = input(f"Process all {len(images)} images? This may use significant API credits. (y/n): ").lower().strip()
        if process_all != 'y':
            try:
                limit = int(input("How many images would you like to process? ").strip())
                if 0 < limit < len(images):
                    print(f"Processing only the first {limit} images.")
                    images_to_process = images[:limit]
                else:
                    print(f"Invalid number. Processing all {len(images)} images.")
                    images_to_process = images
            except ValueError:
                print("Invalid input. Processing all images.")
                images_to_process = images
        else:
            images_to_process = images
        
        # Ask if the user wants to save the images as separate files
        save_images = input("Would you like to save images as separate files? (y/n): ").lower().strip() == 'y'
        
        # Get descriptions for each selected image
        processed_images = []
        for i, img in enumerate(images_to_process):
            print(f"Getting description for image {img['index']} from page {img['page']} ({i+1}/{len(images_to_process)})")
            
            try:
                img['description'] = get_image_description(img['base64'], img['format'])
                
                # If saving as separate files, add a flag to the image data
                img['embed_image'] = not save_images
                
                processed_images.append(img)
                
                # Check if the description contains an error message
                if "[Error getting description:" in img['description']:
                    answer = input("Continue processing more images? (y/n): ").lower().strip()
                    if answer != 'y':
                        print("Stopping image processing. Saving results so far...")
                        break
            except Exception as e:
                print(f"Error processing image {i+1}: {e}")
                answer = input("Continue with next image? (y/n): ").lower().strip()
                if answer != 'y':
                    break
        
        # Save results to markdown
        if processed_images:
            output_file = save_to_markdown(pdf_name, processed_images)
            print(f"Process completed. Results saved to {output_file}")
            if save_images:
                print("Images have been saved as separate files in the current directory.")
        else:
            print("No images were successfully processed. No output file created.")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Saving any processed results...")
        try:
            if 'processed_images' in locals() and processed_images and 'pdf_name' in locals():
                output_file = save_to_markdown(pdf_name, processed_images)
                print(f"Partial results saved to {output_file}")
                if save_images:
                    print("Images have been saved as separate files in the current directory.")
            else:
                print("No processed images to save.")
        except Exception as e:
            print(f"Error saving partial results: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()