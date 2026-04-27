"""Search tools for code and text."""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from jarvis.utils.logger import log


class SearchTools:
    """Tools for searching in files and directories."""
    
    @staticmethod
    def grep(pattern: str, path: str = ".", recursive: bool = True, 
             include_pattern: str = None) -> List[Dict[str, Any]]:
        """
        Search for a pattern in files (like grep).
        
        Args:
            pattern: Regex pattern to search for
            path: Directory to search in
            recursive: Whether to search recursively
            include_pattern: File pattern to include (e.g., "*.py")
        
        Returns:
            List of matches with file, line number, and content
        """
        log("🔍", f"Searching for pattern: {pattern} in {path}")
        
        matches = []
        path_obj = Path(path)
        
        if not path_obj.exists():
            return [{"error": f"Path not found: {path}"}]
        
        # Get files to search
        if recursive:
            if include_pattern:
                files = path_obj.rglob(include_pattern)
            else:
                files = path_obj.rglob("*")
        else:
            if include_pattern:
                files = path_obj.glob(include_pattern)
            else:
                files = path_obj.glob("*")
        
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            
            for file_path in files:
                if file_path.is_file():
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            for line_num, line in enumerate(f, 1):
                                if regex.search(line):
                                    matches.append({
                                        "file": str(file_path),
                                        "line_number": line_num,
                                        "content": line.strip()
                                    })
                    except Exception as e:
                        log("⚠️", f"Error reading {file_path}: {e}")
            
            log("✅", f"Found {len(matches)} matches")
            return matches
            
        except re.error as e:
            error_msg = f"Invalid regex pattern: {str(e)}"
            log("❌", error_msg)
            return [{"error": error_msg}]
    
    @staticmethod
    def find_files(pattern: str, path: str = ".", recursive: bool = True) -> List[str]:
        """
        Find files matching a pattern.
        
        Args:
            pattern: File pattern (e.g., "*.py", "test_*")
            path: Directory to search in
            recursive: Whether to search recursively
        
        Returns:
            List of matching file paths
        """
        log("📁", f"Finding files matching: {pattern} in {path}")
        
        path_obj = Path(path)
        
        if not path_obj.exists():
            return [f"Error: Path not found: {path}"]
        
        if recursive:
            files = list(path_obj.rglob(pattern))
        else:
            files = list(path_obj.glob(pattern))
        
        result = [str(f) for f in files if f.is_file()]
        log("✅", f"Found {len(result)} files")
        return result
    
    @staticmethod
    def find_directories(pattern: str, path: str = ".", recursive: bool = True) -> List[str]:
        """
        Find directories matching a pattern.
        
        Args:
            pattern: Directory pattern
            path: Directory to search in
            recursive: Whether to search recursively
        
        Returns:
            List of matching directory paths
        """
        log("📂", f"Finding directories matching: {pattern} in {path}")
        
        path_obj = Path(path)
        
        if not path_obj.exists():
            return [f"Error: Path not found: {path}"]
        
        if recursive:
            dirs = list(path_obj.rglob(pattern))
        else:
            dirs = list(path_obj.glob(pattern))
        
        result = [str(d) for d in dirs if d.is_dir()]
        log("✅", f"Found {len(result)} directories")
        return result
    
    @staticmethod
    def search_in_file(content: str, pattern: str) -> List[Dict[str, Any]]:
        """
        Search for a pattern in given content.
        
        Args:
            content: Text content to search in
            pattern: Pattern to search for
        
        Returns:
            List of matches with line numbers
        """
        log("🔎", f"Searching pattern in content")
        
        matches = []
        lines = content.split("\n")
        
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            
            for line_num, line in enumerate(lines, 1):
                if regex.search(line):
                    matches.append({
                        "line_number": line_num,
                        "content": line.strip()
                    })
            
            return matches
            
        except re.error as e:
            return [{"error": f"Invalid regex: {str(e)}"}]
