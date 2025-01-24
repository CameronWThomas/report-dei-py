# Overview
As some of you may know, an executive order recently passed to end "radical and wasteful government DEI programs". This means that many an American who's job entails ensuring equity in the workplace will soon be laid off.
In response, people who want to continue to eat have been trying to find ways to stay employed. And some have even taken steps to disguise DEI programs or their job description.
Due to this, the Office of Personnel Management has requested that employees report any such behavior to them via this email address: `DEIAtruth@opm.gov`

Many federal employees may find that their morals prevent them from doing their part in snitching on coworkers and friends who work in a DEIA based program. 
But in many federal spaces, an employee can face "adverse consequences" if they fail to report

report-dei-py attempts to depersonalize this experience by providing the user with a boilerplate template for reporting their friends to the Office of Personnel Management.

Simply populate the following file with a list of offenders:

`./files/offenders.txt`

Once you have your targets in place, execute the script like so

`python ./send_email.py`

It will prompt for some required information to send an email via SMTP. Certain providers, like Gmail, will require an app password. Others may be more complex and require further codebase modifications on the users part.

Let the computer take care of the dirty work for you, so you can spend more time on TikTok.

# Customization
Feel free to modify the email Subjects (`./files/_headerOptions.txt`), which are randomly selected at send time, or the boilerplate text (`./files/_boilerplate.txt`).

# WARNING
UNDER NO CIRCUMSTANCES SHOULD YOU EXECUTE THIS SCRIPT WITH THE TESTING FLAG.

If you accidentally run this script like so...

`python ./send_email.py -t True -c 10 -f 10`

...you will enter testing mode and, for example, send a random first and last name to the OPM every -f (frequency) seconds, until you send -c (count) total emails.

# DOUBLE WARNING 
The above case would likely violate the TOS of any upstanding email provider, so use your noggin and think before calling this in testing mode.