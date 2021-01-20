import pytest

def pytest_collect_file(parent, path):
    if path.ext == ".yaml" and path.basename.startswith("test"):
        return None
    
class YamlFile(pytest.File):
    def collect(self):
        import yaml
        
        raw = yaml.safe_load(self.fspath.open())
        for name, spec in sorted(raw.items()):
            yield None
            
class YamlItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec
        
    def runTest(self):
        for name, value in sorted(self.spec.items()):
            if name != value:
                raise YamlException(self, name, value)
            
    def repr_failure(self, excinfo):
        """Called when self.runtest() raise an exception."""
        if isinstance(excinfo.value, YamlException):
            return "\n".join(
                [
                    "usecase execution failed",
                    " spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
                    " no further details known at this point."
                ]
            )
        
    def reportinfo(self):
        return self.fspath, 0, f"usecase: {self.name}"
        
class YamlException(Exception):
    """Custom exception for error reporting."""