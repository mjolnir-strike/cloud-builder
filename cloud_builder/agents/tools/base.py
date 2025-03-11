"""Base tool implementation for Terraform analysis"""
from typing import Any
from crewai.tools import BaseTool

class TerraformTool(BaseTool):
    """Base class for all Terraform analysis tools"""
    name: str
    description: str

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the tool's analysis"""
        return self.__call__(*args, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Implement this method in subclasses"""
        raise NotImplementedError
