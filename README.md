# `Cutesy_MVC` Framework

[Template Repository available here.](https://github.com/dvanderweele/Cutesy_MVC_Template)

## Overview

Tentatively calling this project "Cutesy_MVC." I'll probably call the command-line utility component something masculine like "cutify." Taylor Otwell doesn't have anything on my ability to name things.

Literally developing this at least in the preliminary stages on Replit on my phone. Just would like to practice python when I have the time, and also would be cool if the end product was something useful to me. 

Taking inspiration from a favorite project of mine: Laravel. Would also like to practice threading a bit, so my idea is to basically have a client-server model where the V of the MVC is on the main thread and the M and C of MVC are on a second thread. The View/User Interface library or system is really up to the user, this framework is agnostic. The `Client` module enables communication between a server thread (that runs most of the other framework systems) and the main thread where the UI lives. These components on the main thread will generate request objects that are sent via queue to the server thread, which eventually sends back a response object via another queue.

Obviously being a solo project that draws inspiration from a major project, I am not implementing all of the features of Laravel. For example, I am creating systems to migrate, query, and model data from SQLite, but I am not building support for any other database systems.

## Tests

To run the framework's tests (i.e., not user-defined tests), run the project as a module from the directory above repo.

```
python -m Cutesy_MVC
```

## Docs

Markdown formatted documentation files can be found in the docs folder.

### Table of Contents

[1 - Database Migrations](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/migrations.md)

[2 - Database Query Tools](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/db.md)

[3 - Cutify Command Line Utility](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/cutify.md)

[4 - The Cutesy ORM and Data Modeling](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/model.md)

[5 - Routing](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/routes.md)

[6 - Controllers](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/controllers.md)

[7 - Client](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/client.md)

[8 - StringBuilder](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/string.md)

[9 - Testing](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/test.md)

[10 - UI State Store](https://github.com/dvanderweele/Cutesy_MVC/blob/master/docs/UI.md)
