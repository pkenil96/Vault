# secureBox

Hi there! Welcome to kenBox.

This is a "me too" application, which in many aspects resembles to the cloud storage or backup application like dropbox, box etc. I'm designing this applicaiton in an attempt to learn and explore the following:

1) Authentication System: Direct login; SSO login using SAML assertions 
2) API: Boto3 to interact with Amazon S3 buckets

This is an attempt to learn system design at a high level and also get some real time coding skills by writing API(s). The authentication system will be built atop Python-Flask. In order to comprehend how a modern authentication system works, i'll be intgrating SSO login to the application using one of the many well known IDP(s): Octa, PingOne or siteminder whichever is easier. The idea is to desig a simple SSO login using SAML assertions with a minimal and least fanciful UI. 

Later post authentcation, the plan would be to deveop a wrapper application on Amazon S3 to create customized storage application.

As this is a wrapper application, there is an exhaustive list of functionalities that can be added and therefore I'll be adding all the use cases here as i move ahead. Once a basic application is built, the plan is to create a layer of security to secure the data that the application hosts and come up with different ways to ensure that the data is secure.

