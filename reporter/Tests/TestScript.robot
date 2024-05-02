*** Test Cases ***
Simple Log Message
    Log    Hello, world!

Log Multiple Messages
    Log    Hello, world!
    Log    This is another message

Skiped Test
    Log    This test is skipped
    Skip    This test is skipped

Failed Test
    Log    This test will fail
    Fail    This test failed