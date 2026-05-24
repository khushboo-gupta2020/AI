import re
from datetime import datetime


class TestCaseGenerator:
    def __init__(self):
        self.counter = 0

    def generate(self, story_data):
        summary = story_data.get("summary", "")
        description = story_data.get("description", "")
        acceptance_criteria = story_data.get("acceptance_criteria", "")
        priority = story_data.get("priority", "Medium")
        labels = story_data.get("labels", [])

        content = f"{summary} {description} {acceptance_criteria}"
        content_lower = content.lower()

        test_cases = []
        test_cases.extend(self._generate_positive_cases(summary, content))
        test_cases.extend(self._generate_negative_cases(summary, content))
        test_cases.extend(self._generate_boundary_cases(summary, content))
        test_cases.extend(self._generate_edge_cases(summary, content, labels))

        if len(test_cases) < 5:
            test_cases.extend(self._generate_generic_cases(summary, len(test_cases)))

        for i, tc in enumerate(test_cases, 1):
            tc["test_case_id"] = f"TC-{i:03d}"

        return test_cases

    def _generate_positive_cases(self, summary, content):
        cases = []

        if any(kw in content.lower() for kw in ["login", "sign in", "authenticate"]):
            cases.append({
                "test_scenario": "Verify successful login with valid credentials",
                "preconditions": "User account exists and is active",
                "test_steps": "1. Navigate to login page\n2. Enter valid username\n3. Enter valid password\n4. Click Login button",
                "expected_result": "User is successfully logged in and redirected to dashboard",
                "priority": "High"
            })

        if any(kw in content.lower() for kw in ["form", "submit", "input", "field"]):
            cases.append({
                "test_scenario": "Verify form submission with valid data",
                "preconditions": "User has access to the form page",
                "test_steps": "1. Navigate to form page\n2. Fill all required fields with valid data\n3. Click Submit button",
                "expected_result": "Form is submitted successfully and success message is displayed",
                "priority": "High"
            })

        if any(kw in content.lower() for kw in ["search", "filter", "query"]):
            cases.append({
                "test_scenario": "Verify search functionality returns correct results",
                "preconditions": "Searchable data exists in the system",
                "test_steps": "1. Navigate to search page\n2. Enter valid search term\n3. Click Search button",
                "expected_result": "Relevant results matching the search term are displayed",
                "priority": "Medium"
            })

        if any(kw in content.lower() for kw in ["upload", "file", "document", "attach"]):
            cases.append({
                "test_scenario": "Verify file upload with valid file",
                "preconditions": "User has permission to upload files",
                "test_steps": "1. Navigate to upload section\n2. Select a valid file\n3. Click Upload button",
                "expected_result": "File is uploaded successfully and confirmation is displayed",
                "priority": "Medium"
            })

        if any(kw in content.lower() for kw in ["delete", "remove", "cancel"]):
            cases.append({
                "test_scenario": "Verify delete operation with confirmation",
                "preconditions": "Item exists and user has delete permission",
                "test_steps": "1. Navigate to item list\n2. Select item to delete\n3. Click Delete button\n4. Confirm deletion in dialog",
                "expected_result": "Item is deleted successfully and no longer appears in list",
                "priority": "High"
            })

        if any(kw in content.lower() for kw in ["export", "download", "report"]):
            cases.append({
                "test_scenario": "Verify export/download functionality",
                "preconditions": "Data exists for export",
                "test_steps": "1. Navigate to data view\n2. Select export format\n3. Click Export button",
                "expected_result": "File is downloaded in selected format with correct data",
                "priority": "Medium"
            })

        if any(kw in content.lower() for kw in ["email", "notification", "alert", "notify"]):
            cases.append({
                "test_scenario": "Verify email/notification is sent on trigger event",
                "preconditions": "Notification settings are configured",
                "test_steps": "1. Perform action that triggers notification\n2. Check email/inbox",
                "expected_result": "Notification email is received with correct content",
                "priority": "Medium"
            })

        if any(kw in content.lower() for kw in ["permission", "role", "access", "authorization"]):
            cases.append({
                "test_scenario": "Verify user can access authorized resources",
                "preconditions": "User is logged in with valid role",
                "test_steps": "1. Login with user credentials\n2. Navigate to authorized resource\n3. Verify access",
                "expected_result": "User can access the resource without errors",
                "priority": "High"
            })

        if not cases:
            cases.append({
                "test_scenario": f"Verify {summary} works as expected",
                "preconditions": "System is configured and user has access",
                "test_steps": f"1. Navigate to relevant page\n2. Perform primary action for: {summary}\n3. Verify outcome",
                "expected_result": "Feature works as described in user story",
                "priority": "High"
            })

        return cases

    def _generate_negative_cases(self, summary, content):
        cases = []

        if any(kw in content.lower() for kw in ["login", "sign in", "authenticate"]):
            cases.append({
                "test_scenario": "Verify login fails with invalid credentials",
                "preconditions": "User account exists",
                "test_steps": "1. Navigate to login page\n2. Enter invalid username or password\n3. Click Login button",
                "expected_result": "Login fails and appropriate error message is displayed",
                "priority": "High"
            })

        if any(kw in content.lower() for kw in ["form", "submit", "input", "field"]):
            cases.append({
                "test_scenario": "Verify form validation with missing required fields",
                "preconditions": "User has access to the form page",
                "test_steps": "1. Navigate to form page\n2. Leave required fields empty\n3. Click Submit button",
                "expected_result": "Form submission is blocked and validation errors are displayed",
                "priority": "High"
            })

        if any(kw in content.lower() for kw in ["email", "format", "pattern", "validate"]):
            cases.append({
                "test_scenario": "Verify validation rejects invalid email format",
                "preconditions": "Form with email field is accessible",
                "test_steps": "1. Navigate to form\n2. Enter invalid email format\n3. Submit form",
                "expected_result": "Error message indicates invalid email format",
                "priority": "Medium"
            })

        cases.append({
            "test_scenario": "Verify system handles unauthorized access attempt",
            "preconditions": "User is not logged in or lacks permissions",
            "test_steps": "1. Attempt to access protected feature without authentication\n2. Observe system response",
            "expected_result": "Access is denied and user is redirected to login or shown error",
            "priority": "High"
        })

        cases.append({
            "test_scenario": "Verify error handling for invalid input data",
            "preconditions": "Feature accepts user input",
            "test_steps": "1. Navigate to input field\n2. Enter special characters or invalid data\n3. Submit",
            "expected_result": "System handles invalid input gracefully with appropriate error message",
            "priority": "Medium"
        })

        return cases

    def _generate_boundary_cases(self, summary, content):
        cases = []

        cases.append({
            "test_scenario": "Verify behavior with maximum allowed input length",
            "preconditions": "Input field has defined character limits",
            "test_steps": "1. Navigate to input field\n2. Enter maximum allowed characters\n3. Submit",
            "expected_result": "Input is accepted and processed correctly",
            "priority": "Medium"
        })

        cases.append({
            "test_scenario": "Verify behavior with empty/null input",
            "preconditions": "Feature accepts user input",
            "test_steps": "1. Navigate to input field\n2. Leave field empty or enter null value\n3. Submit",
            "expected_result": "System handles empty input appropriately with validation message",
            "priority": "Medium"
        })

        if any(kw in content.lower() for kw in ["list", "page", "pagination", "record"]):
            cases.append({
                "test_scenario": "Verify pagination with large dataset",
                "preconditions": "More records exist than page size",
                "test_steps": "1. Navigate to list view\n2. Verify page navigation\n3. Navigate to last page",
                "expected_result": "All records are paginated correctly and navigation works",
                "priority": "Low"
            })

        return cases

    def _generate_edge_cases(self, summary, content, labels):
        cases = []

        cases.append({
            "test_scenario": "Verify behavior with concurrent user actions",
            "preconditions": "Multiple users have access to the feature",
            "test_steps": "1. Have multiple users perform same action simultaneously\n2. Observe system behavior",
            "expected_result": "System handles concurrent actions without data corruption",
            "priority": "Medium"
        })

        cases.append({
            "test_scenario": "Verify data persistence after page refresh",
            "preconditions": "Data has been entered or saved",
            "test_steps": "1. Complete action and save data\n2. Refresh the page\n3. Verify data state",
            "expected_result": "Saved data persists and displays correctly after refresh",
            "priority": "Low"
        })

        return cases

    def _generate_generic_cases(self, summary, count):
        cases = []
        generic = [
            {
                "test_scenario": f"Verify end-to-end flow for {summary}",
                "preconditions": "All prerequisites are met",
                "test_steps": f"1. Start from initial state\n2. Complete full workflow for {summary}\n3. Verify final state",
                "expected_result": "End-to-end flow completes successfully",
                "priority": "High"
            },
            {
                "test_scenario": "Verify UI/UX elements display correctly",
                "preconditions": "Feature page is accessible",
                "test_steps": "1. Navigate to feature page\n2. Verify all UI elements render correctly\n3. Check responsiveness",
                "expected_result": "All UI elements display correctly across screen sizes",
                "priority": "Low"
            },
            {
                "test_scenario": "Verify accessibility compliance",
                "preconditions": "Feature page is accessible",
                "test_steps": "1. Navigate using keyboard only\n2. Verify screen reader compatibility\n3. Check color contrast",
                "expected_result": "Feature meets accessibility standards",
                "priority": "Low"
            }
        ]
        return generic[:5 - count] if count < 5 else []
