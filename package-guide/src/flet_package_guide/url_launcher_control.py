from typing import Optional
from flet import Control, Page
import flet.core.types as types
import concurrent.futures

class UrlLauncherControl(Control):
    """
    A Flet control that wraps the url_launcher Flutter package
    to allow opening URLs.
    """

    def __init__(
        self,
        # Common control properties
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: any = None,
    ):
        Control.__init__(
            self, ref=ref, visible=visible, disabled=disabled, data=data
        )
        self._last_result = None

    def _get_control_name(self):
        return "url_launcher_control" # Name of the Flutter control

    def launch_url(self, url: str) -> bool:
        """
        Attempts to launch the given URL.
        Returns True if successful, False otherwise.
        """
        if not url:
            self._last_result = "Error: URL cannot be empty."
            if self.page: self.page.update() # To update any bound display
            return False
        try:
            # invoke_method returns the result from Dart, which should be a boolean string "true" or "false"
            # or an error string.
            result_str = self.invoke_method(
                "launch_url", {"url": url}, wait_for_result=True
            )

            if isinstance(result_str, str):
                if result_str == "true":
                    self._last_result = f"Successfully launched {url}"
                    if self.page: self.page.update()
                    return True
                elif result_str == "false":
                    self._last_result = f"Failed to launch {url} (Dart returned false)"
                    if self.page: self.page.update()
                    return False
                else: # Expected an error message from Dart
                    self._last_result = f"Failed to launch {url}: {result_str}"
                    if self.page: self.page.update()
                    return False
            else: # Should not happen if Dart side is correct
                self._last_result = f"Unexpected result type from Dart for {url}: {result_str}"
                if self.page: self.page.update()
                return False

        except concurrent.futures.TimeoutError:
            self._last_result = f"Timeout: Did not hear back from Dart while trying to launch {url}."
            if self.page: self.page.update()
            return False
        except Exception as e:
            self._last_result = f"Error launching URL {url}: {e}"
            if self.page: self.page.update()
            return False

    @property
    def last_result(self) -> Optional[str]:
        return self._last_result

    # We don't need _get_children for this simple control
    # We don't have specific attributes to set from Python other than method calls for this example
