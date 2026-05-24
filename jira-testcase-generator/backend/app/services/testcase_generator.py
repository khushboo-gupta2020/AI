import re
from app.models.schemas import JiraStory, TestCase


class TestCaseGenerator:
    def __init__(self, story: JiraStory):
        self.story = story

    def generate(self) -> list[TestCase]:
        test_cases = []
        test_cases.extend(self._generate_positive_tests())
        test_cases.extend(self._generate_negative_tests())
        test_cases.extend(self._generate_boundary_tests())
        test_cases.extend(self._generate_acceptance_criteria_tests())

        for i, tc in enumerate(test_cases, 1):
            tc.test_case_id = f"TC-{self.story.key}-{i:03d}"

        return test_cases

    def _generate_positive_tests(self) -> list[TestCase]:
        tests = []
        summary = self.story.summary
        description = self.story.description

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Happy Path",
            preconditions="User is logged in and has appropriate permissions",
            test_steps=f"1. Navigate to the relevant feature/module\n2. Perform the primary action described in the user story\n3. Verify all required inputs are provided\n4. Submit/execute the action",
            expected_result=f"The system successfully processes the request as described in: {summary}",
            priority="High",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Standard User Flow",
            preconditions="User is on the relevant page with valid session",
            test_steps=f"1. Access the feature from the main navigation\n2. Enter valid data for all required fields\n3. Review the entered information\n4. Confirm/submit the action",
            expected_result="The system processes the request and displays a success confirmation",
            priority="High",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Data Persistence",
            preconditions="User has completed the primary action successfully",
            test_steps="1. Complete the user story workflow\n2. Navigate away from the page\n3. Return to the feature/module\n4. Verify the previously entered data",
            expected_result="All data from the previous session is persisted and displayed correctly",
            priority="Medium",
        ))

        return tests

    def _generate_negative_tests(self) -> list[TestCase]:
        tests = []
        summary = self.story.summary

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Missing Required Fields",
            preconditions="User is on the input form/page",
            test_steps="1. Leave all required fields empty\n2. Attempt to submit the form\n3. Observe validation messages",
            expected_result="The system displays appropriate error messages for each missing required field and prevents submission",
            priority="High",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Invalid Data Input",
            preconditions="User is on the input form/page",
            test_steps="1. Enter invalid data types in fields (e.g., special characters in numeric fields, invalid email format)\n2. Enter excessively long strings\n3. Attempt to submit",
            expected_result="The system validates input and displays appropriate error messages without crashing",
            priority="High",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Unauthorized Access",
            preconditions="User is not logged in or lacks required permissions",
            test_steps="1. Attempt to access the feature without authentication\n2. Attempt to access with insufficient permissions\n3. Observe system response",
            expected_result="The system denies access and redirects to login or displays an appropriate error message",
            priority="High",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Session Timeout Handling",
            preconditions="User has started the workflow but session expires",
            test_steps="1. Begin the user story workflow\n2. Wait for session to expire or manually clear session\n3. Attempt to submit/complete the action\n4. Observe system behavior",
            expected_result="The system detects the expired session and prompts the user to re-authenticate without losing entered data",
            priority="Medium",
        ))

        return tests

    def _generate_boundary_tests(self) -> list[TestCase]:
        tests = []
        summary = self.story.summary

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Boundary Value Analysis",
            preconditions="User is on the input form/page with numeric or length-restricted fields",
            test_steps="1. Enter minimum allowed values\n2. Enter maximum allowed values\n3. Enter values just below minimum and just above maximum\n4. Submit each variation",
            expected_result="The system accepts values at boundaries and rejects values outside boundaries with appropriate messages",
            priority="Medium",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Large Data Volume",
            preconditions="System is configured with standard limits",
            test_steps="1. Prepare a large dataset or bulk entries\n2. Attempt to process/submit the large volume\n3. Monitor system performance and response",
            expected_result="The system handles large data volumes gracefully with appropriate loading indicators and no performance degradation",
            priority="Medium",
        ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Concurrent User Actions",
            preconditions="Multiple users have access to the same feature",
            test_steps="1. User A begins an action on a shared resource\n2. User B simultaneously attempts the same action\n3. Observe system handling of concurrent access",
            expected_result="The system handles concurrent access appropriately with locking, queuing, or conflict resolution",
            priority="Low",
        ))

        return tests

    def _generate_acceptance_criteria_tests(self) -> list[TestCase]:
        tests = []
        ac = self.story.acceptance_criteria
        summary = self.story.summary

        if ac:
            ac_items = self._parse_acceptance_criteria(ac)
            for i, item in enumerate(ac_items[:3]):
                tests.append(TestCase(
                    test_case_id="",
                    test_scenario=f"Verify AC{i+1}: {item[:80]}{'...' if len(item) > 80 else ''}",
                    preconditions="User is on the relevant feature page",
                    test_steps=f"1. Review acceptance criteria: {item}\n2. Perform actions to validate the criteria\n3. Verify the expected behavior matches the acceptance criteria",
                    expected_result=f"The system behavior matches the acceptance criteria: {item}",
                    priority="High",
                ))
        else:
            tests.append(TestCase(
                test_case_id="",
                test_scenario=f"Verify {summary} - General Acceptance Criteria Validation",
                preconditions="User story has been implemented",
                test_steps="1. Review the user story description\n2. Execute the primary workflow\n3. Verify all described behaviors are implemented correctly",
                expected_result="All behaviors described in the user story are implemented and functioning correctly",
                priority="High",
            ))

        tests.append(TestCase(
            test_case_id="",
            test_scenario=f"Verify {summary} - Cross-Browser/Device Compatibility",
            preconditions="Application is deployed and accessible",
            test_steps="1. Open the feature in multiple browsers (Chrome, Firefox, Safari, Edge)\n2. Test on different screen sizes (desktop, tablet, mobile)\n3. Verify consistent behavior and layout",
            expected_result="The feature works correctly across all supported browsers and devices with consistent UI/UX",
            priority="Low",
        ))

        return tests

    @staticmethod
    def _parse_acceptance_criteria(ac_text: str) -> list[str]:
        items = []
        lines = ac_text.split("\n")
        current_item = ""

        for line in lines:
            stripped = line.strip()
            if re.match(r'^[\d\*\-\•]+[\.\)]?\s', stripped) or re.match(r'^(Given|When|Then|And|But)', stripped, re.IGNORECASE):
                if current_item:
                    items.append(current_item.strip())
                current_item = stripped
            elif stripped:
                current_item += " " + stripped

        if current_item:
            items.append(current_item.strip())

        if not items and ac_text.strip():
            items = [item.strip() for item in re.split(r'[;\n]', ac_text) if item.strip()]

        return items if items else [ac_text.strip()]
