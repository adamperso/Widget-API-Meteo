"""Shell command execution tools for Jarvis."""

import subprocess
from typing import Optional, Dict, Any
from jarvis.utils.logger import log


class ShellTools:
    """Tools for executing shell commands."""
    
    @staticmethod
    def run_command(command: str, timeout: int = 30, cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a shell command.
        
        Args:
            command: The command to execute
            timeout: Maximum execution time in seconds
            cwd: Working directory for the command
        
        Returns:
            Dictionary with stdout, stderr, returncode
        """
        log("💻", f"Running command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
            
            if output["success"]:
                log("✅", f"Command executed successfully")
            else:
                log("❌", f"Command failed with code {result.returncode}")
            
            return output
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after {timeout} seconds"
            log("⏱️", error_msg)
            return {
                "stdout": "",
                "stderr": error_msg,
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            log("❌", error_msg)
            return {
                "stdout": "",
                "stderr": error_msg,
                "returncode": -1,
                "success": False
            }
    
    @staticmethod
    def run_python(code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code.
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
        
        Returns:
            Dictionary with output and success status
        """
        log("🐍", "Executing Python code")
        
        try:
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Python code timed out after {timeout} seconds",
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error: {str(e)}",
                "returncode": -1,
                "success": False
            }
    
    @staticmethod
    def check_command_exists(command: str) -> bool:
        """Check if a command exists in the system."""
        try:
            result = subprocess.run(
                ["which", command],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
