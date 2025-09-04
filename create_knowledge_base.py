#!/usr/bin/env python3
"""
Agentic Fabric POC - Project Knowledge Base Extractor
Creates a comprehensive single file containing all project code and structure
for LLM context and documentation purposes.
"""

import os
import datetime
from pathlib import Path


class ProjectKnowledgeExtractor:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.output_file = "KNOWLEDGE_BASE.md"

        # Files and directories to exclude
        self.exclude_dirs = {
            "venv",
            "__pycache__",
            ".git",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
        }

        self.exclude_files = {
            ".DS_Store",
            ".pyc",
            ".pyo",
            ".pyd",
            ".so",
            ".egg-info",
            ".coverage",
            ".env",  # Exclude .env for security
        }

        # File extensions to include full content
        self.include_extensions = {
            ".py",
            ".md",
            ".txt",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".cfg",
            ".ini",
            ".sh",
            ".sql",
        }

        # Maximum file size to include (in bytes)
        self.max_file_size = 50000  # 50KB

    def should_exclude_dir(self, dir_name):
        """Check if directory should be excluded"""
        return dir_name in self.exclude_dirs or dir_name.startswith(".")

    def should_exclude_file(self, file_path):
        """Check if file should be excluded"""
        file_path = Path(file_path)

        # Check file name
        if file_path.name in self.exclude_files:
            return True

        # Check extension
        if file_path.suffix in self.exclude_files:
            return True

        # Check if file is too large
        try:
            if file_path.stat().st_size > self.max_file_size:
                return True
        except OSError:
            return True

        return False

    def should_include_content(self, file_path):
        """Check if file content should be included"""
        file_path = Path(file_path)
        return file_path.suffix.lower() in self.include_extensions

    def get_file_content(self, file_path):
        """Get file content safely"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                return content
        except Exception as e:
            return f"[ERROR READING FILE: {str(e)}]"

    def generate_tree_structure(self):
        """Generate directory tree structure"""
        tree_lines = []

        def add_tree_line(path, prefix="", is_last=True):
            if self.should_exclude_dir(path.name) and path != self.project_root:
                return

            connector = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{connector}{path.name}/")

            # Get subdirectories and files
            try:
                items = sorted(
                    [p for p in path.iterdir() if not self.should_exclude_dir(p.name)]
                )
                dirs = [p for p in items if p.is_dir()]
                files = [
                    p for p in items if p.is_file() and not self.should_exclude_file(p)
                ]

                all_items = dirs + files

                for i, item in enumerate(all_items):
                    is_last_item = i == len(all_items) - 1
                    new_prefix = prefix + ("    " if is_last else "│   ")

                    if item.is_dir():
                        add_tree_line(item, new_prefix, is_last_item)
                    else:
                        file_connector = "└── " if is_last_item else "├── "
                        tree_lines.append(f"{new_prefix}{file_connector}{item.name}")

            except PermissionError:
                pass

        tree_lines.append(f"{self.project_root.name}/")

        # Process root directory contents
        try:
            items = sorted(
                [
                    p
                    for p in self.project_root.iterdir()
                    if not self.should_exclude_dir(p.name)
                ]
            )
            dirs = [p for p in items if p.is_dir()]
            files = [
                p for p in items if p.is_file() and not self.should_exclude_file(p)
            ]

            all_items = dirs + files

            for i, item in enumerate(all_items):
                is_last_item = i == len(all_items) - 1

                if item.is_dir():
                    add_tree_line(item, "", is_last_item)
                else:
                    connector = "└── " if is_last_item else "├── "
                    tree_lines.append(f"{connector}{item.name}")

        except PermissionError:
            tree_lines.append("[Permission denied reading root directory]")

        return "\n".join(tree_lines)

    def collect_all_files(self):
        """Collect all relevant files in the project"""
        all_files = []

        for root, dirs, files in os.walk(self.project_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_dir(d)]

            for file in files:
                file_path = Path(root) / file

                if not self.should_exclude_file(file_path):
                    relative_path = file_path.relative_to(self.project_root)
                    all_files.append(relative_path)

        return sorted(all_files)

    def generate_knowledge_base(self):
        """Generate the complete knowledge base file"""
        print(f"Generating knowledge base for: {self.project_root}")

        content = []

        # Header
        content.append("# AGENTIC FABRIC POC - COMPLETE PROJECT KNOWLEDGE BASE")
        content.append("=" * 80)
        content.append(
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        content.append(f"Project Root: {self.project_root}")
        content.append("")

        # Project Overview
        content.append("## PROJECT OVERVIEW")
        content.append("")
        content.append("**Agentic Fabric POC:** Dual-model AI orchestration platform")
        content.append("- GPT: Master orchestrator for strategic decisions")
        content.append("- Claude: Intelligent agent execution engine")
        content.append("- LangGraph: Workflow coordination")
        content.append("- Streamlit: User interface")
        content.append("")

        # Directory Structure
        content.append("## PROJECT DIRECTORY STRUCTURE")
        content.append("```")
        content.append(self.generate_tree_structure())
        content.append("```")
        content.append("")

        # File Contents Section
        content.append("## COMPLETE FILE CONTENTS")
        content.append("")

        all_files = self.collect_all_files()
        total_files = len(all_files)

        print(f"Processing {total_files} files...")

        for i, file_path in enumerate(all_files, 1):
            full_path = self.project_root / file_path

            print(f"Processing ({i}/{total_files}): {file_path}")

            # Add file header
            content.append(f"### File: {file_path}")
            content.append(f"**Path:** `{file_path}`")

            try:
                file_stats = full_path.stat()
                content.append(f"**Size:** {file_stats.st_size:,} bytes")
                content.append(
                    f"**Modified:** {datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}"
                )
            except OSError:
                content.append("**Size:** Unable to read")

            content.append("")

            # Add file content if it should be included
            if self.should_include_content(full_path):
                file_content = self.get_file_content(full_path)

                # Determine code block language based on extension
                extension = full_path.suffix.lower()
                if extension == ".py":
                    lang = "python"
                elif extension == ".sh":
                    lang = "bash"
                elif extension in [".yml", ".yaml"]:
                    lang = "yaml"
                elif extension == ".json":
                    lang = "json"
                elif extension == ".md":
                    lang = "markdown"
                else:
                    lang = "text"

                content.append(f"```{lang}")
                content.append(file_content)
                content.append("```")
            else:
                content.append("*[Binary file or content not included]*")

            content.append("")
            content.append("-" * 80)
            content.append("")

        # Write to file
        output_path = self.project_root / self.output_file

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"\nKnowledge base generated successfully!")
        print(f"Output file: {output_path}")
        print(f"File size: {output_path.stat().st_size:,} bytes")
        print(f"Total files processed: {total_files}")

        return str(output_path)


def main():
    """Main function to run the knowledge base extractor"""
    print("Agentic Fabric POC - Knowledge Base Extractor")
    print("=" * 50)

    # Check if we're in a project directory
    current_dir = Path.cwd()

    # Look for project indicators
    project_indicators = ["config", "agents", "core", "requirements.txt"]
    has_indicators = any(
        (current_dir / indicator).exists() for indicator in project_indicators
    )

    if not has_indicators:
        print(
            "Warning: Current directory doesn't appear to be the Agentic Fabric project root."
        )
        print(f"Current directory: {current_dir}")
        print("Please navigate to your project directory before running this script.")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != "y":
            return

    # Create extractor and generate knowledge base
    extractor = ProjectKnowledgeExtractor()
    output_file = extractor.generate_knowledge_base()

    print(f"\nKnowledge base created: {output_file}")
    print("\nThis file contains:")
    print("- Complete directory structure")
    print("- All source code files with full content")
    print("- Project configuration and documentation")
    print("- Environment setup information")
    print("- Implementation status and next steps")
    print("\nYou can use this file as context for LLM continuation of the project.")


if __name__ == "__main__":
    main()
