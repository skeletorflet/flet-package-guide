import flet as ft
from flet_package_guide import (
    FletPackageGuide,
    UrlLauncherControl,
)  # Import UrlLauncherControl
import json  # Added import for json


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    def get_random():
        return FletPackageGuide(
            colors=[ft.Colors.RED, ft.Colors.BLUE, ft.Colors.PRIMARY],
            content=ft.Icon(ft.Icons.ABC),
            on_something=lambda e: print(e.data),
            complex_data={
                "hello": "world",
                "foo": "bar",
                "arrs": {
                    "int": 1,
                    "bool": True,
                    "double": 1.123,
                    "list": ["a", 2, True, [[2], 1]],
                    "size": {"width": 300, "height": 300},
                },
            },
        )

    def click(e):
        package.colors = [ft.Colors.random() for i in range(3)]
        package.content = ft.Icon(ft.Icons.random(), color=ft.Colors.random())
        print(package.complex_data["hello"])
        package.update()

    package = get_random()

    # Setup for Dart periodic event
    periodic_event_text = ft.Text("Waiting for Dart periodic event...")

    def handle_dart_periodic_event(e):
        # e.data is expected to be a JSON string like '{"counter": 1}'
        # print(f"Raw periodic event data: {e.data}") # For debugging
        try:
            data = json.loads(e.data)
            periodic_event_text.value = (
                f"Dart periodic event: Counter = {data.get('counter', 'N/A')}"
            )
            # periodic_event_text.update() # Updating the text control individually
            page.update()  # Update the whole page to show changes
        except json.JSONDecodeError:
            periodic_event_text.value = "Error decoding periodic event data."
            # periodic_event_text.update()
            page.update()
        except Exception as ex:
            periodic_event_text.value = f"Error handling periodic event: {ex}"
            # periodic_event_text.update()
            page.update()

    # Assign the handler to the package instance.
    # This will also set package.enable_periodic_events = True due to the setter logic in FletPackageGuide.
    package.on_dart_periodic_event = handle_dart_periodic_event
    # To explicitly enable (though the above line should do it):
    # package.enable_periodic_events = True
    # package.update() # If enable_periodic_events was set explicitly after instantiation and requires an update.

    # --- Text controls for Robust Error Handling Example ---
    error_handling_success_text = ft.Text(
        "Result of successful Dart call will appear here."
    )
    error_handling_failure_text = ft.Text(
        "Result of failing Dart call will appear here."
    )

    # --- Text control for Bi-directional Shared Value Example ---
    shared_value_display_text = ft.Text(
        f"Shared Value: {package.shared_value}"
    )  # Initialize with current value

    # --- UrlLauncherControl Setup ---
    url_input = ft.TextField(
        label="Enter URL", value="https://flet.dev", width=page.width * 0.8
    )
    url_launcher_status = ft.Text("URL Launcher status will appear here.")
    launcher_control = UrlLauncherControl()  # Create an instance

    # --- Handlers for UrlLauncherControl ---
    def do_launch_url(e):
        if not url_input.value:
            url_launcher_status.value = "Please enter a URL."
            url_launcher_status.update()
            return
        launcher_control.launch_url(url_input.value)
        url_launcher_status.value = launcher_control.last_result or "No result yet."
        url_launcher_status.update()

    def refresh_launcher_status(e):
        url_launcher_status.value = launcher_control.last_result or "No result yet."
        url_launcher_status.update()

    # --- Handlers for Robust Error Handling Example ---
    def test_dart_success(e):
        result = package.call_dart_that_might_fail(should_fail=False)
        error_handling_success_text.value = str(result)
        error_handling_success_text.update()
        # page.update()

    def test_dart_failure(e):
        result = package.call_dart_that_might_fail(should_fail=True)
        error_handling_failure_text.value = str(result)
        error_handling_failure_text.update()
        # page.update()

    # --- Handlers for Bi-directional Shared Value Example ---
    def handle_shared_value_update_from_control(e):
        # This handler is called when Python's _on_shared_value_changed_from_dart
        # calls the public on_shared_value_changed event.
        shared_value_display_text.value = f"Shared Value (event): {e.data}"
        shared_value_display_text.update()
        # page.update()

    # Assign the handler to the package instance
    package.on_shared_value_changed = handle_shared_value_update_from_control

    def refresh_shared_value_display(e=None):  # Allow calling without event
        shared_value_display_text.value = (
            f"Shared Value (polled): {package.shared_value}"
        )
        shared_value_display_text.update()
        # page.update()

    def increment_from_python_button_click(e):
        package.increment_shared_value_from_python()
        # The shared_value attribute change in Python should trigger an update in Dart.
        # We also need to update our Python display.
        refresh_shared_value_display()  # Update the text display

    # Handler for async results (from example 1)
    def handle_async_result(data):
        """
        Handles the result from the asynchronous Dart operation.
        """
        print(f"Async result received in Python: {data}")
        # You can update the Flet UI here if needed, for example:
        # page.add(ft.Text(f"Async result: {data}"))
        # page.update()

    # --- Handlers for Task with Progress (Example 4) ---
    task_progress_text = ft.Text("Task progress will appear here.")
    task_status_text = ft.Text("Task status: Idle")

    def handle_task_progress(event_data):
        """Handles progress updates from the Dart task."""
        try:
            task_id_short = event_data.get("task_id", "Unknown")[:8]
            current_step = event_data.get("current_step", "?")
            total_steps = event_data.get("total_steps", "?")
            task_progress_text.value = (
                f"Progress: Task {task_id_short} - Step {current_step}/{total_steps}"
            )
            task_progress_text.update()  # Use individual control update if page update is too broad
            # page.update() # Or update the whole page
        except Exception as ex:
            task_progress_text.value = f"Error in progress handler: {ex}"
            task_progress_text.update()

    def handle_task_completion(event_data):
        """Handles the completion event from the Dart task."""
        try:
            task_id_short = event_data.get("task_id", "Unknown")[:8]
            message = event_data.get("message", "No message.")
            task_status_text.value = f"Status: Task {task_id_short} - {message}"
            task_progress_text.value = ""  # Clear progress text
            task_status_text.update()
            task_progress_text.update()
            # page.update() # Or update the whole page
        except Exception as ex:
            task_status_text.value = f"Error in completion handler: {ex}"
            task_status_text.update()

    def start_the_task(e):
        """Initiates the task with progress updates via the FletPackageGuide instance."""
        task_status_text.value = "Task status: Initiating..."
        task_progress_text.value = "Waiting for first progress..."
        # It's good practice to update the UI immediately after user action
        task_status_text.update()
        task_progress_text.update()
        # page.update()

        package.start_task_with_progress_updates(
            total_steps=5,  # Example: a task with 5 steps
            progress_handler=handle_task_progress,
            completion_handler=handle_task_completion,
        )

    # Button to start the task (defined globally to be added to page layout)
    start_progress_task_button = ft.Button(
        "Start Task with Progress", on_click=start_the_task
    )

    page.add(
        ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.PURPLE_200,
            content=ft.Column([package], expand=True),
        ),
        ft.Button("Go!", on_click=click),
        ft.Button("Go!", on_click=lambda e: print(package.play(" hello"))),
        ft.Button("Go!", on_click=lambda e: print(package.stop(" bye bye"))),
        ft.Button(
            "Test Async Callback",
            on_click=lambda e: package.async_operation_with_callback(
                "Hello Dart from Async Python!", handle_async_result
            ),
        ),
        ft.Text("Results for timeout tests will appear in console."),
        ft.Button(
            "Call Dart: Fast Task (should succeed)",
            on_click=lambda e: print(
                package.call_dart_with_timeout(
                    data_to_send="Process this fast",
                    python_timeout_sec=2.0,  # Python waits for 2 seconds
                    dart_task_duration_ms=1000,  # Dart task runs for 1 second
                )
            ),
        ),
        ft.Button(
            "Call Dart: Slow Task (should timeout)",
            on_click=lambda e: print(
                package.call_dart_with_timeout(
                    data_to_send="Process this slowly",
                    python_timeout_sec=1.0,  # Python waits for 1 second
                    dart_task_duration_ms=2000,  # Dart task runs for 2 seconds
                )
            ),
        ),
        periodic_event_text,  # Add the text control to the page
        ft.Divider(),  # Visual separator
        ft.Text("Task with Progress Example:"),
        task_progress_text,
        task_status_text,
        start_progress_task_button,
        ft.Divider(),
        ft.Text("Robust Error Handling Example:"),
        ft.ElevatedButton("Call Dart (Expect Success)", on_click=test_dart_success),
        error_handling_success_text,
        ft.ElevatedButton("Call Dart (Expect Failure)", on_click=test_dart_failure),
        error_handling_failure_text,
        ft.Divider(),
        ft.Text("Bi-directional Shared Value Example:"),
        shared_value_display_text,
        ft.ElevatedButton(
            "Increment from Python & Refresh Display",
            on_click=increment_from_python_button_click,
        ),
        ft.ElevatedButton(
            "Refresh Display from Python Attribute",
            on_click=refresh_shared_value_display,
        ),
        ft.Text(
            "Note: The Dart side of the control (purple box area) has its own 'Increment from Dart' button."
        ),
        ft.Divider(),
        ft.Text("URL Launcher Example:"),
        launcher_control,  # Add the control itself to the page (displays Dart UI)
        url_input,
        ft.ElevatedButton("Launch URL", on_click=do_launch_url),
        url_launcher_status,
        ft.ElevatedButton(
            "Refresh Last Launch Result", on_click=refresh_launcher_status
        ),
    )


ft.app(main)
