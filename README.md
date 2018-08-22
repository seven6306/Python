CNBL Jenkins CI/CD
==================
![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Jenkins_logo_with_title.svg/640px-Jenkins_logo_with_title.svg.png)
## Overview
 * [Introduction](#workflow)
 * [BIOS Auto Build](#build)
 * [BIOS Auto Release](#release)
 * [BIOS Dairy Report Mechanism](#report)
 * [BIOS Check Setup Item Mechanism](#setup)
 * [Jenkins Send Mail Mechanism](#mail)
 * [BIOS Team Mail Address](#address)

---
## Workflow
Please refer to **http://10.6.75.10:8081/**

#### Description
This build code server is based on Jenkins agent,
It's a job proxy server, build on docker container.

#### Agent Server Connection
1.  **[Agent Connect](http://10.6.75.10:8081/computer/WIN-BUILD-CODE-SERVER/)**
2.  Click Launch agent from browser button, will download the **slave-agent.jnlp**
3.  Run slave-agent.jnlp to connect the master server.
4.  Permanently accept the application access.
5.  When status changed to connected, Jenkins agent was done!

#### Working Space
D:\Jenkins\workspace

#### Python Tool Directory
D:\python_script

#### Veb Tools Directory
D:\Veb30_7

---

## BIOS Auto Build
<a name="build"/>
1.  Job View: [KINGLER1P](http://10.6.75.10:8081/view/KINGLER-1P)

2.  Schedule: **A.M. 03:00**

3.  Build Directory
    e.g., D:\Jenkins\workspace\KINGLER1P-BUILD-BIOS-DAIRY

4.  Python Tools:
    * Rebuild.bat
    * ProjectSelector.py
    * BuildResult.py
    * BuildRetry.py
    * CheckSetup.py
    * EnvironInjector.py

---

## BIOS Auto Release
<a name="release"/>
1.  Job View: [KUNLUNS](http://10.6.75.10:8081/job/KUNLUNS-BUILD-BIOS-RELEASE/ "Title")

2.  Build Directory
    e.g., D:\Jenkins\workspace\KINGLER1P-BUILD-BIOS-RELEASE

3.  Afu Tools: D:\afu_tools (case1: KINGLER, case2:AS60G1, case3:EXEGGCUTE)

4.  Python Tools:
    * Rebuild.bat
    * ProjectSelector.py
    * BuildResult.py
    * EnvironInjector.py
    * Func7zip.py
    * ArchivePackage.py

---

## BIOS Dairy Report Mechanism
When all the project scheduled build finished, the job **PROJECT-BUILD-BIOS-CHECK** will start to check the
file **build_message** below each dairy build project directory, to generate a data for groovy script:
**groovy-html-report.template**, more detail to refer to [Jenkins Send Mail Mechanism](#mail).
<a name="report"/>
1.  Job View: **[PROJECT-BUILD-BIOS-CHECK](http://10.6.75.10:8081/job/PROJECT-BUILD-BIOS-CHECK/)**

2.  Schedule: **A.M. 03:00**

3.  Python Tool: **CollectResults.py**

4.  Collect File: **build_message**
    e.g., D:\Jenkins\workspace\KINGLER1P-BUILD-BIOS-DAIRY\build_message

5.  Physical Path: D:\Jenkins\workspace\PROJECT-BUILD-BIOS-CHECK

---

## BIOS Check Setup Item Mechanism
Auto compare the Setup.Type between backup and build directory (contains all struct),
currently work project only KINGLER1P.
<a name="setup"/>
1.  Backup Directory: **D:\SetupBackup**

2.  Check Tool: **CheckSetup.py**

---

## Jenkins Send Mail Mechanism
**Settings:**
[Jenkins / Management Jenkins / Editable Email Template Management / svn_temp or svn_temp_release](http://10.6.75.10:8081/emailexttemplates/)
<a name="mail"/>
1.  Groovy Script: **D:\Jenkins_script**

2.  Result Template: **template_svn.jelly**
According build result, if fail then send result mail to BIOS team, else not.

3.  Collect Result Pipline: **Jenkinsfile.server.reports**
    * The job on jenkins use to collect each dairy build result and arrange these results to groovy variables.
    * At last send the report list to BIOS team.
    
4.  Report Template: groovy-html-report.template
The template will decorate the result data from CollectResults.py then parse to job environment variables.

---

## BIOS Team Mail Address:

 * Ciou.Beck@inventec.com
 * TAO03GE@inventec.com
<a name="address"/>
