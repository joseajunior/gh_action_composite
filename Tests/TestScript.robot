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
    Pass    This test failed

Failed Test with Multi line message
    Log    This test will also fail
    Pass    This test failed${\n}This is a multi line message${\n}One More Line
