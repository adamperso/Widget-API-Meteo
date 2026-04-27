"""File manipulation tools for Jarvis."""

import os
from pathlib import Path
from typing import List, Optional
from jarvis.utils.logger import log


class FileTools:
    """Tools for file operations: read, write, list."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read contents of a file."""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"Error: File not found: {file_path}"
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            log("📖", f"Read file: {file_path}")
            return content
            
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            log("❌", error_msg)
            return error_msg
    
    @staticmethod
    def write_file(file_path: str, content: str, overwrite: bool = False) -> str:
        """Write content to a file."""
        try:
            path = Path(file_path)
            
            # Check if file exists
            if path.exists() and not overwrite:
                return f"Error: File already exists. Use overwrite=True to replace."
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            log("✍️", f"Wrote file: {file_path}")
            return f"Successfully wrote {len(content)} characters to {file_path}"
            
        except Exception as e:
            error_msg = f"Error writing file: {str(e)}"
            log("❌", error_msg)
            return error_msg
    
    @staticmethod
    def append_file(file_path: str, content: str) -> str:
        """Append content to a file."""
        try:
            path = Path(file_path)
            
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            
            log("➕", f"Appended to file: {file_path}")
            return f"Successfully appended content to {file_path}"
            
        except Exception as e:
            error_msg = f"Error appending to file: {str(e)}"
            log("❌", error_msg)
            return error_msg
    
    @staticmethod
    def list_directory(dir_path: str, recursive: bool = False) -> List[str]:
        """List files in a directory."""
        try:
            path = Path(dir_path)
            
            if not path.exists():
                return [f"Error: Directory not found: {dir_path}"]
            
            if not path.is_dir():
                return [f"Error: Not a directory: {dir_path}"]
            
            files = []
            if recursive:
                for item in path.rglob("*"):
                    files.append(str(item.relative_to(path)))
            else:
                for item in path.iterdir():
                    files.append(item.name)
            
            log("📁", f"Listed directory: {dir_path} ({len(files)} items)")
            return files
            
        except Exception as e:
            error_msg = f"Error listing directory: {str(e)}"
            log("❌", error_msg)
            return [error_msg]
    
    @staticmethod
    def delete_file(file_path: str) -> str:
        """Delete a file."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return f"Error: File not found: {file_path}"
            
            path.unlink()
            log("🗑️", f"Deleted file: {file_path}")
            return f"Successfully deleted: {file_path}"
            
        except Exception as e:
            error_msg = f"Error deleting file: {str(e)}"
            log("❌", error_msg)
            return error_msg
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()
