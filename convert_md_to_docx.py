import os
import subprocess

def convert_markdown_to_docx():
    # Get all files in the current directory
    files = os.listdir('.')

    for file in files:
        # Skip non-markdown files and README.md
        if file.lower().endswith('.md') and file.lower() != 'readme.md':
            base_name = os.path.splitext(file)[0]
            output_file = f"{base_name}.docx"

            print(f"Converting {file} → {output_file}...")
            try:
                subprocess.run(
                    ['pandoc', '-s', file, '-o', output_file],
                    check=True
                )
                print(f"✅ Successfully created {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to convert {file}: {e}")

if __name__ == "__main__":
    convert_markdown_to_docx()
