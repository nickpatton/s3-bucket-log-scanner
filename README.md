# s3 bucket log scanner
This is a python script I wrote as part of a technical interview for a devops role at a certain startup that I won't name. I don't think I did too well during the actual interview, but I thought the challenge was interesting and wanted to finish it afterwards.

Assignment:
>Write a script to scan this bucket s3://some-bucket, read the latest zip file, unzip it and see if the logs contain errors. If there are errors, print them.

Example log file being processed:
<pre>
[2020-01-07 00:17:27,898]           session.py:L436   WARNING: Terminated session for application AVP7HJL: Address renetered in CCA
[2020-01-07 00:17:27,898]           session.py:L440     ERROR: Address renetered in CCA
Traceback (most recent call last):
  File "/home/taskrunner/virtualenvs/selenium-scripts_py3/src/process-paths/process_paths/session.py", line 316, in _map
    app_session.map_output = self.map(app_session)
  File "/home/taskrunner/virtualenvs/selenium-scripts_py3/src/process-paths/process_paths/session.py", line 916, in map
    app_session=app_session,
  File "/tmp/orchestrator_24516598_1578356066/selenium-scripts/crawls/cca/verification_documentation.py", line 83, in manage_verifications
    raise KnownException('Address renetered in CCA')
core.exceptions.KnownException: Address renetered in CCA
[2020-01-07 00:17:27,898]           session.py:L577      INFO: All tags added for AVP7HJL
[2020-01-07 00:17:27,899]           session.py:L577      INFO: All tags resolved for AVP7HJL
</pre>

As with most coding solutions, I'm sure there's a much more elegant solution than mine, but it seemed easiest to use a regex that matched on the timestamp-prefixed log lines and then assume that non-matching lines are part of some stacktrace. My script output the lines of the stacktrace, but didn't include the 'ERROR: Address renetered in CCA' line because it matched my regex with the timestamp at the beginning of the line.