There are three kinds of test case in the test file
- unit test
- Functional Test
- Integration Test

For  ``unit test``: just running the file is ok
For  ``Functional Test and Integration Test``: 
- replace the **STRING_LIST** in test/main.py with the corresponding STRING_LIST in IntergrationTest.py or FunctionalTest.py
- run /test/main.py in Terminal to setup the judger.
- Then, run /src/main.py in ANOTHER Terminal.
- Finally, input 'y' to run the naive testcase.

Note that the above auto test banned all poping window, you can only see the result of the operation by viewing the switching of pages and terminals output

If you prefer manual test, just run src/naive.py and once you run it, a ATM UI and a open app button will show and you can open multiple app by pressing the open app button.