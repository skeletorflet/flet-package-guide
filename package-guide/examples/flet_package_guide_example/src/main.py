import flet as ft
from flet_package_guide import FletPackageGuide
import json # Added import for json


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def get_random():
        return FletPackageGuide(
            colors=[ft.Colors.RED, ft.Colors.BLUE, ft.Colors.PRIMARY],
            content=ft.Icon(ft.Icons.ABC),
            on_something=lambda e: print(e.data),
            complex_data={
                "hello": "world",
                "foo": "bar",
                "arrs": {"int": 1, "bool": True, "double": 1.123, "list": ["a", 2, True, [[2], 1]], "size": {"width":300, "height":300}},
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
            periodic_event_text.value = f"Dart periodic event: Counter = {data.get('counter', 'N/A')}"
            # periodic_event_text.update() # Updating the text control individually
            page.update() # Update the whole page to show changes
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
    )


ft.app(main)
